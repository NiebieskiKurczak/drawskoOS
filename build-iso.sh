#!/bin/bash
set -e

# === CONFIGURATION ===
PROFILE_DIR="$(pwd)"         # Use current directory as archiso profile
OUTPUT_DIR="$PROFILE_DIR/out"
ISO_NAME="drawkoOS-testBuild.iso"

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
LATEST_ISO=$(ls -t archlinux-*.iso | head -n1)
[ -f "$LATEST_ISO" ] && mv "$LATEST_ISO" "$ISO_NAME"

if [ -d "$work_dir" ]; then
  echo "Removing directory: $work_dir"
  rm -rf "$work_dir"
else
  echo "Directory $work_dir does not exist."
fi


echo "✅ ISO built successfully: $OUTPUT_DIR/$ISO_NAME"
