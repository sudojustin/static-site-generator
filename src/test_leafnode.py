import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_tag_no_children(self):
        node = LeafNode('p', 'this is a paragraph node')
        self.assertEqual(node.tag, 'p')
        self.assertIsNone(node.children)

    def test_value(self):
        node = LeafNode('h1', 'this is a heading')
        self.assertEqual(node.value, 'this is a heading')

    def test_props_to_html(self):
        node_props = {
            'href': 'www.google.com',
            'target': '_blank'
        }
        expected_html = ' href="www.google.com" target="_blank"'
        node = LeafNode('a', 'anchor tag', props=node_props)
        props_after_conversion = node.props_to_html()
        self.assertEqual(props_after_conversion, expected_html)

    def test_leaf_to_html(self):
        node = LeafNode('p', 'Hello, World!')
        self.assertEqual(node.to_html(), '<p>Hello, World!</p>')

if __name__ == '__main__':
    unittest.main()
