# Exercise 2 - Your first Git workflow (slide 26)

Statement: https://gist.github.com/bdallard/8bdbdd70f234f94823c0c2cde9515388

## Part 1 - Setup and configuration

```bash
git --version                                   # check Git is installed (brew install git if not)
git config --global user.name "Domitille Caze"
git config --global user.email "domycaze@gmail.com"
```

## Part 2 - Create the first repository

```bash
mkdir my-first-repo
cd my-first-repo
git init
touch readme.txt
```

## Part 3 - First commit

```bash
git status                       # readme.txt is listed as untracked
git add readme.txt
git commit -m "Add readme file"
git log
```

## Part 4 - Make changes

```bash
echo "This is my first Git repository" >> readme.txt
git status
```

`git status` now shows `readme.txt` under **"Changes not staged for commit"** as
*modified*: Git knows the file (it is tracked) and sees it differs from the last
commit, but the change is not staged yet.

```bash
git add readme.txt
git commit -m "Describe the repository in readme"
```

I now have **2 commits**.

## Part 5 - Exploration

- `git diff` shows line-by-line what changed between the working directory and the
  staging area (lines starting with `+` were added, `-` removed). With nothing
  modified it prints nothing.
- `git log --oneline` shows the history with one commit per line: the short hash
  and the message, newest first.

## Part 6 - Branches

```bash
git branch                    # list branches (* marks the current one)
git branch feature-script     # create a branch
git switch feature-script     # switch to it (or: git checkout feature-script)
git switch -c dev             # create AND switch in one command (or: git checkout -b dev)
git switch feature-script     # back to feature-script
git branch                    # verify: * feature-script
```

## Part 7 - Bash script on a branch

```bash
git branch                    # confirm * feature-script
touch install.sh
```

[`install.sh`](install.sh):

```bash
#!/bin/bash
echo "Starting installation..."
sudo apt-get update
sudo apt-get install -y tree
echo "Installation complete!"
```

```bash
chmod +x install.sh
git add install.sh
git commit -m "Add install script"
git log --oneline             # the new commit is on top of the 2 from main
```

## Part 8 - Merging

```bash
git switch main
ls                            # install.sh is NOT there
```

`install.sh` is missing because it was only committed on `feature-script`. Each
branch has its own history, and `main` does not contain that commit yet.

```bash
git merge feature-script
ls                            # install.sh is now there
git log --oneline             # "Add install script" is now in main's history
```

Because `main` had no new commits of its own, Git did a **fast-forward** merge: it
just moved the `main` pointer forward to the commit of `feature-script`, so the
history is a straight line with no merge commit.

```bash
git branch -d feature-script  # delete the merged branch
```

## Part 9 - Push to GitHub

On github.com: **New repository** → name `my-first-repo` → do **not** tick "Add a README".

```bash
git remote add origin https://github.com/domycaze/my-first-repo.git
git branch -M main
git push -u origin main
```

After refreshing, GitHub shows `readme.txt`, `install.sh`, the commit count and
the latest commit message, the same history as my local repo.

## Part 10 - Delete and clone

```bash
cd ..
rm -rf my-first-repo
git clone https://github.com/domycaze/my-first-repo.git
cd my-first-repo
ls                            # readme.txt  install.sh - everything is back
```

## Part 11 - Full workflow from scratch

```bash
cd ..
rm -rf my-first-repo                    # 1. delete local folder
# 2. GitHub → my-first-repo → Settings → Delete this repository

mkdir bash-installer && cd bash-installer   # 3.
git init                                    # 4.
echo "# bash-installer"  > README.md        # 5. README on main
echo "Script that installs the tools I need for development." >> README.md
git add README.md
git commit -m "Add project README"          # 6.

git switch -c feature-install               # 7.
cp ../install.sh .                          # 8. add the script from earlier
chmod +x install.sh
git add install.sh
git commit -m "Add installation script"     # 9.

git switch main                             # 10.
git merge feature-install                   # 11.
git branch -d feature-install               # 12.

# 13. create an empty repo "bash-installer" on GitHub
git remote add origin https://github.com/domycaze/bash-installer.git
git push -u origin main                     # 14.
```

## Reflection questions

1. **Why is version control useful?** It keeps the full history of a project, so
   I can see who changed what and why, go back to any earlier version if something
   breaks, and work with other people on the same code without overwriting each
   other.
2. **Staging vs committing?** Staging (`git add`) chooses which changes go into the
   next snapshot. Committing (`git commit`) actually saves that snapshot
   permanently in the history with a message. Staging lets me commit only part of
   my changes.
3. **When should you commit?** Each time a small, logical piece of work is done and
   working (a feature, a bug fix, a refactor). Small, frequent commits are easier
   to understand and to undo.
4. **`git init` vs `git clone`?** `git init` creates a new, empty repository in the
   current folder. `git clone` copies an existing remote repository (all files and
   history) and sets `origin` automatically.
5. **Why good commit messages?** The history becomes readable: anyone (including
   future me) can understand why a change was made without reading the code, and
   find the commit that introduced a bug.
6. **What are branches for?** They let me develop a feature or test an idea in
   isolation, without touching the stable code on `main`, then merge it when it is
   ready.
7. **When to branch instead of working on main?** For any new feature, experiment
   or bug fix that is not finished yet, and always when working in a team, so
   `main` stays working and deployable.
