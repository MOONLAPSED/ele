#!/bin/bash
# rollout/re-init script for the ele to re-base its source code

source .bashrc  # Source .bashrc for environment settings
PYTHON_SCRIPT="/src/ele_source.py"

if [ "$1" = "read" ]; then
  cat < $PYTHON_SCRIPT
  exit 0
fi

if [ "$1" = "write" ]; then
  echo "$2" | $PYTHON_SCRIPT
  exit 0  
fi

# Read input 
read input

# Convert to JSON
input_json=$(json "${input}")

# Call Python script with JSON input
output_json=$(echo "$input_json" | $PYTHON_SCRIPT)

# Convert JSON output to text
output=$(json -d "$output_json")

# Print output
echo "$output"
