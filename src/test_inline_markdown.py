import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TextInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is **bold** text", TextType.text.name)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold.name)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.text.name),
                TextNode("bold", TextType.bold.name),
                TextNode(" text", TextType.text.name),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.text.name
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold.name)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text.name),
                TextNode("bolded", TextType.bold.name),
                TextNode(" word and ", TextType.text.name),
                TextNode("another", TextType.bold.name),
            ],
            new_nodes,
        )

    def text_delim_bold_multiword(self):
        node = TextNode(
            "This is text with two **bolded words** and **another**", TextType.text.name
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold.name)
        self.assertListEqual(
            [
                TextNode("This is text with two ", TextType.text.name),
                TextNode("bolded words", TextType.bold.name),
                TextNode(" and ", TextType.text.name),
                TextNode("another", TextType.bold.name),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.text.name)
        new_nodes = split_nodes_delimiter([node], "*", TextType.italic.name)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text.name),
                TextNode("italic", TextType.italic.name),
                TextNode(" word", TextType.text.name),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.text.name)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold.name)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.italic.name)
        self.assertListEqual(
            [
                TextNode("bold", TextType.bold.name),
                TextNode(" and ", TextType.text.name),
                TextNode("italic", TextType.italic.name),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.text.name)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code.name)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text.name),
                TextNode("code block", TextType.code.name),
                TextNode(" word", TextType.text.name),
            ],
            new_nodes,
        )

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            images,
        )

    def test_extract_images_no_exclamation_mark(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertListEqual([], images)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            links,
        )

    def test_extract_links_on_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        links = extract_markdown_links(text)
        self.assertListEqual([], links)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.text.name,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text.name),
                TextNode(
                    "image", TextType.image.name, "https://i.imgur.com/zjjcJKZ.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            TextType.text.name,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "image", TextType.image.name, "https://www.example.com/image.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text.name,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text.name),
                TextNode(
                    "image", TextType.image.name, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.text.name),
                TextNode(
                    "second image",
                    TextType.image.name,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.text.name,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text.name),
                TextNode("link", TextType.link.name, "https://boot.dev"),
                TextNode(" and ", TextType.text.name),
                TextNode("another link", TextType.link.name, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.text.name),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.text.name),
                TextNode("text", TextType.bold.name),
                TextNode(" with an ", TextType.text.name),
                TextNode("italic", TextType.italic.name),
                TextNode(" word and a ", TextType.text.name),
                TextNode("code block", TextType.code.name),
                TextNode(" and an ", TextType.text.name),
                TextNode(
                    "obi wan image",
                    TextType.image.name,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.text.name),
                TextNode("link", TextType.link.name, "https://boot.dev"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
