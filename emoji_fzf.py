#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse emojilib keyword list and provide it as an fzf --preview input.
Result is a emoji cli fuzzy search utility 🎉!
"""
from __future__ import print_function
import json
import os
import sys

import click
import pkg_resources

# The emoji library is installed relative to this package on install
if pkg_resources.resource_exists(__name__, "emojilib/emojis.json"):
    EMOJI_LIB_JSON = pkg_resources.resource_string(__name__, "emojilib/emojis.json")
else:
    # it's possible we're running from the source dist instead
    EMOJI_LIB_JSON = open(
        os.path.join(os.path.abspath(__file__), "emojilib", "emojis.json"), "r"
    ).read()

# Load and parse the emoji data now
EMOJI_LIB_JSON = json.loads(EMOJI_LIB_JSON)

# Sanity check
assert EMOJI_LIB_JSON, "Dang, emojilib/emojis.json is not installed 😢"


@click.group()
@click.version_option()
def cli():
    """CLI entrance point"""


@cli.command()
def preview():
    """Return an fzf-friendly search list for emoji"""
    for key, val in EMOJI_LIB_JSON.items():
        click.secho(key, bold=True, nl=False)
        click.echo(u" {}".format(u" ".join(val["keywords"])))


@cli.command()
@click.option("--name", help="Name of emoji to retrieve", type=click.STRING)
def get(name=None):
    """
    Return an emoji by canonical name. Pipe a name string in on stdin, or
    provide the name via `--name` arg.
    """
    if name is None and not sys.stdin.isatty():
        name = click.get_text_stream("stdin").read().strip()
    if not name:
        sys.exit(-1)

    render = EMOJI_LIB_JSON[name]["char"]

    # include newline only if we're not redirected
    if sys.stdout.isatty():
        print(render)
    else:
        if sys.version_info < (3, 0):
            # the following is a lame hack to handle python 2 compatibility, oof
            # from: https://stackoverflow.com/a/20447935
            import codecs

            utf8_writer = codecs.getwriter("utf8")
            sys.stdout = utf8_writer(sys.stdout)

        sys.stdout.write(render)


if __name__ == "__main__":
    cli()
