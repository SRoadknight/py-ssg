import unittest 
from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_valid_no_child_parents(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_valid_child_parents(self):
        node_parent = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node =  ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                node_parent
            ],
        )
        expected = (
            "<p><b>Bold text</b>Normal text<i>italic"
            " text</i>Normal text<p><b>Bold text"
            "</b>Normal text<i>italic text</i>"
            "Normal text</p></p>"
        )
        self.assertEqual(node.to_html(), expected)


    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag="p", children=[]).to_html()

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(children=[]).to_html() 

    def test_valid_depth_parents(self):
        last_node_with_children =  ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        middle_node_with_grandchildren = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                last_node_with_children
            ],
        )

        top_node_with_grandchildren = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                middle_node_with_grandchildren
            ],
        )

        expected = (
            "<p><b>Bold text</b>Normal text<i>italic"
            " text</i>Normal text<p><b>Bold text"
            "</b>Normal text<i>italic text</i>"
            "Normal text<p><b>Bold text"
            "</b>Normal text<i>italic text</i>"
            "Normal text</p></p></p>"
        )
        self.assertEqual(
            top_node_with_grandchildren.to_html(), 
            expected
        )