import unittest 
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self): 
        dummy_props = {"href": "https://www.google.com", "target": "_blank"}
        props_string =  " href=\"https://www.google.com\" target=\"_blank\""
        node = HTMLNode("a", "Click Here", props=dummy_props)
        converted_props = node.props_to_html()
        self.assertEqual(converted_props, props_string)
    
        node_none = HTMLNode("p", "I'm a paragraph", None, None)
        converted_props_none = node_none.props_to_html()
        self.assertEqual(converted_props_none, "")

    def test_values(self):
        node1 = HTMLNode("p", "paragraph", None, None)
        self.assertEqual(node1.tag, "p")
        self.assertEqual(node1.value, "paragraph")
        self.assertEqual(node1.children, None)
        self.assertEqual(node1.props, None)
        self.assertEqual(node1.__repr__(), "HTMLNode(p, paragraph, children: None, None)")

        node2 = HTMLNode("div", "This is a div", [node1], None)
        self.assertEqual(node2.children, [node1])
        self.assertEqual(
            node2.__repr__(), 
            "HTMLNode(div, This is a div, children: [HTMLNode(p, paragraph, children: None, None)], None)"
        )

