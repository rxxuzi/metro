import os
import sys
import json
import platform
import urllib.request
import tarfile
import zipfile
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = os.path.join(BASE_DIR, '../bin')
DB_FILE = os.path.join(BASE_DIR, 'database/app.db.json')

def show_help():
    print("Usage:")
    print("  metro install --list             - List all available apps")
    print("  metro install <app_name>         - Install app to metro/bin")
    print("  metro install -r <app_name>      - Remove app from metro/bin")
    print("  metro install --help,-h          - Show this help message")

def list_apps():
    with open(DB_FILE, 'r') as f:
        apps = json.load(f)
        print("Available apps:")
        for app in apps:
            print(f"  {app}")

def install_app(app_name):
    with open(DB_FILE, 'r') as f:
        apps = json.load(f)
    
    if app_name not in apps:
        print(f"Error: {app_name} is not available.")
        return

    arch = platform.machine()
    if arch == 'x86_64':
        arch = 'amd64'
    elif arch == 'i686' or arch == 'i386':
        arch = 'i686'
    else:
        print(f"Error: Unsupported architecture {arch}.")
        return

    app_info = apps.get(app_name)
    url = app_info.get(arch)

    if not url:
        print(f"Error: {app_name} is not available for {arch}.")
        return

    file_name = url.split('/')[-1]
    file_path = os.path.join(BIN_DIR, file_name)

    if os.path.exists(file_path):
        print(f"{file_name} already exists. Removing the old file.")
        os.remove(file_path)

    print(f"Downloading {app_name} from {url}...")
    urllib.request.urlretrieve(url, file_path)
    print(f"Downloaded {app_name} to {file_path}.")

    if file_name.endswith(".tar.xz") or file_name.endswith(".tgz") or file_name.endswith(".tar.gz"):
        with tarfile.open(file_path) as tar:
            tar.extractall(BIN_DIR)
    elif file_name.endswith(".zip"):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(BIN_DIR)

    for root, dirs, files in os.walk(BIN_DIR):
        for file in files:
            if os.access(os.path.join(root, file), os.X_OK):
                shutil.move(os.path.join(root, file), BIN_DIR)

    os.remove(file_path)
    print(f"{app_name} has been installed to {BIN_DIR}.")

def remove_app(app_name):
    app_path = os.path.join(BIN_DIR, app_name)
    if os.path.exists(app_path):
        if os.path.isdir(app_path):
            shutil.rmtree(app_path)
        else:
            os.remove(app_path)
        print(f"{app_name} has been removed from {BIN_DIR}.")
    else:
        print(f"Error: {app_name} is not installed.")

if len(sys.argv) < 2:
    show_help()
else:
    command = sys.argv[1]
    if command == '--list':
        list_apps()
    elif command == '--help' or command == '-h':
        show_help()
    elif command == '-r' and len(sys.argv) == 3:
        remove_app(sys.argv[2])
    elif len(sys.argv) == 2:
        install_app(sys.argv[1])
    else:
        show_help()
