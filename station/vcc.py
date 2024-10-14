import os
import shutil
import platform
import sys

def get_vim_colors_dir():
    system = platform.system()
    
    if system == "Windows":
        return os.path.expanduser('~/vimfiles/colors')
    elif system == "Linux" or system == "Darwin":
        return os.path.expanduser('~/.vim/colors')
    else:
        return None

def get_metro_colors_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../vimscript/color'))

def get_colorschemes(vim_colors_dir):
    schemes = []
    if not os.path.exists(vim_colors_dir):
        print(f"Directory {vim_colors_dir} not found.")
        return schemes

    for file in os.listdir(vim_colors_dir):
        if file.endswith(".vim"):
            schemes.append(file.replace(".vim", ""))
    return schemes

def set_colorscheme(scheme_name, vimrc_path):
    with open(vimrc_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(vimrc_path, 'w', encoding='utf-8') as f:
        found = False
        for line in lines:
            if line.strip().startswith('colorscheme'):
                f.write(f'colorscheme {scheme_name}\n')
                found = True
            else:
                f.write(line)
        if not found:
            f.write(f'\ncolorscheme {scheme_name}\n')

def select_colorscheme(schemes):
    print("Select a colorscheme:")
    for i, scheme in enumerate(schemes):
        print(f"{i + 1}: {scheme}")
    choice = int(input("\nEnter the number of your choice: ")) - 1
    if 0 <= choice < len(schemes):
        return schemes[choice]
    else:
        print("Invalid choice!")
        return None

def move_default_colors_if_needed(vim_colors_dir, metro_colors_dir):
    if not os.path.exists(vim_colors_dir):
        os.makedirs(vim_colors_dir)
    if not os.listdir(vim_colors_dir):
        print(f"No colorschemes found in {vim_colors_dir}. Moving default color schemes from {metro_colors_dir}.")
        for file in os.listdir(metro_colors_dir):
            if file.endswith(".vim"):
                shutil.copy(os.path.join(metro_colors_dir, file), vim_colors_dir)
        print(f"Default color schemes moved to {vim_colors_dir}.")

def show_help():
    print("Usage:")
    print("  metro vcc               - Change Vim color scheme")
    print("  metro vcc -h            - Show this help message")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        show_help()
        return

    vim_colors_dir = get_vim_colors_dir()
    metro_colors_dir = get_metro_colors_dir()
    
    if vim_colors_dir is None:
        print("Unsupported platform.")
        return

    vimrc_path = os.path.expanduser('~/.vimrc')
    move_default_colors_if_needed(vim_colors_dir, metro_colors_dir)

    schemes = get_colorschemes(vim_colors_dir)
    if not schemes:
        print(f"No colorschemes found in {vim_colors_dir}.")
        return

    selected_scheme = select_colorscheme(schemes)
    if selected_scheme:
        set_colorscheme(selected_scheme, vimrc_path)
        print(f"Colorscheme set to: {selected_scheme}")

if __name__ == "__main__":
    main()
