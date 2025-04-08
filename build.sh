#!/bin/bash

set -e  # Exit on any error

VERSION_FILE="app/app-version"

# Ensure at least one argument is provided
if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 --debug|--release [--major|--minor|--patch]"
    exit 1
fi

# Check build mode
if [[ $1 == "--debug" ]]; then
    MODE="debug"
elif [[ $1 == "--release" ]]; then
    MODE="release"
else
    echo "Invalid mode: $1"
    echo "Usage: $0 --debug|--release [--major|--minor|--patch]"
    exit 1
fi

# Optional version bump
bump_version() {
    current_version=$(cat "$VERSION_FILE")
    IFS='.' read -r major minor patch <<< "$current_version"

    case "$1" in
        --major)
            ((major++))
            minor=0
            patch=0
            ;;
        --minor)
            ((minor++))
            patch=0
            ;;
        --patch)
            ((patch++))
            ;;
        *)
            echo "Unknown version bump flag: $1" >&2
            exit 1
            ;;
    esac

    new_version="${major}.${minor}.${patch}"
    echo "$new_version" > "$VERSION_FILE"
    echo "🔧 Version bumped to $new_version"
}

if [[ $# -eq 2 ]]; then
    case "$2" in
        --major|--minor|--patch)
            bump_version "$2"
            ;;
        *)
            echo "Invalid version flag: $2"
            echo "Usage: $0 --debug|--release [--major|--minor|--patch]"
            exit 1
            ;;
    esac
fi

# Call Python updater
echo "🔄 [$MODE] Updating files with version from $VERSION_FILE..."
if python3 update_version.py; then
    echo "✅ Version update successful."
else
    echo "❌ Version update failed!" >&2
    exit 1
fi


# Ensure we are in the correct directory
TARGET_DIR="./app"
if [[ ! $(pwd) == *"$TARGET_DIR" ]]; then
    echo "Navigating to $TARGET_DIR..."
    cd "$TARGET_DIR" || { echo "Failed to navigate to $TARGET_DIR"; exit 1; }
fi

# Load environment variables
source ../.prepare-env

env | grep -i "p4a"

# Execute buildozer command
echo "Running buildozer in $MODE mode..."
buildozer -v android "$MODE"
