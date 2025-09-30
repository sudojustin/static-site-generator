import unittest
from blocktype import block_to_block_type, BlockType

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

