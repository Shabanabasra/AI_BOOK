#!/bin/bash

# Default values
STAGE="misc"
TITLE=""
AGENT_MODEL="agent" # As per requirements, agent and model should be 'agent'

# Function to slugify a string
slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-zA-Z0-9.]+/-/g' | sed -E 's/^-+|-+$//g'
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --title)
            TITLE="$2"
            shift
            ;;
        --stage)
            STAGE="$2"
            shift
            ;;
        *)
            echo "Unknown parameter passed: $1"
            echo "Usage: $0 --title "Your Prompt Title" [--stage <stage_name>]"
            exit 1
            ;;
    esac
    shift
done

# Validate required arguments
if [ -z "$TITLE" ]; then
    echo "Error: --title argument is required."
    echo "Usage: $0 --title "Your Prompt Title" [--stage <stage_name>]"
    exit 1
fi

SLUGIFIED_TITLE=$(slugify "$TITLE")
DATE_YMD=$(date +%Y%m%d)
TIMESTAMP=$(date +%s)
CURRENT_DATETIME=$(date +"%Y-%m-%d %H:%M:%S")

# Construct file path
OUTPUT_DIR="history/prompts/$STAGE"
FILE_NAME="${DATE_YMD}-${TIMESTAMP}-${SLUGIFIED_TITLE}.${STAGE}.prompt.md"
FULL_PATH="${OUTPUT_DIR}/${FILE_NAME}"

# Create directory if it doesn't exist
mkdir -p "$OUTPUT_DIR" || { echo "Error: Failed to create directory $OUTPUT_DIR"; exit 1; }

# Write the YAML frontmatter and markdown content to the file
cat <<EOF > "$FULL_PATH"
---
agent: $AGENT_MODEL
model: $AGENT_MODEL
name: "$SLUGIFIED_TITLE"
description: "Prompt for $TITLE"
tools: []
argument-hint: "Use this prompt for $TITLE"
---

## PHR Metadata
- **Title**: $TITLE
- **Stage**: $STAGE
- **Date**: $CURRENT_DATETIME
EOF

echo "PHR file created at: $FULL_PATH"
chmod +x "$FULL_PATH" # Make the file executable, though not strictly necessary for a markdown file.
