#!/bin/bash
# rollout/re-init script for the ele to re-base its source code

source .bashrc  # Source .bashrc for environment settings

# Argument Handling
if [ -z "$1" ]
then
    echo "No argument provided. Performing default actions..."
else
    echo "Argument passed: $1"
fi