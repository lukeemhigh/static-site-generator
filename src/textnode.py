from htmlnode import LeafNode
from enum import Enum

TextType = Enum("TextType", ["text", "bold", "italic", "code", "link", "image"])


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.text.name:
            return LeafNode(None, text_node.text, None)
        case TextType.bold.name:
            return LeafNode("b", text_node.text, None)
        case TextType.italic.name:
            return LeafNode("i", text_node.text, None)
        case TextType.code.name:
            return LeafNode("code", text_node.text, None)
        case TextType.link.name:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.image.name:
            return LeafNode(
                "img", "", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError("Unsupported text type")
