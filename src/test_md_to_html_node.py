import unittest
import textwrap
from md_to_html_node import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
        """).strip()
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>',
        )

    def test_codeblock(self):
        md = textwrap.dedent("""
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
        """).strip()
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>',
        )

    def test_heading(self):
        md = '# Heading 1\n\n## Heading 2'
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Heading 1</h1><h2>Heading 2</h2></div>',
        )

    def test_quote_block(self):
        md = '> This is a quote\n> continued here'
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>This is a quote continued here</blockquote></div>',
        )

    def test_unordered_list(self):
        md = '- Item 1\n- Item 2\n- Item 3'
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>',
        )

    def test_ordered_list(self):
        md = '1. First\n2. Second\n3. Third'
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>',
        )

    def test_mixed_blocks(self):
        md = textwrap.dedent("""
            # Heading

            This is **bold** text

            - List item 1
            - List item 2

            ```
            Code here
            ```
        """).strip()
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Heading</h1><p>This is <b>bold</b> text</p><ul><li>List item 1</li><li>List item 2</li></ul><pre><code>Code here\n</code></pre></div>',
        )


if __name__ == '__main__':
    unittest.main()

