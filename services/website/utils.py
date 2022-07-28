"""Module containing utility functions for the website service"""
import os.path

import markdown

_MARKDOWN_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "markdown")


def render_markdown(filename: str) -> str:
    """Reads the content in the markdown file and returns its html format"""
    file_path = os.path.join(_MARKDOWN_FOLDER, filename)

    with open(file_path, "r") as file:
        return markdown.markdown(file.read())
