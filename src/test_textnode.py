import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_text_type(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node.text_type, node2.text_type)

    def test_not_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is not a text node', TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_no_url(self):
        node = TextNode('This is a text node', TextType.BOLD)
        self.assertIsNone(node.url)

    def test_url(self):
        expected_url = 'www.youtube.com'
        node = TextNode('This is a text node', TextType.IMAGE, 'www.youtube.com')
        self.assertEqual(node.url, expected_url)


if __name__ == '__main__':
    unittest.main()
