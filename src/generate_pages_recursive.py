import os
from pathlib import Path
from generate_page import generate_page

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = '/'):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                md_path = os.path.join(root, file)
                relative_path = os.path.relpath(md_path, dir_path_content)
                html_filename = os.path.splitext(relative_path)[0] + '.html'
                dest_path = os.path.join(dest_dir_path, html_filename)
                generate_page(md_path, template_path, dest_path, basepath)

