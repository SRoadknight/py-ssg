import re

from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for index, old_node in enumerate(old_nodes):
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        split_nodes = process_text_node(old_nodes, old_node, index, delimiter, text_type)
        new_nodes.extend(split_nodes)
    return new_nodes

def process_text_node(old_nodes, current_node, index, delimiter, text_type):
    split_nodes = []
    sections = current_node.text.split(delimiter)
    if len(sections) % 2 == 0:
        split_nodes = handle_even_sections(old_nodes, index, sections, delimiter, text_type)
    else:
        split_nodes = handle_odd_sections(sections, text_type)
    return split_nodes

def handle_even_sections(old_nodes, index, sections, delimiter, text_type):
    split_nodes = [TextNode(sections[0], TextType.TEXT)]
    current_index = index + 1
    if len(sections) >= 2:
        split_nodes.append(TextNode(sections[1], text_type if text_type == TextType.BOLD else TextType.TEXT))
    combined_text = "".join(sections[2:])
    while current_index < len(old_nodes):
        current_node = old_nodes[current_index]
        if current_node.text_type != TextType.TEXT.value:
            combined_text += f"**{current_node.text}**"
            current_index += 1
        elif delimiter in current_node.text:
            combined_text = handle_delimiter_in_text(current_node, combined_text, delimiter)
            del old_nodes[index + 1 : current_index]
            split_nodes.append(TextNode(combined_text, TextType.ITALIC))
            break
    else:
        handle_unclosed_delimiter(old_nodes, index, split_nodes, delimiter)
    return split_nodes

def handle_delimiter_in_text(current_node, combined_text, delimiter):
    before_delimiter = current_node.text.split(delimiter)[0]
    after = current_node.text.split(delimiter)[1:]
    combined_text += before_delimiter
    current_node.text = f"{delimiter}".join(after)
    return combined_text

def handle_unclosed_delimiter(old_nodes, index, split_nodes, delimiter):
    previous_node = old_nodes[index - 1]
    combined_text = ""
    if previous_node.text_type == TextType.BOLD.value and previous_node.text[0] == delimiter:
        before_delimiter = old_nodes[index].text.split(delimiter)[0]
        after = "".join(old_nodes[index].text.split(delimiter)[1:])
        combined_text = f"**{previous_node.text[1:]}**{before_delimiter}"
        previous_node.text_type = TextType.ITALIC.value
        previous_node.text = combined_text
        split_nodes[0].text = after
    elif previous_node.text_type == TextType.BOLD.value and delimiter in previous_node.text:
        previous_node.text += delimiter
    else:
        raise ValueError("Invalid markdown: formatted section not closed")

def handle_odd_sections(sections, text_type):
    split_nodes = []
    for i, section in enumerate(sections):
        if section == "":
            continue
        node_type = TextType.TEXT if i % 2 == 0 else text_type
        split_nodes.append(TextNode(section, node_type))
    return split_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
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
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
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
        if old_node.text_type != TextType.TEXT.value:
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
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes