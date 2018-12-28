# .vimrc
Lightweight Vim runtime configuration.

## Setup
Almost everything is setup and downloaded automatically. Just run the following commands, and you will be good to go.

* `cd ~`
* `wget https://raw.githubusercontent.com/Joklost/.vimrc/master/.vimrc`
* `vim`

## Usage
The .vimrc will check for updates on GitHub when you launch vim, and it will let you know if an update is available.

Available commands:
* `:CheckUpdate`
  * Will check if a newer version is on GitHub.
* `:Update`
  * Will force an update.

## Costumization
Adding custom plugins, commands or sourcing vimfiles can be done by creating a `config.json` file in the `~/.vim/` directory.

```json
{
    "plugins": [
        "neovimhaskell/haskell-vim"
    ],
    "cmds": [
        "nmap <up> :NERDTreeToggle<cr>",
        "nnoremap gV `[v`]"
    ],
    "vimfiles": [
        "~/.vim/custom.vim"
    ]
}
```

The vimfiles are sourced last, with the commands being sourced just before. Remember to type `:PlugInstall` when adding new plugins.

