from copy_static import copy_static  # your function from the previous step
from md_to_html_node import markdown_to_html_node  # if you want to build HTML pages
import os

def main():
    copy_static('static', 'public')

    md_file = 'content/index.md'
    if os.path.exists(md_file):
        with open(md_file, 'r', encoding='utf-8') as f:
            markdown = f.read()

        html_node = markdown_to_html_node(markdown)
        html_str = html_node.to_html()

        output_file = os.path.join('public', 'index.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_str)
        print(f'Generated {output_file}')

if __name__ == '__main__':
    main()

