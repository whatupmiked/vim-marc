# vim-marc
Plugin for transforming biblographic records in MarcEdit .mrk format to [marc21](https://www.loc.gov/marc/bibliographic/) .mrc records.

[![asciicast](https://asciinema.org/a/MgUA593GNoz1tHGAO1euIJ2oF.svg)](https://asciinema.org/a/MgUA593GNoz1tHGAO1euIJ2oF?autoplay=1&loop=1&speed=2)

## Documentation
To view the documentation in vim type `:help vim-marc`
If the documentation is not loading, compile help tags file `:helptags ALL`

## Usage
Typing `:MrcCompile` in VIM ex-mode will cause a .mrc file to be converted
to .mrk format.
Typing `:MrcDisplay` in VIM ex-mode will cause a .mrk file to be converted
to the .mrc format.

### Hot keys
Hot keys for the functions can be mapped in your VIM configuration file
which is `.vimrc` on Linux/Unix or `vimrc` on Windows.

For example, to map the `MrcCompile` function to the Ctrl+k hotkey and the
`MrcDisplay` function to Ctrl+l add the following to your VIMRC:
```
map <C-k> :MrcCompile<CR>
map <C-l> :MrcDisplay<CR>
```

### Notes on syntax highlighting
VIM has a maximum # of characters per line that it can highlight be default.
This value is 3000. If you have a long .mrc record, or multiple records in a
single .mrc file you may hit the line highlighting limit. To remove the limit
add set smc=0 to your vimrc file. Warning: this may add redraw delay.
Alternatively set it to a large value of your choice (e.g. 10000). For more
details on smc type :help smc.
