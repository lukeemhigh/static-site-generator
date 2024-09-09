import unittest
from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)

    def test_url_is_not_none(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertIsNotNone(node.url)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, bold, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node", "text", None)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("This is a bold text node", "bold", None)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("This is a link", "link", "https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_text_node_to_html_node_image(self):
        text_node = TextNode(
            "This is an image description", "image", "https://www.example.com/image.jpg"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(
            html_node.props,
            {
                "src": "https://www.example.com/image.jpg",
                "alt": "This is an image description",
            },
        )


if __name__ == "__main__":
    unittest.main()
