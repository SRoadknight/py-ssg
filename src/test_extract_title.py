import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        title ="# This Is a Simple Title"
        self.assertEqual(extract_title(title), "This Is a Simple Title")
    
    def test_leading_whitespace(self):
        title ="   # This has leading whitespace"
        self.assertEqual(extract_title(title), "This has leading whitespace")

    def test_whitespace_leading_trailing(self):
        title = "   # This has whitespace on both sides   "
        self.assertEqual(extract_title(title), "This has whitespace on both sides")

    def test_title_later_in_md(self):
        md = """ This is some markdown
        where a title is found later on


        # Title
        """ 
        self.assertEqual(extract_title(md), "Title")

    def test_title_later_in_md(self):
        md = """ This is some markdown
        where a title is found later on 
        with whitespace

        
           # Title   
        """ 
        self.assertEqual(extract_title(md), "Title")

    def test_no_title(self):
        md = """ This is some markdown
        where no title will be found
        """ 
        with self.assertRaises(ValueError):
            extract_title(md)
        