"""
Package setup.

Set me up with `python setup.py bdist_wheel --universal`
"""
import io
from setuptools import setup

# Get long description from readme
with io.open("README.md", "rt", encoding="utf8") as readmefile:
    README = readmefile.read()

setup(
    # I think using `-` instead of `_` is more user-friendly, but due to python
    # import directives not allowing `-`, keep everything consistent with `_`.
    name="emoji-fzf",
    version="0.0.7",
    description="Emoji searcher for use with fzf",
    author="Noah Pendleton",
    author_email="2538614+noahp@users.noreply.github.com",
    url="https://github.com/noahp/emoji-fzf",
    project_urls={
        "Code": "https://github.com/noahp/emoji-fzf",
        "Issue tracker": "https://github.com/noahp/emoji-fzf/issues",
    },
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=["click"],
    # using markdown as pypi description:
    # https://dustingram.com/articles/2018/03/16/markdown-descriptions-on-pypi
    setup_requires=["setuptools>=38.6.0", "wheel>=0.31.0", "twine>=1.11.0"],
    py_modules=["emoji_fzf"],
    packages=["emojilib"],
    include_package_data=True,
    entry_points={"console_scripts": ["emoji-fzf = emoji_fzf:cli"]},
    # For scripts, this corrects shebang replacement, from:
    #  https://github.com/pybuilder/pybuilder/issues/168
    options={"build_scripts": {"executable": "/usr/bin/env python"}},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
