from pathlib import Path
from extract_title import extract_title
from md_to_html_node import markdown_to_html_node

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    # Read markdown
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_content = markdown_to_html_node(markdown_content).to_html()

    # Extract title
    title = extract_title(markdown_content)

    # Replace placeholders
    full_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    # Ensure destination directory exists
    dest_dir = Path(dest_path).parent
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Write output
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

