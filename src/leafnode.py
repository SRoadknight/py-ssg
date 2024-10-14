from htmlnode import HTMLNode 

class LeafNode(HTMLNode):

    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)
    
    def to_html(self):
        if not self.value: 
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value 
        
        html_props = self.props_to_html()
        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"
