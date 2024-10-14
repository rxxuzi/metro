#!/bin/bash

# 各種パスの設定
STATION_DIR="$(cd "$(dirname "$0")/station" && pwd)"
VIMSCRIPT_DIR="$(cd "$(dirname "$0")/vimscript" && pwd)"
VIMRC_PATH="$VIMSCRIPT_DIR/.vimrc"
VIM_COLORS_DIR="$VIMSCRIPT_DIR/color"
HOME_VIMRC="$HOME/.vimrc"
HOME_VIM_COLORS="$HOME/.vim/colors"
BASH_ALIASES_PATH="$STATION_DIR/bashrc/.bash_aliases"
HOME_BASH_ALIASES="$HOME/.bash_aliases"
BIN_DIR="$(cd "$(dirname "$0")/bin" && pwd)"

echo "Installing required Python packages with pip3..."
pip3 install os sys json platform urllib3 tarfile zipfile shutil

echo 'export PATH=$PATH:~/metro/bin' >> ~/.bashrc
source ~/.bashrc
chmod +x "$BIN_DIR/metro"
echo "bin/metro has been added to the PATH and made executable."

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

if [ -f "$HOME_BASH_ALIASES" ]; then
    read -p ".bash_aliases already exists. Do you want to append the new aliases? (y/n): " append_aliases
    if [ "$append_aliases" = "y" ]; then
        cat "$BASH_ALIASES_PATH" >> "$HOME_BASH_ALIASES"
        echo "New aliases have been appended to ~/.bash_aliases."
    else
        echo ".bash_aliases was not modified."
    fi
else
    cp "$BASH_ALIASES_PATH" "$HOME_BASH_ALIASES"
    echo ".bash_aliases has been applied."
fi

echo "Metro has been initialized successfully."
