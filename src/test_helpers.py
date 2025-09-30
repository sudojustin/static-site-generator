import unittest
from textnode import TextNode, TextType
from helpers import (BlockType, block_to_block_type, extract_markdown_images, extract_markdown_links, markdown_to_blocks, 
    split_nodes_delimiter, split_nodes_image, split_nodes_link, 
    text_node_to_html_node, split_nodes_image, split_nodes_link, text_to_textnodes)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode('This is a text node', TextType.TEXT)
        html_node = text_node_to_html_node(node)
        assert html_node is not None
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, 'This is a text node')

    def test_text_node(self):
        node = TextNode('Hello', TextType.TEXT)
        html_node = text_node_to_html_node(node)
        assert html_node is not None
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, 'Hello')
        self.assertIsNone(html_node.children)

    def test_bold_node(self):
        node = TextNode('Bold text', TextType.BOLD)
        html_node = text_node_to_html_node(node)
        assert html_node is not None
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'Bold text')

    def test_italic_node(self):
        node = TextNode('Italic text', TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        assert html_node is not None
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'Italic text')

    def test_code_node(self):
        node = TextNode('print("hi")', TextType.CODE)
        html_node = text_node_to_html_node(node)
        assert html_node is not None
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, 'print("hi")')

    def test_link_node(self):
        node = TextNode('Google', TextType.LINK, url='https://google.com')
        html_node = text_node_to_html_node(node)
        assert html_node is not None
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'Google')
        assert html_node.props is not None
        self.assertEqual(html_node.props['href'], 'https://google.com')

    def test_image_node(self):
        node = TextNode('Alt text', TextType.IMAGE, url='https://image.com/img.png')
        html_node = text_node_to_html_node(node)
        assert html_node is not None
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        assert html_node.props is not None
        self.assertEqual(html_node.props['src'], 'https://image.com/img.png')
        self.assertEqual(html_node.props['alt'], 'Alt text')

    def test_empty_text_node(self):
        node = TextNode('', TextType.TEXT)
        html_node = text_node_to_html_node(node)
        assert html_node is not None
        self.assertEqual(html_node.value, '')

    def test_invalid_text_type(self):
        class FakeTextType:
            pass
        node = TextNode('Hello', FakeTextType)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_link_node_no_url(self):
        node = TextNode('Broken link', TextType.LINK)
        html_node = text_node_to_html_node(node)
        assert html_node is not None
        assert html_node.props is not None
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.props['href'], None)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_simple_code(self):
        node = TextNode('This is a `code` example', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, 'code')

    def test_simple_bold(self):
        node = TextNode('This is **bold** text', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, 'bold')

    def test_simple_italic(self):
        node = TextNode('This is _italic_ text', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, 'italic')

    def test_multiple_bold(self):
        node = TextNode('**Hello** world **again**!', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[1].text, 'Hello')
        self.assertEqual(new_nodes[3].text, 'again')

    def test_no_delimiter(self):
        node = TextNode('No formatting here', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, 'No formatting here')
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_non_text_node(self):
        node = TextNode('Bold node', TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_delimiter_at_start(self):
        node = TextNode('**Start bold** then text', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes[0].text, '')
        self.assertEqual(new_nodes[1].text, 'Start bold')

    def test_delimiter_at_end(self):
        node = TextNode('End bold **finish**', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes[-1].text, '')

    def test_unmatched_delimiter(self):
        node = TextNode('This is **bold text', TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], '**', TextType.BOLD)

    def test_mixed_delimiters(self):
        nodes = [TextNode('Text with `code` and _italic_ text', TextType.TEXT)]
        nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
        italic_nodes = [n for n in nodes if n.text_type == TextType.ITALIC]
        self.assertEqual(len(italic_nodes), 1)
        self.assertEqual(italic_nodes[0].text, 'italic')


class TestMarkdownExtraction(unittest.TestCase):
    def test_single_image(self):
        text = 'This is an ![image](https://i.imgur.com/zjjcJKZ.png)'
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [('image', 'https://i.imgur.com/zjjcJKZ.png')])

    def test_multiple_images(self):
        text = '![first](url1) and ![second](url2)'
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [('first', 'url1'), ('second', 'url2')])

    def test_image_with_empty_alt(self):
        text = '![](https://example.com/image.png)'
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [('', 'https://example.com/image.png')])

    def test_image_with_special_chars(self):
        text = '![a_b-c](https://example.com/img-1.png)'
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [('a_b-c', 'https://example.com/img-1.png')])

    def test_no_images(self):
        text = 'No images here, just text.'
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [])

    def test_image_and_link_mixed(self):
        text = '![img](imgurl) and [link](linkurl)'
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [('img', 'imgurl')])

    def test_single_link(self):
        text = 'This is a [link](https://example.com)'
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [('link', 'https://example.com')])

    def test_multiple_links(self):
        text = '[first](url1) and [second](url2)'
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [('first', 'url1'), ('second', 'url2')])

    def test_link_with_empty_text(self):
        text = '[](https://example.com)'
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [('', 'https://example.com')])

    def test_link_with_special_chars(self):
        text = '[a_b-c](https://example.com/page-1)'
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [('a_b-c', 'https://example.com/page-1')])

    def test_no_links(self):
        text = 'No links here, just text.'
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [])

    def test_link_and_image_mixed(self):
        text = '![img](imgurl) and [link](linkurl)'
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [('link', 'linkurl')])

    def test_link_with_exclamation_at_start(self):
        # ensure it does not match image syntax
        text = '![img](imgurl) [not image](linkurl)'
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [('not image', 'linkurl')])


class TestSplitNodesImage(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            'This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)',
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode('This is text with an ', TextType.TEXT),
                TextNode('image', TextType.IMAGE, 'https://i.imgur.com/zjjcJKZ.png'),
                TextNode(' and another ', TextType.TEXT),
                TextNode('second image', TextType.IMAGE, 'https://i.imgur.com/3elNhQu.png'),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode('Just some text with no images', TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_image_at_start(self):
        node = TextNode('![start](url1) followed by text', TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode('start', TextType.IMAGE, 'url1'),
                TextNode(' followed by text', TextType.TEXT)
            ],
            new_nodes
        )

    def test_image_at_end(self):
        node = TextNode('Text before image ![end](url2)', TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode('Text before image ', TextType.TEXT),
                TextNode('end', TextType.IMAGE, 'url2'),
            ],
            new_nodes
        )

    def test_multiple_images_adjacent(self):
        node = TextNode('![one](url1)![two](url2)', TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode('one', TextType.IMAGE, 'url1'),
                TextNode('two', TextType.IMAGE, 'url2'),
            ],
            new_nodes
        )

    def test_non_text_node_pass_through(self):
        node = TextNode('Already bold', TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


class TestSplitNodesLink(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            'This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)',
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode('This is text with a link ', TextType.TEXT),
                TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
                TextNode(' and ', TextType.TEXT),
                TextNode('to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev'),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode('Just some text with no links', TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_link_at_start(self):
        node = TextNode('[start](url1) followed by text', TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode('start', TextType.LINK, 'url1'),
                TextNode(' followed by text', TextType.TEXT),
            ],
            new_nodes
        )

    def test_link_at_end(self):
        node = TextNode('Text before link [end](url2)', TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode('Text before link ', TextType.TEXT),
                TextNode('end', TextType.LINK, 'url2'),
            ],
            new_nodes
        )

    def test_multiple_links_adjacent(self):
        node = TextNode('[one](url1)[two](url2)', TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode('one', TextType.LINK, 'url1'),
                TextNode('two', TextType.LINK, 'url2'),
            ],
            new_nodes
        )

    def test_non_text_node_pass_through(self):
        node = TextNode('Already bold', TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)


class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = 'Just some plain text'
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, 'Just some plain text')
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_bold_text(self):
        text = 'This is **bold** text'
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0].text, 'This is ')
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, 'bold')
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, ' text')
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_italic_text(self):
        text = 'This is _italic_ text'
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[1].text, 'italic')
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)

    def test_code_text(self):
        text = 'This is `code` example'
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[1].text, 'code')
        self.assertEqual(nodes[1].text_type, TextType.CODE)

    def test_image_text(self):
        text = 'An image ![alt](url) here'
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[1].text, 'alt')
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, 'url')

    def test_link_text(self):
        text = 'A link [click](http://example.com)'
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[1].text, 'click')
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, 'http://example.com')

    def test_mixed_content(self):
        text = 'Start **bold** _italic_ `code` ![img](url) [link](href)'
        nodes = text_to_textnodes(text)
        expected_types = [
            TextType.TEXT, TextType.BOLD, TextType.TEXT, TextType.ITALIC,
            TextType.TEXT, TextType.CODE, TextType.TEXT, TextType.IMAGE,
            TextType.TEXT, TextType.LINK
        ]
        self.assertEqual([n.text_type for n in nodes], expected_types)

    def test_text_with_multiple_same_delimiters(self):
        text = '**first** and **second**'
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[1].text, 'first')
        self.assertEqual(nodes[3].text, 'second')

    def test_text_with_no_delimiters(self):
        text = 'No formatting here'
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                'This is **bolded** paragraph',
                'This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line',
                '- This is a list\n- with items',
            ],
        )

    def test_single_block(self):
        md = 'Just a single paragraph with no blank lines'
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ['Just a single paragraph with no blank lines'])

    def test_leading_and_trailing_newlines(self):
        md = '\n\nLeading and trailing newlines\n\n'
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ['Leading and trailing newlines'])

    def test_multiple_consecutive_blank_lines(self):
        md = 'Paragraph 1\n\n\n\nParagraph 2'
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ['Paragraph 1', 'Paragraph 2'])

    def test_list_block_only(self):
        md = '- Item 1\n- Item 2\n- Item 3'
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ['- Item 1\n- Item 2\n- Item 3'])

    def test_empty_string(self):
        md = ''
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_blank_lines(self):
        md = '\n\n\n\n'
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_mixed_blank_lines_and_text(self):
        md = '\n\nText 1\n\n\nText 2\n\n\n\nText 3\n\n'
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ['Text 1', 'Text 2', 'Text 3'])


class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph_block(self):
        block = 'This is a normal paragraph.'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_block(self):
        block = '# This is a heading'
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = '### Subheading'
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = '```\nprint("Hello")\n```'
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = '> This is a quote\n> continuing the quote'
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = '- Item 1\n- Item 2\n- Item 3'
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = '1. First\n2. Second\n3. Third'
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_non_sequential(self):
        block = '1. First\n3. Second\n4. Third'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        block = ''
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == '__main__':
    unittest.main()

