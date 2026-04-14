import requests
import json
import base64
from collections import defaultdict
from typing import Dict, List, Set


class RepoRelationshipAnalyzer:
    def __init__(self, username: str, token: str = None):
        """
        Initialize GitHub repository relationship analyzer
        
        Args:
            username: GitHub username to scan
            token: Optional GitHub personal access token
        """
        self.username = username
        self.headers = {}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.base_url = 'https://api.github.com'
    
    def get_all_repos(self) -> List[Dict]:
        """Fetch all repositories for the user"""
        repos = []
        page = 1
        
        if self.headers.get('Authorization'):
            url = f'{self.base_url}/user/repos'
            params = {'page': page, 'per_page': 100, 'affiliation': 'owner'}
        else:
            url = f'{self.base_url}/users/{self.username}/repos'
            params = {'page': page, 'per_page': 100, 'type': 'public'}
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                break
            
            data = response.json()
            if not data:
                break
            
            repos.extend(data)
            page += 1
        
        return repos
    
    def get_submodules(self, repo_name: str, repo_owner: str = None) -> List[str]:
        """Extract submodule names from a repository"""
        if repo_owner is None:
            repo_owner = self.username
            
        url = f'{self.base_url}/repos/{repo_owner}/{repo_name}/contents/.gitmodules'
        response = requests.get(url, headers=self.headers)
        
        submodules = []
        
        if response.status_code == 200:
            content = response.json()
            gitmodules_content = base64.b64decode(content['content']).decode('utf-8')
            
            for line in gitmodules_content.split('\n'):
                line = line.strip()
                if line.startswith('url =') or line.startswith('url='):
                    url_part = line.split('=', 1)[1].strip()
                    if self.username in url_part or repo_owner in url_part:
                        repo = url_part.split('/')[-1].replace('.git', '')
                        submodules.append(repo)
        
        return submodules
    
    def analyze_relationships(self) -> Dict:
        """
        Analyze repository relationships and return dependency structure
        
        Returns:
            Dictionary with roots and their dependency trees
        """
        print(f"Scanning repositories for {self.username}...")
        repos = self.get_all_repos()
        print(f"Found {len(repos)} repositories\n")
        
        # Build dependency graph
        dependencies = {}  # repo -> list of submodules
        all_repos = set()
        submodules_set = set()
        
        for repo in repos:
            repo_name = repo['name']
            all_repos.add(repo_name)
            
            print(f"Checking {repo_name}...")
            submodules = self.get_submodules(repo_name, repo['owner']['login'])
            
            if submodules:
                dependencies[repo_name] = submodules
                submodules_set.update(submodules)
        
        # Find root repositories (not used as submodules)
        root_repos = sorted(all_repos - submodules_set)
        
        print(f"\n✓ Found {len(root_repos)} root repositories")
        print(f"✓ Found {len(submodules_set)} submodule repositories")
        
        return {
            'roots': root_repos,
            'dependencies': dependencies,
            'all_repos': sorted(all_repos),
            'submodules': sorted(submodules_set)
        }
    
    def print_relationships(self, analysis: Dict):
        """Print repository relationships in a clear format"""
        print("\n" + "="*70)
        print("REPOSITORY DEPENDENCY ANALYSIS")
        print("="*70)
        
        print(f"\nRoot Repositories: {len(analysis['roots'])}")
        print(f"Total Repositories: {len(analysis['all_repos'])}")
        print(f"Submodule Repositories: {len(analysis['submodules'])}")
        
        print("\n" + "-"*70)
        print("ROOT REPOSITORIES AND THEIR DEPENDENCIES:")
        print("-"*70)
        
        dependencies = analysis['dependencies']
        
        for root in analysis['roots']:
            print(f"\n📦 {root}")
            if root in dependencies:
                self._print_tree(root, dependencies, "")
            else:
                print("   └── (no submodules)")
    
    def _print_tree(self, repo: str, dependencies: Dict, prefix: str, visited: Set = None):
        """Recursively print dependency tree"""
        if visited is None:
            visited = set()
        
        if repo in visited:
            return
        
        visited.add(repo)
        
        if repo in dependencies:
            subs = dependencies[repo]
            for i, sub in enumerate(subs):
                is_last = i == len(subs) - 1
                connector = "└──" if is_last else "├──"
                print(f"{prefix}   {connector} {sub}")
                
                new_prefix = prefix + ("      " if is_last else "   │  ")
                self._print_tree(sub, dependencies, new_prefix, visited)
    
    def get_dependency_depth(self, repo: str, dependencies: Dict, visited: Set = None) -> int:
        """Calculate maximum dependency depth for a repository"""
        if visited is None:
            visited = set()
        
        if repo in visited or repo not in dependencies:
            return 0
        
        visited.add(repo)
        
        max_depth = 0
        for sub in dependencies[repo]:
            depth = self._get_dependency_depth(sub, dependencies, visited.copy())
            max_depth = max(max_depth, depth)
        
        return max_depth + 1
    
    def _get_dependency_depth(self, repo: str, dependencies: Dict, visited: Set) -> int:
        """Helper for dependency depth calculation"""
        if repo in visited or repo not in dependencies:
            return 0
        
        visited.add(repo)
        
        max_depth = 0
        for sub in dependencies[repo]:
            depth = self._get_dependency_depth(sub, dependencies, visited.copy())
            max_depth = max(max_depth, depth)
        
        return max_depth + 1
    
    def get_reverse_dependencies(self, analysis: Dict) -> Dict[str, List[str]]:
        """Find which repositories depend on each repository"""
        reverse_deps = defaultdict(list)
        
        for parent, children in analysis['dependencies'].items():
            for child in children:
                reverse_deps[child].append(parent)
        
        return dict(reverse_deps)
    
    def export_to_json(self, analysis: Dict, filename: str = None):
        """Export analysis to JSON file"""
        if filename is None:
            filename = f"{self.username}_dependencies.json"
        
        # Add reverse dependencies
        analysis['reverse_dependencies'] = self.get_reverse_dependencies(analysis)
        
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"\n📄 JSON exported to: {filename}")
        return filename
    
    def export_to_markdown(self, analysis: Dict, filename: str = None):
        """Export analysis to Markdown file"""
        if filename is None:
            filename = f"{self.username}_dependencies.md"
        
        dependencies = analysis['dependencies']
        reverse_deps = self.get_reverse_dependencies(analysis)
        
        # Sort roots by number of submodules (descending)
        sorted_roots = sorted(
            analysis['roots'],
            key=lambda r: len(dependencies.get(r, [])),
            reverse=True
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# Repository Dependency Analysis: {self.username}\n\n")
            f.write("## Overview\n\n")
            f.write(f"- **Total Repositories:** {len(analysis['all_repos'])}\n")
            f.write(f"- **Root Repositories:** {len(analysis['roots'])}\n")
            f.write(f"- **Submodule Repositories:** {len(analysis['submodules'])}\n")
            f.write(f"- **Repositories with Submodules:** {len(dependencies)}\n\n")
            
            # Root repositories and their dependencies
            f.write("## Root Repositories and Dependencies\n\n")
            f.write("*Sorted by number of submodules (most complex first)*\n\n")
            
            for root in sorted_roots:
                submodule_count = len(dependencies.get(root, []))
                f.write(f"### 📦 {root}")
                if submodule_count > 0:
                    f.write(f" ({submodule_count} submodules)")
                f.write("\n\n")
                
                if root in dependencies:
                    f.write("**Dependencies:**\n\n")
                    self._write_markdown_tree(f, root, dependencies, "", set())
                else:
                    f.write("*No submodules*\n\n")
                f.write("\n")
            
            # Most depended upon
            if reverse_deps:
                f.write("## Most Depended Upon Repositories\n\n")
                f.write("Repositories used as submodules by other projects.\n\n")
                sorted_deps = sorted(reverse_deps.items(), key=lambda x: len(x[1]), reverse=True)
                
                for repo, parents in sorted_deps:
                    f.write(f"### {repo}\n\n")
                    f.write(f"Used by **{len(parents)}** repository(ies):\n\n")
                    for parent in parents:
                        f.write(f"- {parent}\n")
                    f.write("\n")
            
            # Most complex repositories
            if dependencies:
                f.write("## Most Complex Repositories\n\n")
                f.write("Repositories with the most submodules.\n\n")
                sorted_complex = sorted(dependencies.items(), key=lambda x: len(x[1]), reverse=True)
                
                for repo, subs in sorted_complex:
                    f.write(f"### {repo}\n\n")
                    f.write(f"Contains **{len(subs)}** submodule(s):\n\n")
                    for sub in subs:
                        f.write(f"- {sub}\n")
                    f.write("\n")
            
            # All repositories list
            f.write("## Complete Repository List\n\n")
            f.write("### Root Repositories\n\n")
            for repo in sorted_roots:
                sub_count = len(dependencies.get(repo, []))
                if sub_count > 0:
                    f.write(f"- **{repo}** ({sub_count} submodules)\n")
                else:
                    f.write(f"- {repo}\n")
            
            if analysis['submodules']:
                f.write("\n### Submodule Repositories\n\n")
                for repo in analysis['submodules']:
                    parent_count = len(reverse_deps.get(repo, []))
                    f.write(f"- **{repo}** (used by {parent_count} repositories)\n")
        
        print(f"📄 Markdown exported to: {filename}")
        return filename
    
    def _write_markdown_tree(self, f, repo: str, dependencies: Dict, prefix: str, visited: Set):
        """Write dependency tree in markdown format"""
        if repo in visited:
            return
        
        visited.add(repo)
        
        if repo in dependencies:
            subs = dependencies[repo]
            for i, sub in enumerate(subs):
                is_last = i == len(subs) - 1
                connector = "└──" if is_last else "├──"
                f.write(f"{prefix}{connector} {sub}<br>\n")
                
                new_prefix = prefix + ("    " if is_last else "│   ")
                self._write_markdown_tree(f, sub, dependencies, new_prefix, visited)
    
    def print_summary(self, analysis: Dict):
        """Print a concise summary of relationships"""
        print("\n" + "="*70)
        print("DEPENDENCY SUMMARY")
        print("="*70)
        
        dependencies = analysis['dependencies']
        reverse_deps = self.get_reverse_dependencies(analysis)
        
        # Most depended upon repositories
        if reverse_deps:
            print("\n📊 Most Depended Upon (used as submodules):")
            sorted_deps = sorted(reverse_deps.items(), key=lambda x: len(x[1]), reverse=True)
            for repo, parents in sorted_deps[:10]:
                print(f"   • {repo}: used by {len(parents)} repositories")
                for parent in parents:
                    print(f"      - {parent}")
        
        # Most complex repositories (most submodules)
        if dependencies:
            print("\n🔧 Most Complex (most submodules):")
            sorted_complex = sorted(dependencies.items(), key=lambda x: len(x[1]), reverse=True)
            for repo, subs in sorted_complex[:10]:
                print(f"   • {repo}: {len(subs)} submodules")


def main():
    """Main function"""
    print("GitHub Repository Dependency Analyzer")
    print("="*70)
    
    username = input("Enter GitHub username: ").strip()
    
    print("\nOptional: Enter GitHub Personal Access Token")
    print("(Press Enter to skip - only public repos will be scanned)")
    token = input("Token: ").strip() or None
    
    # Analyze relationships
    analyzer = RepoRelationshipAnalyzer(username, token)
    analysis = analyzer.analyze_relationships()
    
    # Display results
    analyzer.print_relationships(analysis)
    analyzer.print_summary(analysis)
    
    # Export to both JSON and Markdown
    analyzer.export_to_json(analysis)
    analyzer.export_to_markdown(analysis)
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()