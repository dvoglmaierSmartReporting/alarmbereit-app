#!/bin/bash

set -e  # Exit on any error
set -u  # Treat unset variables as errors

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

# Run tests
echo "🧪 Running tests with pytest..."
pytest tests/ -v | tee build-test.log
exit_code=${PIPESTATUS[0]}

if [ "$exit_code" -eq 0 ]; then
    echo "✅ All tests passed."
else
    echo "❌ Tests failed. Aborting build!" >&2
    exit $exit_code
fi

# update iOS proxy directory

SRC_BASE="../feuerwehr_app/app"
SRC_BASE="./app"
DST_BASE="../ios_builds/feuerwehr_app_proxy/app/"

# Copy single files (overwrite with -f)
cp -f "$SRC_BASE/main.py" "$DST_BASE/"
echo "main.py updated"

cp -f "$SRC_BASE/feuerwehr.kv" "$DST_BASE/"
echo "feuerwehr.kv updated"

# Copy folders (overwrite by removing target first)
copy_dir() {
    local src="$1"
    local dst="$2"
    if [ -d "$dst" ]; then
        rm -rf "$dst"
    fi
    cp -r "$src" "$dst"
    echo "$(basename "$src") folder updated"
}

copy_dir "$SRC_BASE/assets"   "$DST_BASE/assets"
copy_dir "$SRC_BASE/content"  "$DST_BASE/content"
copy_dir "$SRC_BASE/errors"   "$DST_BASE/errors"
copy_dir "$SRC_BASE/fonts"    "$DST_BASE/fonts"
copy_dir "$SRC_BASE/helper"   "$DST_BASE/helper"
copy_dir "$SRC_BASE/screens"  "$DST_BASE/screens"
copy_dir "$SRC_BASE/storage"  "$DST_BASE/storage"

# Optional iOS icon update
IOS_DIR="fa1000-ios"
ICON_TARGET="$IOS_DIR/icon.png"
ICON_SOURCE="$SRC_BASE/assets/firetruck_icon.png"

if [ -d "$IOS_DIR" ] && [ -f "$ICON_TARGET" ]; then
    cp -f "$ICON_SOURCE" "$ICON_TARGET"
    echo "icon.png updated"
fi

echo "✅ Successfully updated iOS proxy directory."
echo ""
echo ""


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
