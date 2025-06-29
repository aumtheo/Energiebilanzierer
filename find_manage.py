#!/usr/bin/env python3
import os

def find_manage_py(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if 'manage.py' in files:
            print(os.path.abspath(os.path.join(root, 'manage.py')))

if __name__ == '__main__':
    # passe den Pfad hier ggf. an, falls dein Projekt-Root anders heißt
    project_root = os.path.dirname(__file__)
    find_manage_py(project_root)