from copy_static import copy_static
from generate_pages_recursive import generate_pages_recursive
import shutil
from pathlib import Path
import sys

def main():
    # Grab basepath from CLI argument, default to '/'
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'

    docs_dir = Path('docs')

    # Delete old docs directory
    if docs_dir.exists():
        shutil.rmtree(docs_dir)

    # Copy static files
    copy_static('static', 'docs')

    # Generate all pages recursively
    generate_pages_recursive('content', 'template.html', 'docs', basepath)

if __name__ == '__main__':
    main()

