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
@click.option(
    "-c",
    "--custom-aliases",
    "custom_aliases_file",
    help="Path to custom alias JSON file",
    type=click.File("r"),
    default=None,
)
def cli(custom_aliases_file=None):
    """CLI entrance point"""
    if custom_aliases_file:
        try:
            custom_aliases = json.load(custom_aliases_file)
            for item in custom_aliases:
                emoji = list(item.keys())[0]
                cust_aliases = item.get(emoji, [])
                for key, val in EMOJIS.items():
                    if val.get("emoji") == emoji:
                        EMOJIS[key]["aliases"] = set(
                            list(EMOJIS[key]["aliases"]) + cust_aliases
                        )
                        # No need to go further
                        break
        except AttributeError:
            print("The custom alias file provided is invalid", file=sys.stderr)
            sys.exit(2)


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
    "--skip-multichar",
    "skip_multichar",
    help="Whether to skip multicharacter emojis",
    is_flag=True,
    default=False,
    show_default=True,
)
def preview(prepend_emoji=False, skip_multichar=False):
    """Return an fzf-friendly search list for emoji"""
    for name, val in EMOJIS.items():
        emoji = val.get("emoji", "?")
        if skip_multichar and len(emoji) > 1:
            continue
        if prepend_emoji:
            click.secho(u"{} ".format(emoji), nl=False)
        click.secho(name, bold=True, nl=False)
        click.echo(u" {}".format(u" ".join(val.get("aliases", set()))))


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
    # https://stackoverflow.com/a/49680253/1872036
    # pylint: disable=no-value-for-parameter
    cli()
