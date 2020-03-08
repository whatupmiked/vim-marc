# vim-marc
Plugin for converting MARC 21 bibliographic records between .mrc, .mrk and .xml file formats.

[![asciicast](https://asciinema.org/a/WGLMwpUtLvsx1jfQlbFGS2hgz.svg)](https://asciinema.org/a/WGLMwpUtLvsx1jfQlbFGS2hgz?autoplay=1&loop=1&speed=2)

## Formats
`vim-marc` converts between 3 standard formats:
- **.mrk** mnemonic text format native to [MarcEdit](https://marcedit.reeset.net/)'s MarcEditor, used for editing and displaying bibliographic records in a human readable format.
- **.mrc** [MARC 21](https://www.loc.gov/marc/bibliographic/) Machine Readable Cataloguing standard for bibliographic data using [ISO 2709:2008](https://www.iso.org/standard/41319.html).
- **.xml** XML format using the [Library of Congress MARC21 XML Schema](http://www.loc.gov/standards/marcxml/).

## Commands
`:Mrc21`        Converts to MARC 21 format, sets file type to .mrc  
`:MrcMrk`       Converts to mnemonic text format, sets file type to .mrk  
`:MrcXML`       Converts to MARC XML format, sets file type to .xml  
`:MrcCycle`     Cycles through MARC 21, Mnnemonic text format and MARC XML, sets file type respectively to .mrc, .mrk and .xml  

## Mappings
Hot keys for the above commands can created with the [map](http://vimdoc.sourceforge.net/htmldoc/map.html) command and added to your VIM configuration file .vimrc (Linux/Unix) or vimrc (Windows).

```
map <C-C> :Mrc21<CR>
map <C-K> :MrcMrk<CR>
map <C-X> :MrcXML<CR>
map <C-Y> :MrcCycle<CR>
```
These can be changed to a hot key of your choice.

**Note:** A list of predefined mode-specific mappings can be inserted in
`/plugin/vim-marc.vim`

## Syntax highlighting
`vim-marc` is packaged with syntax highlighting for .mrc and .mrk formats.
It uses the build-in .xml highlighting in vim.

Note: Vim has a maximum # of characters per line that it can highlight by default. This value is 3000. If you have a long record, or multiple records in a single .mrc file you may hit the highlighting limit.

To remove the limit add set smc=0 to your vimrc file.Warning: this may add redraw delay. Alternatively, set it to a large value of your choice (eg. 10000).

## Encoding
When converting between .mrk and .mrc, `vim-marc` enforces utf-8 character encoding in order to get the correct ASCII character length.

## Documentation
To view the documentation in vim type `:help vim-marc`
If the documentation is not loading, compile help tags file `:helptags ALL`

## Dependencies
Tested on Vim version 8.1 and Python version 3.5.2 or later.

## Contribution
Pull requests welcome!
Please feel free to rate the plugin on [vim.org](https://www.vim.org/scripts/script.php?script_id=5809) if you like it!

## License
[MIT License](https://opensource.org/licenses/MIT)
