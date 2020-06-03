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
@click.pass_context
@click.option(
    "-c",
    "--custom-aliases",
    "custom_aliases_file",
    help="Path to custom alias JSON file",
    type=click.File("r"),
    default=None,
)
def cli(ctx, custom_aliases_file=None):
    """CLI entrance point"""
    ctx.ensure_object(dict)
    emojis_custom = EMOJIS
    if custom_aliases_file:
        try:
            custom_aliases = json.load(custom_aliases_file)
        except AttributeError:
            print("The custom alias file provided is invalid", file=sys.stderr)
            sys.exit(2)

        for item in custom_aliases:
            emoji = list(item.keys())[0]
            cust_aliases = item.get(emoji, [])
            for key, val in emojis_custom.items():
                if val.get("emoji") == emoji:
                    emojis_custom[key]["aliases"] = set(
                        list(emojis_custom[key]["aliases"]) + cust_aliases
                    )
                    # No need to go further
                    break

    ctx.obj["emojis"] = emojis_custom


@cli.command()
@click.option(
    "--prepend",
    "prepend_emoji",
    help="Whether to prefix the preview with the emoji",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.pass_context
def preview(ctx, prepend_emoji=False):
    """Return an fzf-friendly search list for emoji"""
    for name, val in ctx.obj["emojis"].items():
        emoji = val.get("emoji", "?")
        if prepend_emoji:
            click.secho(u"{} ".format(emoji), nl=False)
        click.secho(name, bold=True, nl=False)
        click.echo(u" {}".format(u" ".join(val.get("aliases", set()))))


@cli.command()
@click.option("--name", help="Name of emoji to retrieve", type=click.STRING)
@click.pass_context
def get(ctx, name=None):
    """
    Return an emoji by canonical name. Pipe a name string in on stdin, or
    provide the name via `--name` arg.
    """
    if name is None and not sys.stdin.isatty():
        name = click.get_text_stream("stdin").read().strip()
    if not name:
        sys.exit(-1)

    render = ctx.obj["emojis"][name]["emoji"]

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
