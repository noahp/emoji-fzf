# emoji fzf
Small utility for manipulating emojis via fzf's `--preview` hook!

Depends on fzf being installed to the system (integrates via bash alias/
function rather than using fzf bindings or whatnot).

# Use it
```bash
pip install emoji_fzf

# add me to your ~/.bashrc or ~/.zshrc or whatnot
alias emoj="emoji_fzf preview | fzf --preview 'emoji_fzf get --name {1}' | cut -d \" \" -f 1 | emoji_fzf get"
# to copy to xclip or pbcopy after selecting
emoj | xclip
```
