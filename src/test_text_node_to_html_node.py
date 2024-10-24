import unittest
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_no_tag(self):
        node = TextNode("I have no tag", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "I have no tag")
    
    def test_basic_tag(self):
        node = TextNode("I am bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>I am bold</b>")

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<a href=\"https://www.google.com\">Google</a>")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<img src=\"https://www.google.com\" alt=\"This is an image\" />")

    def test_invalid_lin(self):
        node = TextNode("This is an invalid link", TextType.LINK)
        with self.assertRaises(ValueError):
            html_node = text_node_to_html_node(node)

    def test_invalid_image(self):
        node = TextNode("This is an invalid image", TextType.IMAGE)
        with self.assertRaises(ValueError):
             html_node = text_node_to_html_node(node)
