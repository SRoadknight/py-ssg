from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = map(lambda block: block.strip(), blocks)
    blocks = [block for block in blocks if block]
    return blocks 


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING.value
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE.value
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH.value
        return BlockType.QUOTE.value
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH.value
        return BlockType.ULIST.value
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH.value
        return BlockType.ULIST.value
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH.value
            i += 1
        return BlockType.OLIST.value
    return BlockType.PARAGRAPH.value


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH.value:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING.value:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE.value:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST.value:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST.value:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE.value:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "normal":
            return LeafNode(tag=None, value=text_node.text)
        case "bold":
            children = text_to_children(text_node.text)
            if children:
                return ParentNode("strong", children)
            return LeafNode(tag="strong", value=text_node.text)
        case "italic":
            children = text_to_children(text_node.text)
            if children:
                return ParentNode("em", children)
            return LeafNode(tag="em", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            if not text_node.url: 
                raise ValueError("Url not entered")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case "image":
            if not text_node.url:
                raise ValueError("Url not entered")
            return LeafNode(tag="img", value="", props={
                "src": text_node.url, 
                "alt": text_node.text
            })
        case _:
            raise ValueError("Invalid tag")



def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
        

