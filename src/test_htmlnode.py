import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_tag_no_children(self):
        node = HTMLNode('p', 'this is a paragraph node')
        self.assertEqual(node.tag, 'p')
        self.assertIsNone(node.children)

    def test_value(self):
        node = HTMLNode('h1', 'this is a heading')
        self.assertEqual(node.value, 'this is a heading')

    def test_props_to_html(self):
        node_props = {
            'href': 'www.google.com',
            'target': '_blank'
        }
        expected_html = ' href="www.google.com" target="_blank"'
        node = HTMLNode('a', 'anchor tag', children=None, props=node_props)
        props_after_conversion = node.props_to_html()
        self.assertEqual(props_after_conversion, expected_html)


if __name__ == '__main__':
    unittest.main()
