#!/bin/bash
set -e

# === CONFIGURATION ===
PROFILE_DIR="$(pwd)"         # Use current directory as archiso profile
OUTPUT_DIR="$PROFILE_DIR/out"
ISO_NAME="drawkoOS-testBuild.iso"
WORK_DIR="$PROFILE_DIR/work"  # Define work directory

# === CHECK DEPENDENCIES ===
command -v mkarchiso >/dev/null 2>&1 || {
    echo >&2 "mkarchiso not found. Install it with: sudo pacman -S archiso";
    exit 1;
}

# === CREATE OUTPUT DIR ===
mkdir -p "$OUTPUT_DIR"

# === BUILD ISO ===
echo "Building ISO from profile at: $PROFILE_DIR"
sudo mkarchiso -v -o "$OUTPUT_DIR" "$PROFILE_DIR"

# === RENAME OUTPUT ISO ===
cd "$OUTPUT_DIR"
LATEST_ISO=$(ls -t drawskoOS-*.iso 2>/dev/null | head -n1)

if [ -n "$LATEST_ISO" ] && [ -f "$LATEST_ISO" ]; then
    mv "$LATEST_ISO" "$ISO_NAME"
    echo "✅ ISO renamed to: $ISO_NAME"
else
    echo "❌ Error: No drawskoOS-*.iso file found in output directory"
    exit 1
fi

# === CLEANUP WORK DIRECTORY ===
if [ -d "$WORK_DIR" ]; then
    echo "Removing work directory: $WORK_DIR"
    sudo rm -rf "$WORK_DIR"
else
    echo "Work directory $WORK_DIR does not exist (already cleaned up)"
fi

echo "✅ ISO built successfully: $OUTPUT_DIR/$ISO_NAME"
