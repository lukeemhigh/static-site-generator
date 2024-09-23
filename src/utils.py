import os
import shutil
from block_markdown import markdown_to_html_node, extract_title


def recursive_copy(source: str, destination: str) -> None:
    if not os.path.exists(destination):
        os.mkdir(destination)
    else:
        for item in os.listdir(destination):
            item_path = os.path.join(destination, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            elif os.path.isfile(item_path):
                os.remove(item_path)
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            recursive_copy(source_path, destination_path)


def generate_page(source_file, template_file, dest_file) -> None:
    print(f"Generating page from {source_file} to {dest_file} using {template_file}")
    with open(source_file, "r") as source_file:
        markdown = source_file.read()
    with open(template_file, "r") as template_file:
        template = template_file.read()
    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    dest_dir_path = os.path.dirname(dest_file)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_file, "w") as dest_file:
        dest_file.write(page)


def generate_pages_recursive(source_path, template_file, dest_path) -> None:
    for item in os.listdir(source_path):
        source_item_path = os.path.join(source_path, item)
        dest_item_path = os.path.join(dest_path, item)
        if os.path.isfile(source_item_path):
            dest_item_file = dest_item_path.rstrip(".md") + ".html"
            generate_page(source_item_path, template_file, dest_item_file)
        else:
            generate_pages_recursive(source_item_path, template_file, dest_item_path)
