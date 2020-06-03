#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse emojilib keyword list and provide it as an fzf --preview input.
Result is a emoji cli fuzzy search utility 🎉!
"""
from __future__ import print_function

import json
import sys

import click

from .emoji_fzf_emojilib import EMOJIS


@click.group()
@click.version_option()
def cli():
    """CLI entrance point"""


@cli.command()
@click.option(
    "--prepend",
    "prepend_emoji",
    help="Whether to prefix the preview with the emoji",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    "-c",
    "--custom-aliases",
    "custom_aliases_file",
    help="Path to custom alias JSON file",
    type=click.File("r"),
    default=None,
)
def preview(prepend_emoji=False, custom_aliases_file=None):
    """Return an fzf-friendly search list for emoji"""
    custom_aliases = {}
    if custom_aliases_file:
        try:
            custom_aliases = {
                x.get("emoji"): x.get("aliases") for x in json.load(custom_aliases_file)
            }
        except AttributeError:
            print("Invalid customization provided", file=sys.stderr)
            sys.exit(2)

    for key, val in EMOJIS.items():
        emoji = val.get("emoji", "?")
        if prepend_emoji:
            click.secho(u"{} ".format(emoji), nl=False)
        click.secho(key, bold=True, nl=False)
        aliases = list(val.get("aliases", []))
        aliases += custom_aliases.get(emoji, [])
        click.echo(u" {}".format(u" ".join(aliases)))


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

    render = EMOJIS[name]["emoji"]

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
