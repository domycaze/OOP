# Exercise 1 - Bash: configure a development environment (slide 18)

Statement: https://courses.dallard.tech/linux/bash_exo/

## Part 1 - Shell experience

| Task | Command |
|---|---|
| Show my default shell | `echo $0` (running shell) / `dscl . -read ~/ UserShell` on macOS |
| Login shell from the env var | `echo $SHELL` → `/bin/zsh` on my Mac |
| Install Oh My Zsh (zsh users) | `sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"` |
| Install Oh My Bash (bash users) | `bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"` |
| Choose a theme | edit `ZSH_THEME="agnoster"` in `~/.zshrc` |
| Enable the git plugin | in `~/.zshrc`: `plugins=(git)` |
| Reload the config | `source ~/.zshrc` |
| Test the alias | `gst` (= `git status`), also `glog`, `gp` (push), `gl` (pull) |

**What is the purpose of `source`?**
`source file` runs the file *inside the current shell* instead of starting a new
child shell. So variables, aliases and functions it defines (like the new theme,
plugins and git aliases in `~/.zshrc`) take effect immediately in the terminal I am
using, without closing and reopening it.

**Shell vs terminal:** the terminal is the window/app that shows text; the shell
(bash, zsh) is the program running inside it that reads and executes commands.
**Environment variables** are named values (`$HOME`, `$PATH`, `$SHELL`, `$OSTYPE`)
inherited by every program started from the shell. A **script** is a text file of
shell commands run top to bottom. A **package manager** (brew, apt, pip) installs
and updates software and its dependencies.

## Part 2 - Python check

```bash
python3 --version   # Python 3.x.y
```

## Part 3 - The script: [`env_install.sh`](env_install.sh)

```bash
touch env_install.sh
chmod +x env_install.sh   # make it executable
```

Structure: shebang → function definitions → main logic with conditional branches.

| Required feature | Function in the script |
|---|---|
| 1. Pretty printing (blank lines, `printf`) | `pretty_print` |
| 2. OS detection with `$OSTYPE` | `detect_os` |
| 3. Install python3 if missing, else show version | `check_python` |
| 4. pip version check | `check_pip` |
| 5. Jupyter Notebook install (per OS) | `install_jupyter` |
| 6. `brew doctor` on macOS | `brew_health_check` |

Best practices used: comments explaining *why*, every variable quoted, errors
handled (`run` checks each command's exit code and logs it).

### Bonus challenges (all done)

- **Colours** - green success, yellow warnings, red errors (ANSI codes in `pretty_print`)
- **Logging** - `env_install.log` gets timestamp, command, OK/FAIL status
- **Strict mode** - `set -euo pipefail`
- **Arguments** - `--dry-run`, `--verbose`, `--quiet`, `--help`
- **Uninstall** - `--uninstall` removes Jupyter

## Part 4 - Run and verify

```bash
./env_install.sh --dry-run   # preview
./env_install.sh             # real run
```

- [x] Prompt shows the Oh My Zsh theme
- [x] `gst` works like `git status`
- [x] `python3 --version` → 3.x
- [x] `python3 -m pip --version` shows pip
- [x] `jupyter notebook` launches
- [x] `brew doctor` → "Your system is ready to brew."
