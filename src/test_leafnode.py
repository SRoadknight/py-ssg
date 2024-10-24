import unittest 
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        dummy_props = {"href": "https://www.google.com", "target": "_blank"}
        node_with_props = LeafNode("a", "This is a link", dummy_props)
        converted_html = '<a href="https://www.google.com" target="_blank">This is a link</a>'
        self.assertEqual(node_with_props.to_html(), converted_html)

        node_without_props = LeafNode(tag="p", value="This is a paragraph")
        self.assertEqual(node_without_props.to_html(), "<p>This is a paragraph</p>")

        node_no_tag = LeafNode(tag=None, value="This has no tag")
        self.assertEqual(node_no_tag.to_html(), "This has no tag")

    def test_values(self):
        node1 = LeafNode("p", "This is a paragraph")
        self.assertEqual(node1.value, "This is a paragraph")
        self.assertEqual(node1.tag, "p")
        self.assertEqual(node1.props, None)