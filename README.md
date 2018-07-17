[![Build Status](https://travis-ci.com/noahp/emoji_fzf.svg?branch=master)](https://travis-ci.com/noahp/emoji_fzf)
[![PyPI version](https://img.shields.io/pypi/v/emoji_fzf.svg?longCache=true)](https://pypi.org/project/emoji_fzf/)

# emoji fzf
Small utility for manipulating emojis via [fzf](https://github.com/junegunn/fzf's) `--preview` hook!

Depends on fzf being installed to the system (integrates via bash alias/
function rather than using fzf bindings or whatnot).

# Use it
To use with fzf's preview browser, you'll need to install fzf, see instructions:
https://github.com/junegunn/fzf#installation

```bash
pip install emoji_fzf

# add me to your ~/.bashrc or ~/.zshrc or whatnot
alias emoj="emoji_fzf preview | fzf --preview 'emoji_fzf get --name {1}' | cut -d \" \" -f 1 | emoji_fzf get"
# to copy to xclip (use pbcopy on mac) after selecting
emoj | xclip
```
