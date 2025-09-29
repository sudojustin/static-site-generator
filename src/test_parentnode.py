import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_children(self):
        child = LeafNode('p', 'this is a paragraph node')
        parent = ParentNode('div', [child])
        self.assertIsNotNone(parent.children)

    def test_no_children_exception(self):
        with self.assertRaises(ValueError, msg='ParentNode must have children'):
            parent = ParentNode('div', children=None)
            parent.to_html()

    def test_no_tag_exception(self):
        with self.assertRaises(ValueError, msg='ParentNode must have a tag'):
            child = LeafNode('p', 'this is a paragraph node')
            parent = ParentNode(tag=None, children=[child])
            parent.to_html()

    def test_to_html_with_children(self):
        child = LeafNode('span', 'child')
        parent = ParentNode('div', [child])
        self.assertEqual(parent.to_html(), '<div><span>child</span></div>')

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode('b', 'grandchild')
        child = ParentNode('span', [grandchild])
        parent = ParentNode('div', [child])
        self.assertEqual(
            parent.to_html(),
            '<div><span><b>grandchild</b></span></div>',
        )

    def test_multiple_mixed_children(self):
        children = [
            LeafNode('b', 'Bold'),
            LeafNode(None, ' plain '),
            LeafNode('i', 'italic'),
        ]
        parent = ParentNode('p', children)
        expected = '<p><b>Bold</b> plain <i>italic</i></p>'
        self.assertEqual(parent.to_html(), expected)

    def test_deeply_nested_nodes(self):
        node = ParentNode('div', [
            ParentNode('section', [
                ParentNode('article', [
                    LeafNode('p', 'deep text')
                ])
            ])
        ])
        expected = '<div><section><article><p>deep text</p></article></section></div>'
        self.assertEqual(node.to_html(), expected)

    def test_props_rendering(self):
        child = LeafNode('span', 'hello')
        parent = ParentNode('div', [child], props={'class': 'greeting', 'id': 'main'})
        html = parent.to_html()
        self.assertIn('<div class="greeting" id="main">', html)
        self.assertTrue(html.endswith('</div>'))

    def test_empty_leafnode_value(self):
        children = [
            LeafNode('b', ''),
            LeafNode(None, 'Text after empty bold')
        ]
        parent = ParentNode('p', children)
        expected = '<p><b></b>Text after empty bold</p>'
        self.assertEqual(parent.to_html(), expected)


if __name__ == '__main__':
    unittest.main()
