from copy_static import copy_static
from generate_pages_recursive import generate_pages_recursive
import shutil
from pathlib import Path

def main():
    public_dir = Path('public')

    # Delete everything in public
    if public_dir.exists():
        shutil.rmtree(public_dir)

    # Copy static files
    copy_static('static', 'public')

    # Generate index page
    generate_pages_recursive('content', 'template.html', 'public')

if __name__ == '__main__':
    main()

