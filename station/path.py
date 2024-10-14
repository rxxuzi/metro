#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

# Constants
BASHRC_PATH = Path.home() / '.bashrc'
BACKUP_PATH = Path.home() / '.bashrc.backup'

def backup_bashrc():
    if not BACKUP_PATH.exists():
        try:
            with BASHRC_PATH.open('r') as original, BACKUP_PATH.open('w') as backup:
                backup.write(original.read())
            print(f"Backup created at: {BACKUP_PATH}")
        except Exception as e:
            print(f"Error creating backup: {e}")
            sys.exit(1)
    else:
        print(f"Backup already exists at: {BACKUP_PATH}")

def load_bashrc():
    try:
        with BASHRC_PATH.open('r') as file:
            lines = file.readlines()
        return lines
    except Exception as e:
        print(f"Error reading {BASHRC_PATH}: {e}")
        sys.exit(1)

def save_bashrc(lines):
    try:
        with BASHRC_PATH.open('w') as file:
            file.writelines(lines)
        print(".bashrc has been updated.")
    except Exception as e:
        print(f"Error writing to {BASHRC_PATH}: {e}")
        sys.exit(1)

def get_path_entries(lines):
    for line in lines:
        if line.startswith('export PATH='):
            # Extract the PATH line
            path_line = line.strip().split('=', 1)[1].strip('"')
            paths = path_line.split(':')
            return paths
    return []

def set_path_entries(lines, paths):
    new_path = ':'.join(paths)
    new_line = f'export PATH="{new_path}"\n'
    new_lines = []
    path_set = False
    for line in lines:
        if line.startswith('export PATH='):
            new_lines.append(new_line)
            path_set = True
        else:
            new_lines.append(line)
    if not path_set:
        new_lines.append(new_line)
    return new_lines

def add_path(entry):
    backup_bashrc()
    lines = load_bashrc()
    paths = get_path_entries(lines)
    abs_entry = str((Path.cwd() / entry).resolve())
    if abs_entry in paths:
        print(f"Path already exists: {abs_entry}")
        return
    paths.append(abs_entry)
    lines = set_path_entries(lines, paths)
    save_bashrc(lines)
    print(f"Path added: {abs_entry}")
    print("Please run `reload` to apply the changes.")

def remove_path(entry):
    backup_bashrc()
    lines = load_bashrc()
    paths = get_path_entries(lines)
    abs_entry = str((Path.cwd() / entry).resolve())
    if abs_entry not in paths:
        print(f"Path not found: {abs_entry}")
        return
    paths.remove(abs_entry)
    lines = set_path_entries(lines, paths)
    save_bashrc(lines)
    print(f"Path removed: {abs_entry}")
    print("Please run `source ~/.bashrc` to apply the changes.")

def list_paths():
    lines = load_bashrc()
    paths = get_path_entries(lines)
    if not paths:
        print("No paths found in PATH.")
        return
    print("PATH Entries:")
    for idx, path in enumerate(paths, start=1):
        print(f"{idx}. {path}")

def show_help():
    help_text = """
Usage:
    metro path -a <path>      Add a new path to .bashrc
    metro path -r <path>      Remove a path from .bashrc
    metro path -l             List all paths in .bashrc
    metro path -h             Show this help message

Examples:
    metro path -a .
    metro path -a bin/
    metro path -r .
    metro path -l
"""
    print(help_text)

def main():
    parser = argparse.ArgumentParser(description='Manage PATH in .bashrc', add_help=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', metavar='<path>', help='Add a new path to .bashrc')
    group.add_argument('-r', '--remove', metavar='<path>', help='Remove a path from .bashrc')
    group.add_argument('-l', '--list', action='store_true', help='List all paths in .bashrc')
    group.add_argument('-h', '--help', action='store_true', help='Show help message')

    args = parser.parse_args()

    if args.add:
        add_path(args.add)
    elif args.remove:
        remove_path(args.remove)
    elif args.list:
        list_paths()
    elif args.help or len(sys.argv) == 1:
        show_help()
    else:
        print("Invalid option.")
        show_help()

if __name__ == '__main__':
    main()
