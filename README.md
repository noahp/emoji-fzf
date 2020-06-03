[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/ambv/black)
[![GitHub Workflow
Status](https://img.shields.io/github/workflow/status/noahp/emoji-fzf/main-ci?style=for-the-badge)](https://github.com/noahp/emoji-fzf/actions)
[![PyPI
version](https://img.shields.io/pypi/v/emoji-fzf.svg?style=for-the-badge)](https://pypi.org/project/emoji-fzf/)
[![PyPI
pyversions](https://img.shields.io/pypi/pyversions/emoji-fzf.svg?style=for-the-badge)](https://pypi.python.org/pypi/emoji-fzf/)
[![License:
MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

# emoji fzf

Small utility for manipulating emojis via
[fzf's](https://github.com/junegunn/fzf) `--preview` hook!

<img src="https://cdn.rawgit.com/noahp/emoji-fzf/assets/demo.svg">

Depends on fzf being installed to the system (integrates via bash alias/
function rather than using fzf bindings or whatnot).

## Use it

To use with fzf's preview browser, you'll need to install fzf, see instructions:
https://github.com/junegunn/fzf#installation

```bash
pip install emoji-fzf

# if you aren't installing to a virtual env, you may need to add this to path
# (if it wasn't already) to access the tool
export PATH=$PATH:~/.local/bin

# add me to your ~/.bashrc or ~/.zshrc or whatnot
alias emoj="emoji-fzf preview | fzf --preview 'emoji-fzf get --name {1}' | cut -d \" \" -f 1 | emoji-fzf get"
# to copy to xclip system keyboard (on mac use pbcopy) after selecting
emoj | xclip -selection c
```

## Alternative setup

If you prefer not to use fzf's preview feature and have the emojis appear
before their aliases you can use the following alias instead:

```bash
alias emoj="emoji-fzf preview --prepend | fzf | awk '{ print \$1 }'"
```

## Custom aliases

emoji-fzf uses a pre-defined set of aliases for every emoji. If you want to
define your own, ie add custom aliases for some emojis you can do this via the
`--custom-aliases` flag.

Please note that these aliases will be appended to the list of pre-defined
aliases and not replace them.

1. First you need to create a JSON file with the following structure:

```json
[
  {
    "emoji": "👍",
    "aliases": [
      "my-custom-alias",
      "good-boy"
    ]
  },
  {
    "emoji": "💯",
    "aliases": [
      "epic-victory-royale"
    ]
  }
]
```

2. Now you can call `emoji-fzf` like so:

```bash
emoji-fzf preview --custom-aliases /path/to/your-custom-aliases.json
```

## Development/testing

This uses a Dockerfile to keep the test build environment relatively clean and
locked. The full test infrastructure is:

- Docker container, based on buildpack Debian jessie image
- tox-conda, which enables us to install any python version available on conda
  channels (here just a few since the supported list is relatively small)
- tox to run the tests + build checks
- black formatting check
- check-wheel-contents and isort for more styling/idiomatic usage checks

To run the test suite in docker just as CI does:

```bash
# build the image and tag it as 'emoji-fzf'
docker build -t emoji-fzf --build-arg "UID=$(id -u)" -f Dockerfile

# from this repo root, mount the cwd into the container and run tox
docker run -v $(pwd):/mnt/workspace -t emoji-fzf bash -c "cd /mnt/workspace && tox"
```
