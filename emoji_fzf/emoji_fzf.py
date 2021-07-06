#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse emojilib keyword list and provide it as an fzf --preview input.
Result is a emoji cli fuzzy search utility 🎉!
"""
from __future__ import print_function

import json
import shlex
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


def print_emoji_from_name(name):
    # skip unknown emojis
    if name not in EMOJIS:
        return

    render = EMOJIS[name]["emoji"]

    # include newline only if we're not redirected
    if sys.stdout.isatty():
        print(render)
    else:
        if sys.version_info < (3, 0):
            # the following is a lame hack to handle python 2 compatibility, oof
            # from: https://stackoverflow.com/a/20447935 . we have to disable
            # =all instead of just =import-outside-toplevel because python2.7
            # pylint doesn't support that flag :c
            import codecs  # pylint: disable=all

            utf8_writer = codecs.getwriter("utf8")
            sys.stdout = utf8_writer(sys.stdout)

        sys.stdout.write(render)


@cli.command()
@click.argument("name", nargs=-1, type=click.STRING)
@click.option("--name", "arg_name", help="Name of emoji to retrieve", type=click.STRING)
def get(name, arg_name):
    """
    Return 1 or more emoji by canonical name. Names can be piped in on stdin,
    passed by the '--name' arg, or passed as positional args, or any combination
    of those.
    """
    names = name + (arg_name,)
    if not sys.stdin.isatty():
        names = (
            tuple(shlex.split(click.get_text_stream("stdin").read().strip())) + names
        )

    for this_emoji in names:
        print_emoji_from_name(this_emoji)


if __name__ == "__main__":
    # https://stackoverflow.com/a/49680253/1872036
    # pylint: disable=no-value-for-parameter
    cli()
