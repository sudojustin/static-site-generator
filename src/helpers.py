import re
from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag='b', value=text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag='i', value=text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag='code', value=text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag='img', value='', props={'src': text_node.url, 'alt': text_node.text})
    raise ValueError(f'{text_node.text_type} not in TextType')


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        text_remaining = node.text
        for alt_text, url in images:
            # Split text at the image markdown
            split_text = text_remaining.split(f'![{alt_text}]({url})', 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text_remaining = split_text[1]  # remaining text after the image

        if text_remaining:
            new_nodes.append(TextNode(text_remaining, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        text_remaining = node.text
        for anchor_text, url in links:
            split_text = text_remaining.split(f'[{anchor_text}]({url})', 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            text_remaining = split_text[1]

        if text_remaining:
            new_nodes.append(TextNode(text_remaining, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split('\n\n')]
    return [block for block in blocks if block]

