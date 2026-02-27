# GIT
## some basic concepts
* HEAD is simply a pointer that tells Git “where you currently are” in the repository.
* In most cases, HEAD points to a branch name rather than directly to a commit
* Git resolves your current commit by following pointers: HEAD → main → commit → tree → files
* Sometimes HEAD points directly to a commit hash instead of a branch name. This is called detached HEAD state. It happens when you checkout a specific commit by its hash or checkout a tag.
* 2 types of merging
    1. Fast-Forward Merge: The Simple Case
    2. Three-Way Merge: When Branches Diverge
* merge commits can clutter the history to avoid that use rebase
* rebase actually append the feature branch to the main branch, by rewriting the updated commit history by adding the changes of main branch made after making feature branch or in simple words It replays (re-creates) your feature branch commits on top of main, rewriting history.
* a branch is just a pointer to a commit.
git rebase main # Replays your feature branch commits on top of main.
* github only takes .git repo from local machine not the the working directory

## basics
* git init
* git clone <repo_url>
* git add .
* git commit -m"hello"
* git commit -m"hi" --allow-empty
* git status
* git log
* git log --oneline
---
## remote
* git remote add origin <repo_url> 
* git remote remove origin
* git remote -v #it just check weather the remote details are there in local git repo
* git push origin main
* git push origin main --force
* git pull origin main
* git pull
* git push
---
## branch
* git branch -M main :set default branch name as main
* git branch :list all branches
* git branch <branch_name> :create new branch
* git branch <branch_name> <commit_hash> :create new branch from specific commit
* git checkout <branch_name> :switch to another branch
* git merge <branch_name> :merge specific branch to current branch
# we can also merge the branches in the pull request process on github
# it is good practice to delete branches after merging, because they are still pointing the the last commit of that branch not merge commit
* git branch -d <branch_name> :delete branch locally
* delete remote branch from github ui
* then remove the cached origin/feature branch by running git fetch --prune

---
## version_control
* git reset <file_name> :unstage added file
* git reset --soft <commit_hash> :move head to specific commit keeping changes staged
* git reset --hard <commit_hash> :move the head to specific commit by discarding all changes
* git revert <commit_hash> :create new commit to undo a specific commit
---
## auth with github
* git internally uses gh cli for managing authorization credential
* gh auth login
* gh auth status
* gh auth switch
---
## deleting commits (git reset)
* if it is local (not pushed) use: ```git reset --soft HEAD~1``` # it undo last 1 commit and make changes staged (use ```--hard``` if you want to permanently delete last commit without staging)
* if it is pushed to remote use above command to change it locally first, then use: ```git push origin main --force```
# it won't work to delete first commit, for that reinitialize whole repo
---
## reverting commits{commit reset with history} (git revert)
* git revert <commit hash> # it create a commit that removes all the changes made by this commit only by keeping all other later commits intact, Attention it may introduce conflicts if the changes in that commit is modified in later commits, so try to use it in only the most recent commit
---
## making .git lighter
* git gc # garbage collection, it delete all the objects in .git/ that are no longer referenced by git history
