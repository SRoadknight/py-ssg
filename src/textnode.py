from enum import Enum 

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

text_type_map_html = {
    TextType.TEXT: None,
    TextType.BOLD: "strong",
    TextType.ITALIC: "em",
    TextType.CODE: "code",
    TextType.LINK: "a",
    TextType.IMAGE: "img",
}

class TextNode():
    def __init__(self, text="", text_type=TextType.TEXT, children=None, url=None):
        self.text = text if text else ""
        self.text_type = text_type
        self.children = children if children else []
        self.url = url 

    def is_leaf(self):
        return not self.children
    
    def __eq__(self, other):
        return (
            self.text == other.text 
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        if self.is_leaf():
            return f"TextNode({self.text}, {self.text_type}, {self.url})"
        return f"TextNode({self.text}, {self.text_type}, {self.url}, {self.children})"
