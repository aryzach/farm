filetype plugin indent on
syntax on

" spell checker
map <F5> :setlocal spell! spelllang=en_us<CR>

"remap 
:imap jj <Esc>

map e :set number!

"CtrlP"
set runtimepath^=~/.vim/pack/vendor/start/ctrlp.vim
"set runtimepath^=~/.vim/bundle/ctrlp.vim
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'
"CtrlP"
"new"
syntax on
set backspace=indent,eol,start
set nocp
set autoindent
set ignorecase
set smartcase

nnoremap <Left>  :echoe "Use h"<CR>
nnoremap <Right> :echoe "Use l"<CR>
nnoremap <Up>    :echoe "Use k"<CR>
nnoremap <Down>  :echoe "Use j"<CR>
" ...and in insert mode
inoremap <Left>  <ESC>:echoe "Use h"<CR>
inoremap <Right> <ESC>:echoe "Use l"<CR>
inoremap <Up>    <ESC>:echoe "Use k"<CR>
inoremap <Down>  <ESC>:echoe "Use j"<CR>
"new"
set number
set ma
filetype plugin indent on
"tabs to spaces
set expandtab
set shiftwidth=4
"On pressing tab, insert 2 spaces
"set expandtab
" " show existing tab with 2 spaces width
" set tabstop=2
" set softtabstop=2
" " when indenting with '>', use 2 spaces width
" set shiftwidth=2
