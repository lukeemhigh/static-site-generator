import re
from enum import Enum
from typing import List
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

BlockType = Enum(
    "BlockType",
    ["paragraph", "heading", "code", "quote", "unordered_list", "ordered_list"],
)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    title_re = re.compile(r"^#{1}\s.*$", re.MULTILINE)
    for line in lines:
        if title_re.match(line):
            return line.lstrip("# ")
    raise Exception("No title found")


def markdown_to_blocks(markdown: str) -> List[str]:
    return list(
        filter(None, map(lambda block: block.strip(), re.split(r"\n\n", markdown)))
    )


def block_to_block_type(block: str) -> str:
    lines = block.split("\n")
    block_types_re = {
        "heading": re.compile(r"^#{1,6}\s.*$", re.MULTILINE),
        "code": re.compile(r"^`{3}\n.*\n`{3}", re.MULTILINE),
        "quote": re.compile(r"^>\s?.*$", re.MULTILINE),
        "unordered_list": re.compile(r"^[\*-]\s.*$", re.MULTILINE),
        "ordered_list": re.compile(r"^1\.\s.*$", re.MULTILINE),
    }
    for block_type, pattern in block_types_re.items():
        if pattern.match(block):
            match block_type:
                case "heading":
                    return BlockType.heading.name
                case "code":
                    if len(lines) > 1:
                        return BlockType.code.name
                case "quote":
                    for line in lines:
                        if not line.startswith(">"):
                            return BlockType.paragraph.name
                    return BlockType.quote.name
                case "unordered_list":
                    for line in lines:
                        if not pattern.match(line):
                            return BlockType.paragraph.name
                    return BlockType.unordered_list.name
                case "ordered_list":
                    i = 1
                    for line in lines:
                        if not line.startswith(f"{i}. "):
                            return BlockType.paragraph.name
                        i += 1
                    return BlockType.ordered_list.name
    return BlockType.paragraph.name


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children_list: List[ParentNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children_list.append(html_node)
    return ParentNode("div", children_list)


def block_to_html_node(block) -> ParentNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.paragraph.name:
            return paragraph_to_html_node(block)
        case BlockType.heading.name:
            return heading_to_html_node(block)
        case BlockType.code.name:
            return code_to_html_node(block)
        case BlockType.quote.name:
            return quote_to_html_node(block)
        case BlockType.unordered_list.name:
            return ulist_to_html_node(block)
        case BlockType.ordered_list.name:
            return olist_to_html_node(block)
        case _:
            raise ValueError("Invalid block type")


def text_to_children(text: str) -> List[LeafNode]:
    textnodes = text_to_textnodes(text)
    children: List[LeafNode] = []
    for textnode in textnodes:
        html_node = text_node_to_html_node(textnode)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {block}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items: List[ParentNode] = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items: List[ParentNode] = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines: List[str] = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
