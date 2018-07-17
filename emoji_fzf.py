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

# The emoji library is installed to the system directory on package install
EMOJI_LIB_JSON = os.path.join(sys.prefix, "emojilib", "emojis.json")


@click.group()
@click.version_option()
def cli():
    """CLI entrance point"""
    pass


@cli.command()
def preview():
    """Return an fzf-friendly search list for emoji"""
    with open(EMOJI_LIB_JSON, "r") as emojifile:
        emojilist = json.load(emojifile)
    for key, val in emojilist.items():
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
        raise RuntimeError("No emoji key passed 😭")
    with open(EMOJI_LIB_JSON, "r") as emojifile:
        emojilist = json.load(emojifile)
    render = emojilist[name]["char"]

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
