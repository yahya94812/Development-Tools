# Git Reference Notes

---

## Core Concepts

**HEAD** is a pointer that tells Git where you currently are in the repository. In most cases, HEAD points to a branch name rather than directly to a commit, and Git resolves your current position by following the chain: `HEAD → main → commit → tree → files`.

When HEAD points directly to a commit hash instead of a branch name, this is called **detached HEAD state**. It happens when you checkout a specific commit by its hash or checkout a tag.

A **branch** is simply a pointer to a commit.

---

## Merging

There are two types of merges:

**1. Fast-Forward Merge** — The simple case, used when no divergence exists between branches.

**2. Three-Way Merge** — Used when branches have diverged. Merge commits can clutter history; use rebase to avoid this.

---

## Rebasing

Rebase replays (re-creates) your feature branch commits on top of another branch, rewriting commit history. In effect, it appends the feature branch to main by incorporating all changes made to main after the feature branch was created.

```bash
git rebase main   # Replays your feature branch commits on top of main
```

> **Note:** GitHub only takes the `.git` repo from your local machine, not the working directory.

---

## Basics

```bash
git init
git clone <repo_url>
git add .
git commit -m "message"
git commit -m "message" --allow-empty
git status
git log
git log --oneline
```

---

## Remote

```bash
git remote add origin <repo_url>   # Add a remote
git remote remove origin           # Remove a remote
git remote -v                      # Check remote details stored in local repo

git push origin main               # Push to remote
git push origin main --force       # Force push
git pull origin main               # Pull from remote
git pull                           # Pull (default remote/branch)
git push                           # Push (default remote/branch)
```

---

## Branches

```bash
git branch -M main                          # Set default branch name to main
git branch                                  # List all branches
git branch <branch_name>                    # Create new branch
git branch <branch_name> <commit_hash>      # Create new branch from specific commit
git checkout <branch_name>                  # Switch to a branch
git merge <branch_name>                     # Merge a branch into current branch
git branch -d <branch_name>                 # Delete branch locally
git fetch --prune                           # Remove cached remote-tracking branches (e.g. origin/feature)
```

> You can also merge branches via a Pull Request on GitHub. It is good practice to delete branches after merging — they still point to their last commit, not the merge commit. Delete remote branches from the GitHub UI, then run `git fetch --prune` to clean up locally.

---

## Version Control

```bash
git reset <file_name>              # Unstage a staged file
git reset --soft <commit_hash>     # Move HEAD to a commit, keeping changes staged
git reset --hard <commit_hash>     # Move HEAD to a commit, discarding all changes
git revert <commit_hash>           # Create a new commit that undoes a specific commit
```

---

## Authentication with GitHub

Git internally uses the GitHub CLI (`gh`) for managing authorization credentials.

```bash
gh auth login
gh auth status
gh auth switch
```

---

## Deleting Commits (`git reset`)

**If the commit is local (not pushed yet):**
```bash
git reset --soft HEAD~1    # Undo last commit, keep changes staged
git reset --hard HEAD~1    # Permanently delete last commit and discard changes
```

**If the commit has already been pushed:**
```bash
# First, reset locally using one of the commands above, then force push:
git push origin main --force
```

> Note: Resetting the very first commit won't work this way — you'll need to reinitialize the entire repo.

---

## Reverting Commits (`git revert`)

```bash
git revert <commit_hash>
```

Creates a new commit that removes all changes introduced by the specified commit, while keeping all later commits intact. This is safe for shared/public history.

> **Caution:** May introduce conflicts if the reverted changes were modified by later commits. Best used on the most recent commit.

---

## Maintenance

```bash
git gc    # Garbage collection — deletes unreferenced objects in .git/ to reduce repo size
```