from utils import recursive_copy, generate_pages_recursive


def main():
    recursive_copy("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
