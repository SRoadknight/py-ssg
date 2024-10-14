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