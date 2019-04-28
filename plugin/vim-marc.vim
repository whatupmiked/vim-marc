"Tutorial Used
"candidtim.github.io/vim/2017/08/11/write-vim-plugin-in-python.html
if !has("python3")
    echo "VIM has to be compiled with +python3 for vim-marc to work"
    finish
endif

if exists('g:marc_plugin_loaded')
    finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import mmmarc
EOF

function! MrcCompile()
    py3 mmmarc.mrcCompile()
endfunction
command! -nargs=0 MrcCompile call MrcCompile()

function! MrcDisplay()
    py3 mmmarc.mrcDisplay()
endfunction
command! -nargs=0 MrcDisplay call MrcDisplay()

let g:marc_plugin_loaded = 1
