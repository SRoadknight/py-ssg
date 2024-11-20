import re

from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = parse_inline(text)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def parse_inline(text):
    stack = []
    result = []
    buffer = ""
    i  = 0

    while i < len(text):
        # Deal with closing italics and bolds in the correct order (if italic is inside bold, close italic first)
        if text[i:i+3] == "***" or text[i:i+2] == "**" or text[i] == "*":
            if buffer:
                if stack:
                    stack[-1].children.append(TextNode(text=buffer))
                else:
                    result.append(TextNode(text=buffer))
                buffer = ""
            
            # Closing italic inside bold (add italic to bold children) then closing bold
            if len(stack) == 2 and text[i:i+3] == "***" and stack[-1].text_type == TextType.ITALIC and stack[-2].text_type == TextType.BOLD:
                node = stack.pop()
                stack[-1].children.append(node)
                node = stack.pop()
                result.append(node)
                i += 3
            # Closing bold or italic (match with opening bold or italic)
            elif stack and stack[-1].text_type == (TextType.BOLD if text[i:i+2] == "**" else TextType.ITALIC):
                node = stack.pop()
                if stack:
                    stack[-1].children.append(node)
                else:
                    result.append(node)
                i += 2 if text[i:i+2] == "**" else 1
            # Opening bold or italic
            else:
                stack.append(TextNode(text_type=TextType.BOLD if text[i:i+2] == "**" else TextType.ITALIC))
                i += 2 if text[i:i+2] == "**" else 1
        # Adding text to buffer        
        else:
            buffer += text[i]
            i += 1

    # Flush buffer
    if buffer:
        if stack:
            stack[-1].children.append(TextNode(text=buffer))
        else:
            result.append(TextNode(text=buffer))
    # Close all unclosed bolds and italics
    while stack:
        node = stack.pop()
        if stack:
            stack[-1].children.append(node)
        else:
            result.append(node)

    return result

                
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))
            new_nodes.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(text=original_text, text_type=TextType.TEXT))
    return new_nodes