#!/bin/bash

STATION_DIR="$(cd "$(dirname "$0")/station" && pwd)"
VIMSCRIPT_DIR="$(cd "$(dirname "$0")/vimscript" && pwd)"
VIMRC_PATH="$VIMSCRIPT_DIR/.vimrc"
VIM_COLORS_DIR="$VIMSCRIPT_DIR/color"
HOME_VIMRC="$HOME/.vimrc"
HOME_VIM_COLORS="$HOME/.vim/colors"
BASH_ALIASES_PATH="$STATION_DIR/bashrc/aliases.bash"
PKG_BASH_PATH="$STATION_DIR/bashrc/metro.bashrc"
HOME_BASH_ALIASES="$HOME/.bash_aliases"
HOME_BASHRC="$HOME/.bashrc"

echo "Installing required Python packages with pip3..."
pip3 install os sys json platform urllib3 tarfile zipfile shutil

if [ ! -f "$ORIGINAL_BASHRC" ]; then
    cp "$HOME_BASHRC" "$ORIGINAL_BASHRC"
    echo "Original .bashrc has been saved to $ORIGINAL_BASHRC."
fi

if ! grep -q "source $PKG_BASH_PATH" "$HOME_BASHRC"; then
    echo "source $PKG_BASH_PATH" >> "$HOME_BASHRC"
    echo "Contents of pkg.bash have been added to .bashrc."
else
    echo "pkg.bash is already sourced in .bashrc."
fi

if [ -f "$HOME_VIMRC" ]; then
    read -p ".vimrc already exists. Do you want to overwrite it? (y/n): " overwrite_vimrc
    if [ "$overwrite_vimrc" = "y" ]; then
        cp "$VIMRC_PATH" "$HOME_VIMRC"
        echo ".vimrc has been overwritten."
    else
        echo ".vimrc was not overwritten."
    fi
else
    cp "$VIMRC_PATH" "$HOME_VIMRC"
    echo ".vimrc has been applied."
fi

if [ ! -d "$HOME_VIM_COLORS" ]; then
    mkdir -p "$HOME_VIM_COLORS"
fi
cp "$VIM_COLORS_DIR"/*.vim "$HOME_VIM_COLORS"
echo "Vim colorschemes have been copied to ~/.vim/colors."

source ~/.bashrc
chmod +x bin/metro
echo "bin/metro has been added to the PATH and made executable."

echo "Metro has been initialized successfully. Please restart your terminal for changes to take effect."
