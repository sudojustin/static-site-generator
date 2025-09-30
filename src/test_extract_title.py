import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_header(self):
        self.assertEqual(extract_title('# Hello'), 'Hello')

    def test_header_with_whitespace(self):
        self.assertEqual(extract_title('#   Hello World  '), 'Hello World')

    def test_header_in_middle(self):
        md = 'Some text\n# My Title\nMore text'
        self.assertEqual(extract_title(md), 'My Title')

    def test_no_header(self):
        with self.assertRaises(ValueError):
            extract_title('No header here')

    def test_multiple_headers(self):
        md = '# First\n# Second'
        self.assertEqual(extract_title(md), 'First')

if __name__ == '__main__':
    unittest.main()

