#!/bin/bash

# Change to the script's directory
cd "$(dirname "$0")"

# Use absolute path for DOWNLOAD_DIR
DOWNLOAD_DIR="$(pwd)/../data"
URL="https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE243275&format=file"
NEW_FILENAME="sc_data.tar"
EXTRACT_DIR="$DOWNLOAD_DIR/extracted"
mkdir -p "$EXTRACT_DIR"
NEW_FOLDERNAME="SC_DATA"

# Download the file and rename it
wget -nc -O "$DOWNLOAD_DIR/$NEW_FILENAME" "$URL"

# Unzip and rename the file
tar -xvf "$DOWNLOAD_DIR/$NEW_FILENAME" -C "$EXTRACT_DIR"

# Delete files containing "loupe"
find "$EXTRACT_DIR" -type f -iname "*loupe*" -delete

# Create the final destination directory
mkdir -p "$DOWNLOAD_DIR/$NEW_FOLDERNAME"

# Move remaining files to the final destination
find "$EXTRACT_DIR" -type f -print0 | xargs -0 -I {} mv {} "$DOWNLOAD_DIR/$NEW_FOLDERNAME/"

# Clean up the temporary extraction directory
rm -rf "$EXTRACT_DIR"

cd "$DOWNLOAD_DIR/$NEW_FOLDERNAME"

echo $PWD
tar -xzvf GSM7782699_spatial.tar.gz
