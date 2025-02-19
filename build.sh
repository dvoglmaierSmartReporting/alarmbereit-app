#!/bin/bash

# Ensure a mandatory argument is provided
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 --debug | --release"
    exit 1
fi

# Check if the argument is valid
if [[ $1 == "--debug" ]]; then
    MODE="debug"
elif [[ $1 == "--release" ]]; then
    MODE="release"
else
    echo "Invalid argument: $1"
    echo "Usage: $0 --debug | --release"
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
