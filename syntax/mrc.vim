" Name: vim-marc
" Description: syntax highlight for .mrc files
" Authors: Michael Doyle & Miglena Minkova
" Date: June 16, 2019
"
" Refer to :help digraph-table for more details on the character encoding
" \%x1e = MrcField = RECORD SEPERATOR
" \%x1d = MrcRecord = GROUP SEPERATOR
" \%x1f = MrcSubfield = UNIT SEPERATOR
"
" VIM has a maximum # of characters per line that it can highlight be default.
" This value is 3000. If you have a long record, or multiple records in a
" single .mrc file you may hit the highlighting limit. To remove the limit add
" set smc=0 to your vimrc file. Warning: this may add redraw delay.
" Alternatively set it to a large value of your choice (e.g. 10000). For more
" details on smc type :help smc.
"
"" Refer to :help usr_44.txt for more details on syntax highlighting
"
"" Define Highlight Groups
syntax region MrcRecord start=/\d\{5}\w\{3}[ a]a22\d\{5}\p\{3}4500/ matchgroup=MrcGroup end=/\%x1d/ contains=MrcDir,MrcField,MrcSubfield
syntax region MrcDir matchgroup=MrcLDR start=/\d\{5}\w\{3}[ a]a22\d\{5}\p\{3}4500/ matchgroup=MrcField end=/\%x1e/ contained
syntax match MrcField /\%x1e/ contained
syntax region MrcSubfield start=/\%x1f/ matchgroup=MrcSubfieldTag end=/\w/ contained
"" Colour groups
highlight link MrcDir Statement
highlight link MrcSubfield Statement

highlight link MrcSubfieldTag Keyword
highlight link MrcField Number
highlight link MrcRecord String

highlight link MrcGroup Identifier
highlight link MrcLDR Identifier
