# vim-marc
Plugin for transforming mrk snippets to mrc records.

[![asciicast](https://asciinema.org/a/Kv2B2FifC1VvbL1RkJZUuVFn9.svg)](https://asciinema.org/a/Kv2B2FifC1VvbL1RkJZUuVFn9?autoplay=1)

## Documentation
To view the documentation in vim type `:help vim-marc`
If the documentation is not loading, compile help tags file `:helptags ALL`

## Usage
Typing `:MrcCompile` in VIM ex-mode will cause a .mrc file to be converted to .mrk format.
Typeing `:MrcDisplay` in VIM ex-mode will cause a .mrk file to be converted to the .mrc format.

### Hot keys
Hot keys for the functions can be mapped in your VIM configuration file which is `.vimrc` on Linux/Unix or `vimrc` on Windows.

For example, to map the `MrcCompile` function to the Ctrl+k hotkey and the `MrcDisplay` function to Ctrl+l add the following to your VIMRC:
```
map <C-k> :MrcCompile<CR>
map <C-l> :MrcDisplay<CR>
```
