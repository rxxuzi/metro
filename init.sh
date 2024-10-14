#!/bin/bash

STATION_DIR="$(cd "$(dirname "$0")/station" && pwd)"
VIMSCRIPT_DIR="$(cd "$(dirname "$0")/vimscript" && pwd)"
VIMRC_PATH="$VIMSCRIPT_DIR/.vimrc"
VIM_COLORS_DIR="$VIMSCRIPT_DIR/color"
HOME_VIMRC="$HOME/.vimrc"
HOME_VIM_COLORS="$HOME/.vim/colors"
BASH_ALIASES_PATH="$STATION_DIR/bashrc/.bash_aliases"
PKG_BASH_PATH="$STATION_DIR/bashrc/pkg.bash"
HOME_BASH_ALIASES="$HOME/.bash_aliases"
HOME_BASHRC="$HOME/.bashrc"
ORIGINAL_BASHRC="$HOME/origin.bashrc"

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

# bin/metro を PATH に追加
echo 'export PATH="$PATH:~/metro/bin"' >> ~/.bashrc
source ~/.bashrc
chmod +x bin/metro
echo "bin/metro has been added to the PATH and made executable."

# 最終メッセージ
echo "Metro has been initialized successfully. Please restart your terminal for changes to take effect."
