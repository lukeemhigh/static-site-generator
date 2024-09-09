from textnode import TextNode


def main():
    dummy_node = TextNode("This is a text node", "bold", "https://www.boot.dev")

    print(dummy_node.__repr__())


if __name__ == "__main__":
    main()
