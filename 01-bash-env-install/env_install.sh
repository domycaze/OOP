#!/usr/bin/env bash
# =============================================================================
# env_install.sh - set up a Python / Jupyter development environment
#
# Usage:
#   ./env_install.sh              normal run
#   ./env_install.sh --dry-run    show what would be done, change nothing
#   ./env_install.sh --verbose    print every command before it runs
#   ./env_install.sh --quiet      only print warnings and errors
#   ./env_install.sh --uninstall  remove what this script installed (Jupyter)
#
# Every action is also written to env_install.log (timestamp, command, status).
# =============================================================================

# Strict mode (bonus): stop on errors, unset variables and failed pipes
set -euo pipefail

LOG_FILE="$(dirname "$0")/env_install.log"
DRY_RUN=false
VERBOSE=false
QUIET=false
UNINSTALL=false

# --- Colours (bonus) ---------------------------------------------------------
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

# --- Functions ---------------------------------------------------------------

# Feature 1: pretty printing. Blank line before and after, printf for portability.
# $1 = message, $2 = level (info | success | warn | error), default info
pretty_print() {
    local message="$1"
    local level="${2:-info}"
    local colour="$RESET"

    case "$level" in
        success) colour="$GREEN" ;;
        warn)    colour="$YELLOW" ;;
        error)   colour="$RED" ;;
    esac

    # In quiet mode only warnings and errors are shown
    if [[ "$QUIET" == true && "$level" != "warn" && "$level" != "error" ]]; then
        return 0
    fi

    printf "\n%b%s%b\n\n" "$colour" "$message" "$RESET"
}

# Write one line to the log file: timestamp | status | message
log() {
    printf "%s | %s | %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2" >> "$LOG_FILE"
}

# Run a command with logging, dry-run and verbose support.
# Returns the command's exit code so the caller can react to failures.
run() {
    local cmd="$*"
    if [[ "$VERBOSE" == true ]]; then
        printf "+ %s\n" "$cmd"
    fi
    if [[ "$DRY_RUN" == true ]]; then
        printf "[dry-run] %s\n" "$cmd"
        log "DRY-RUN" "$cmd"
        return 0
    fi
    if "$@"; then
        log "OK" "$cmd"
        return 0
    else
        local code=$?
        log "FAIL($code)" "$cmd"
        return "$code"
    fi
}

# Feature 2: operating system detection with $OSTYPE
detect_os() {
    case "${OSTYPE:-unknown}" in
        darwin*)            OS="macos" ;;
        linux-gnu*|linux*)  OS="linux" ;;
        msys*|cygwin*)      OS="windows" ;;
        *)                  OS="unknown" ;;
    esac
}

# Install a package with the right package manager for this OS
install_package() {
    local package="$1"
    case "$OS" in
        macos)
            if ! command -v brew >/dev/null 2>&1; then
                pretty_print "Homebrew is not installed. Install it from https://brew.sh first." error
                return 1
            fi
            run brew install "$package"
            ;;
        linux)
            run sudo apt-get update
            run sudo apt-get install -y "$package"
            ;;
        *)
            pretty_print "Unsupported OS ($OSTYPE): install $package manually." error
            return 1
            ;;
    esac
}

# Feature 3: install python3 if missing, otherwise show its version
check_python() {
    if command -v python3 >/dev/null 2>&1; then
        pretty_print "Python is installed: $(python3 --version 2>&1)" success
    else
        pretty_print "python3 not found, installing it..." warn
        if [[ "$OS" == "macos" ]]; then
            install_package python
        else
            install_package python3
        fi
    fi
}

# Feature 4: make sure pip is available and show its version
check_pip() {
    if python3 -m pip --version >/dev/null 2>&1; then
        pretty_print "pip is installed: $(python3 -m pip --version)" success
    else
        pretty_print "pip not found, installing it..." warn
        if [[ "$OS" == "linux" ]]; then
            install_package python3-pip
        else
            run python3 -m ensurepip --upgrade
        fi
    fi
}

# Feature 5: install Jupyter Notebook (command differs by OS)
install_jupyter() {
    if command -v jupyter >/dev/null 2>&1; then
        pretty_print "Jupyter is already installed: $(jupyter --version 2>/dev/null | head -n 1)" success
        return 0
    fi
    pretty_print "Installing Jupyter Notebook..."
    case "$OS" in
        macos) run brew install jupyterlab ;;
        linux) run python3 -m pip install --user notebook ;;
        *)     run python3 -m pip install notebook ;;
    esac
}

# Feature 6: macOS only - check Homebrew is healthy
brew_health_check() {
    if [[ "$OS" == "macos" ]] && command -v brew >/dev/null 2>&1; then
        pretty_print "Running brew doctor..."
        # brew doctor exits non-zero for warnings, which should not stop the script
        run brew doctor || pretty_print "brew doctor reported warnings (see above)." warn
    fi
}

# Bonus: undo what the script installed
uninstall() {
    pretty_print "Uninstalling Jupyter..." warn
    case "$OS" in
        macos) run brew uninstall jupyterlab || true ;;
        *)     run python3 -m pip uninstall -y notebook || true ;;
    esac
    pretty_print "Uninstall finished. Python itself was left in place." success
}

parse_args() {
    for arg in "$@"; do
        case "$arg" in
            --dry-run)   DRY_RUN=true ;;
            --verbose)   VERBOSE=true ;;
            --quiet)     QUIET=true ;;
            --uninstall) UNINSTALL=true ;;
            -h|--help)
                sed -n '3,12p' "$0"
                exit 0
                ;;
            *)
                pretty_print "Unknown option: $arg (use --help)" error
                exit 1
                ;;
        esac
    done
}

# --- Main logic --------------------------------------------------------------
main() {
    parse_args "$@"
    detect_os
    log "START" "env_install.sh $* (OS=$OS)"
    pretty_print "Starting environment setup on: $OS"

    if [[ "$UNINSTALL" == true ]]; then
        uninstall
        exit 0
    fi

    check_python
    check_pip
    install_jupyter
    brew_health_check

    pretty_print "Environment ready! Launch Jupyter with: jupyter notebook" success
    log "END" "success"
}

main "$@"
