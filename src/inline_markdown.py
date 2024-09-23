from typing import List, Tuple
import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: str
) -> List[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.text.name:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.text.name))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    image_re = re.compile(r"!\[(.*?)\]\((.*?)\)")
    return image_re.findall(text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    link_re = re.compile(r"(?<!!)\[(.*?)\]\((.*?)\)")
    return link_re.findall(text)


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.text.name:
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
                new_nodes.append(TextNode(sections[0], TextType.text.name))
            new_nodes.append(TextNode(image[0], TextType.image.name, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.text.name))
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.text.name:
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
                new_nodes.append(TextNode(sections[0], TextType.text.name))
            new_nodes.append(TextNode(link[0], TextType.link.name, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.text.name))
    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.text.name)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.bold.name)
    nodes = split_nodes_delimiter(nodes, "*", TextType.italic.name)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code.name)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
