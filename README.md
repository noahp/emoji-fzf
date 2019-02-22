[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/ambv/black)
[![Travis (.com)
branch](https://img.shields.io/travis/com/noahp/emoji-fzf/master.svg?style=for-the-badge)](https://travis-ci.com/noahp/emoji-fzf)
[![PyPI
version](https://img.shields.io/pypi/v/emoji-fzf.svg?style=for-the-badge)](https://pypi.org/project/emoji-fzf/)
[![PyPI
pyversions](https://img.shields.io/pypi/pyversions/emoji-fzf.svg?style=for-the-badge)](https://pypi.python.org/pypi/emoji-fzf/)
[![License:
MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

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
