"""
Package setup.

Set me up with `python setup.py bdist_wheel --universal`
"""
from setuptools import setup

setup(
    # I think using `-` instead of `_` is more user-friendly, but due to python
    # import directives not allowing `-`, keep everything consistent with `_`.
    name="emoji_fzf",
    version="0.0.1",
    description="Emoji searcher for use with fzf",
    author="Noah Pendleton",
    author_email="2538614+noahp@users.noreply.github.com",
    url="https://github.com/noahp/emoji_fzf",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["click"],
    # using markdown as pypi description:
    # https://dustingram.com/articles/2018/03/16/markdown-descriptions-on-pypi
    setup_requires=["setuptools>=38.6.0", "wheel>=0.31.0", "twine>=1.11.0"],
    py_modules=["emoji_fzf"],
    data_files=[("emojilib", ["emojilib/emojis.json", "emojilib/LICENSE"])],
    entry_points={"console_scripts": ["emoji_fzf = emoji_fzf:cli"]},
    # For scripts, this corrects shebang replacement, from:
    #  https://github.com/pybuilder/pybuilder/issues/168
    options={"build_scripts": {"executable": "/usr/bin/env python"}},
)
