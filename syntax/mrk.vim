" Name: vim-marc
" Description: syntax highlighting for mrk file type
" Authors: Michael Doyle & Miglena Minkova
" Date: June 29, 2019
"
"" Refer to :help usr_44.txt for more details on syntax highlighting
"
"" Define Highlight Groups
syntax region MrcField start=/^=\(\d\{3}\)\@=/ end=/$/ contains=MrcDir,MrcSubField,MrcSubPunct,MrcEndPunct,MrcIndicator
syntax match MrcLDR /\c=LDR.*/
syntax match MrcDir /=\d\{3}/ contained
syntax match MrcSubField /\$\w/ contained
" used % as delimiter to match /
syntax match MrcSubPunct %\(:\|;\|,\|=\|/\)\(\$\w\)\@=% contained
syntax match MrcEndPunct /\.$/ contained
syntax match MrcIndicator /\(=\d\{3}\s\+\)\@<=\(\d\|\\\)\+/ contained
"" Define Colour Groups
highlight link MrcLDR Identifier
highlight link MrcField String
highlight link MrcDir Statement

highlight link MrcSubField Keyword
highlight link MrcSubPunct Keyword

highlight link MrcEndPunct Number
highlight link MrcIndicator Number
