#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse emojilib keyword list and provide it as an fzf --preview input.
Result is a emoji cli fuzzy search utility 🎉!
"""
from __future__ import print_function
import argparse
import sys
from emoji_fzf.emoji_fzf_emojilib import EMOJIS


def preview(args):
    """Return an fzf-friendly search list for emoji"""
    del args
    for key, val in EMOJIS.items():
        try:
            print(key, u" {}".format(u" ".join(val["keywords"])))
        except UnicodeEncodeError:
            pass


def get(args):
    """
    Return an emoji by canonical name. Pipe a name string in on stdin, or
    provide the name via `--name` arg.
    """
    name = args.name
    if name is None and not sys.stdin.isatty():
        name = sys.stdin.read().strip()
    if not name:
        sys.exit(-1)

    render = EMOJIS[name]["char"]

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


def get_version():
    """get package version"""
    from emoji_fzf.version import __VERSION__

    return __VERSION__


def main():
    """cli entrance point"""
    parser = argparse.ArgumentParser(
        description="Print emoji from canonical name, or return a list of alias for emojis"
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(get_version())
    )

    subparsers = parser.add_subparsers()
    parser_get = subparsers.add_parser(
        "get",
        help=(
            "Return an emoji by canonical name. Pipe a name string in on stdin, or"
            " provide the name via `--name` arg."
        ),
    )
    parser_get.add_argument("--name", type=str, help="Name of emoji to retrieve")
    parser_get.set_defaults(func=get)

    parser_preview = subparsers.add_parser(
        "preview", help="Return an fzf-friendly search list for emoji"
    )
    parser_preview.set_defaults(func=preview)

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
