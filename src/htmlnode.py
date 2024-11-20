class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        self.value = value 
        self.children = children 
        self.props = props 
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        s = ""
        for key, value in self.props.items():
            s += f" {key}=\"{value}\""
        return s

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


SELF_CLOSING = {"img"}

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value 
        
        html_props = self.props_to_html()
        if self.tag in SELF_CLOSING:
            return f"<{self.tag}{html_props} />"
        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=[], props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.children:
            raise ValueError("All parent nodes must have a child")
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        
        s = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
           s += child.to_html()
        return s + f"</{self.tag}>"
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


