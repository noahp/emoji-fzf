[![Build Status](https://travis-ci.com/noahp/emoji-fzf.svg?branch=master)](https://travis-ci.com/noahp/emoji-fzf)
[![PyPI version](https://img.shields.io/pypi/v/emoji-fzf.svg?longCache=true)](https://pypi.org/project/emoji-fzf/)

# emoji fzf
Small utility for manipulating emojis via [fzf's](https://github.com/junegunn/fzf) `--preview` hook!

<img src="https://cdn.rawgit.com/noahp/emoji-fzf/assets/demo.svg">

Depends on fzf being installed to the system (integrates via bash alias/
function rather than using fzf bindings or whatnot).

# Use it
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
