[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/ambv/black)
[![GitHub Workflow
Status](https://img.shields.io/github/actions/workflow/status/noahp/emoji-fzf/main.yml?branch=main&style=for-the-badge)](https://github.com/noahp/emoji-fzf/actions)
[![PyPI
version](https://img.shields.io/pypi/v/emoji-fzf.svg?style=for-the-badge)](https://pypi.org/project/emoji-fzf/)
[![PyPI
pyversions](https://img.shields.io/pypi/pyversions/emoji-fzf.svg?style=for-the-badge)](https://pypi.python.org/pypi/emoji-fzf/)
[![License:
MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

- [emoji-fzf](#emoji-fzf)
  - [Installation](#installation)
    - [zsh plugin](#zsh-plugin)
    - [Manually](#manually)
      - [Shell alias](#shell-alias)
      - [vim](#vim)
  - [Alternative setup](#alternative-setup)
  - [Custom emoji aliases](#custom-emoji-aliases)
  - [Development/testing](#developmenttesting)
    - [Building package for publishing](#building-package-for-publishing)

<!-- omit in toc -->

# emoji-fzf

Small utility for manipulating emojis via
[fzf's](https://github.com/junegunn/fzf) `--preview` hook!

<img src="https://cdn.rawgit.com/noahp/emoji-fzf/assets/demo.svg">

## Installation

1. Install `fzf` if you don't have it already to use its preview browser:

   https://github.com/junegunn/fzf#installation

2. Install the latest release of `emoji-fzf` from pypi:

   ```bash
   pip install emoji-fzf
   ```

See `emoji-fzf --help` for supported commands.

_This project allows you to install the tool in an isolated environment:
https://github.com/pipxproject/pipx_

### zsh plugin

There's an excellent zsh plugin available, see here (thanks @pschmitt !):
https://github.com/pschmitt/emoji-fzf.zsh

### Manually

#### Shell alias

You could add a shell alias like the following to your shell init script:

```bash
# if you aren't installing to a virtual env, you may need to add this to path
# (if it wasn't already) to access the tool from a pip installation
export PATH=$PATH:~/.local/bin

# add me to your ~/.bashrc or ~/.zshrc or whatnot
alias emoj="emoji-fzf preview | fzf -m --preview "emoji-fzf get --name {1}" | cut -d " " -f 1 | emoji-fzf get"
# to copy to xclip system keyboard (on mac use pbcopy) after selecting
emoj | xclip -selection c
```

#### vim

You can also add the following to a `~/.vimrc` file (apologies for the kludgy
vimscript, I'm not great at it), to enable `C-e` to open the emoji picker and
insert the selected emoji:

```vimscript
" Use emoji-fzf and fzf to fuzzy-search for emoji, and insert the result
function! InsertEmoji(emoji)
    let @a = system('cut -d " " -f 1 | emoji-fzf get', a:emoji)
    normal! "agP
endfunction

command! -bang Emoj
  \ call fzf#run({
      \ 'source': 'emoji-fzf preview',
      \ 'options': '--preview ''emoji-fzf get --name {1}''',
      \ 'sink': function('InsertEmoji')
      \ })
" Ctrl-e in normal and insert mode will open the emoji picker.
" Unfortunately doesn't bring you back to insert mode 😕
map <C-e> :Emoj<CR>
imap <C-e> <C-o><C-e>
```

## Alternative setup

If you prefer not to use fzf's preview feature and have the emojis appear
before their aliases you can use the following alias instead:

```bash
alias emoj="emoji-fzf preview --prepend | fzf | awk '{ print \$1 }'"
```

## Custom emoji aliases

emoji-fzf uses a pre-defined set of aliases for every emoji. If you want to
define your own, ie add custom aliases for some emojis you can do this via the
`--custom-aliases` flag.

Please note that these aliases will be appended to the list of pre-defined
aliases and not replace them.

1. First you need to create a JSON file with the following structure:

   ```json
   [
     {
       "👍": ["my-custom-alias", "good-boy"]
     },
     {
       "💯": ["epic-victory-royale"]
     }
   ]
   ```

2. Now you can call `emoji-fzf` like so:

   ```bash
   emoji-fzf --custom-aliases /path/to/your-custom-aliases.json preview
   ```

## Development/testing

This uses a Dockerfile to keep the test build environment relatively clean and
locked. The full test infrastructure is:

- Docker container, based on Ubuntu 20.04
- tox to run the tests + build checks
- pre-commit to run isort, black, etc.
- check-wheel-contents for built wheel sanity

To run the test suite in docker just as CI does:

```bash
./test.sh
```

### Building package for publishing

This just uses old timey setuptools:

```bash
python setup.py sdist bdist_wheel
```

Use `twine` to upload to pypi.
