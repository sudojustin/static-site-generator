from parentnode import ParentNode
from leafnode import LeafNode
from helpers import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    text_to_textnodes,
    text_node_to_html_node
)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in nodes]
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            count = len(block) - len(block.lstrip('#'))
            heading_text = block.lstrip('#').strip()
            html_children = text_to_children(heading_text)
            node = ParentNode(f'h{count}', html_children)

        elif block_type == BlockType.PARAGRAPH:
            flat_text = ' '.join(line.strip() for line in block.splitlines())
            html_children = text_to_children(flat_text)
            node = ParentNode('p', html_children)

        elif block_type == BlockType.CODE:
            lines = block.splitlines()
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].startswith('```'):
                lines = lines[:-1]
            code_text = '\n'.join(lines) + '\n'
            code_node = LeafNode('code', code_text)
            node = ParentNode('pre', [code_node])

        elif block_type == BlockType.QUOTE:
            flat_text = ' '.join(line.lstrip('> ').strip() for line in block.splitlines())
            html_children = text_to_children(flat_text)
            node = ParentNode('blockquote', html_children)

        elif block_type == BlockType.UNORDERED_LIST:
            list_items = [line[2:].strip() for line in block.splitlines()]
            li_nodes = [ParentNode('li', text_to_children(item)) for item in list_items]
            node = ParentNode('ul', li_nodes)

        elif block_type == BlockType.ORDERED_LIST:
            list_items = [line.split('. ', 1)[1].strip() for line in block.splitlines()]
            li_nodes = [ParentNode('li', text_to_children(item)) for item in list_items]
            node = ParentNode('ol', li_nodes)

        else:
            flat_text = ' '.join(line.strip() for line in block.splitlines())
            html_children = text_to_children(flat_text)
            node = ParentNode('p', html_children)

        block_nodes.append(node)

    return ParentNode('div', block_nodes)

