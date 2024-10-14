#!/bin/bash

PROMPT_ALTERNATIVES=("twoline" "oneline" "backtrack" "minimal" "classic")
PKG_BASH_PATH="$HOME/metro/station/bashrc/metro.bashrc"

function set_prompt() {
    local choice=$1
    if [[ $choice -lt 0 || $choice -ge ${#PROMPT_ALTERNATIVES[@]} ]]; then
        echo "Invalid choice. Please select a number between 0 and $((${#PROMPT_ALTERNATIVES[@]} - 1))."
        exit 1
    fi
    local selected_prompt="${PROMPT_ALTERNATIVES[$choice]}"
    if grep -q "PROMPT_ALTERNATIVE=" "$PKG_BASH_PATH"; then
        sed -i "s/PROMPT_ALTERNATIVE=.*/PROMPT_ALTERNATIVE=$selected_prompt/" "$PKG_BASH_PATH"
    else
        echo "PROMPT_ALTERNATIVE=$selected_prompt" >> "$PKG_BASH_PATH"
    fi

    echo "Prompt style set to $selected_prompt in pkg.bash. Please run 'source ~/.bashrc' to apply the changes."
}

function show_help() {
    echo "Usage: metro prompt set <0-4>"
    echo "Options:"
    echo "  0: twoline   - Default two-line prompt"
    echo "  1: oneline   - Single-line prompt"
    echo "  2: backtrack - Backtrack-style prompt"
    echo "  3: minimal   - Minimalist prompt"
    echo "  4: classic   - Classic-style prompt"
}

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

if [ "$#" -ne 2 ] || [ "$1" != "set" ]; then
    show_help
    exit 1
fi

set_prompt $2
