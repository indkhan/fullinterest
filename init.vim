" ================================
" Plugin Management with vim-plug
" ================================
call plug#begin('~/.vim/plugged')

" Basic Plugins
Plug 'http://github.com/tpope/vim-surround'         " Surrounding (ysw)
Plug 'https://github.com/tpope/vim-commentary'         " Commenting (gcc & gc)
Plug 'https://github.com/preservim/nerdtree'            " File manager (NERDTree)
Plug 'https://github.com/vim-airline/vim-airline'        " Status bar
Plug 'https://github.com/ryanoasis/vim-devicons'         " Developer Icons
Plug 'https://github.com/preservim/tagbar', {'on': 'TagbarToggle'} " Code structure navigation
Plug 'https://github.com/junegunn/fzf.vim'               " Fuzzy Finder (requires Silversearcher-ag for :Ag)
Plug 'https://github.com/junegunn/fzf'                  " Fuzzy finder core

" Color schemes and themes
Plug 'https://github.com/morhetz/gruvbox'
Plug 'https://github.com/vim-airline/vim-airline-themes'

" Utilities
Plug 'https://github.com/mbbill/undotree'               " Undo tree visualizer
Plug 'neoclide/coc.nvim', {'branch': 'release'}        " Intellisense engine
Plug 'https://github.com/lepture/vim-jinja'              " Jinja syntax highlighting
Plug 'https://github.com/tpope/vim-fugitive'             " Git integration
Plug 'https://github.com/matze/vim-move'                 " Moving lines/blocks easily
Plug 'voldikss/vim-floaterm'                             " Floating terminal
Plug 'vim-python/python-syntax'                        " Enhanced Python syntax highlighting
Plug 'alvan/vim-closetag'                              " Auto-close HTML/XML tags

" Additional Enhancements
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'} " Better syntax highlighting via tree-sitter
Plug 'folke/which-key.nvim'                              " Displays possible keybindings in a popup
Plug 'airblade/vim-gitgutter'                            " Git changes in the gutter

call plug#end()

" =====================================
" General Editor Settings & Enhancements
" =====================================

" Basic settings
set number                           " Show line numbers
set relativenumber                   " Relative line numbers
set mouse=a                          " Enable mouse support
set autoindent                       " Auto indent new lines
set tabstop=4                        " Tab width
set softtabstop=4
set shiftwidth=4                     " Indentation width
set smarttab
set encoding=UTF-8                   " Use UTF-8 encoding
set visualbell                       " Use visual bell instead of sound
set scrolloff=5                      " Keep 5 lines visible when scrolling

" Filetype detection and syntax
filetype plugin indent on
syntax on

" Persistent Undo: Retain undo history between sessions
if has("persistent_undo")
    set undofile
    set undodir=~/.vim/undodir
endif

" Search Enhancements
set incsearch                        " Incremental search
set hlsearch                         " Highlight search matches
set ignorecase                       " Ignore case when searching
set smartcase                        " Case-sensitive if uppercase is used

" Clipboard Integration (for Windows and others)
set clipboard=unnamedplus            " Use system clipboard

" Always show the sign column (for git signs, diagnostics, etc.)
set signcolumn=yes

" ======================
" NERDTree Configuration
" ======================
" Show hidden files (like .env) by default
let g:NERDTreeShowHidden = 1
" Customize folder arrows
let g:NERDTreeDirArrowExpandable = "+"
let g:NERDTreeDirArrowCollapsible = "~"
let g:python_highlight_all = 1

" Key mappings for NERDTree & UndoTree
nnoremap <C-f> :NERDTreeFocus<CR>
nnoremap <C-n> :NERDTree<CR>
nnoremap <C-t> :NERDTreeToggle<CR>
nnoremap <C-l> :UndotreeToggle<CR>

" =============================
" Vim Airline & Tagbar Settings
" =============================
let g:airline_powerline_fonts = 1
if !exists('g:airline_symbols')
    let g:airline_symbols = {}
endif
let g:bullets_enabled_file_types = ['markdown', 'text']
let g:airline_left_sep = ''
let g:airline_left_alt_sep = ''
let g:airline_right_sep = ''
let g:airline_right_alt_sep = ''
let g:airline_symbols.branch = ''
let g:airline_symbols.readonly = ''
let g:airline_symbols.linenr = ''

" Tagbar: Toggle code outline
nmap <F6> :TagbarToggle<CR>

" =======================
" CoC (Completion Engine)
" =======================
" Confirm completion if popup is visible; otherwise, insert a new line with an undo break.
inoremap <silent><expr> <CR> coc#pum#visible() ? coc#pum#confirm() : "\<C-g>u\<CR>"

" Use Tab and Shift-Tab for navigating the completion menu
inoremap <expr> <Tab> pumvisible() ? "\<C-N>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-P>" : "\<C-H>"

" ========================
" Floaterm & Other Mappings
" ========================
" Floaterm key mappings
let g:floaterm_keymap_new    = '<F7>'
let g:floaterm_keymap_prev   = '<F8>'
let g:floaterm_keymap_next   = '<F9>'
let g:floaterm_keymap_toggle = '<F12>'
" Save and run the current Python file in a new floaterm
nnoremap <F5> :w<CR>:FloatermNew --autoclose=0 python3 %<CR>

" Clear search highlighting
nnoremap <F3> :noh<CR>

" Disable middle mouse clicks to prevent accidental input
map <MiddleMouse> <Nop>
imap <MiddleMouse> <Nop>
map <2-MiddleMouse> <Nop>
imap <2-MiddleMouse> <Nop>
map <3-MiddleMouse> <Nop>
imap <3-MiddleMouse> <Nop>
map <4-MiddleMouse> <Nop>
imap <4-MiddleMouse> <Nop>

" ========================
" Window Navigation Mappings
" ========================
" Quickly move between split windows using Ctrl + h/j/k/l
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" =============================
" Translucent Background Setup
" =============================
" Instead of a fully transparent background, we set a dark background color.
" Adjust the hex color (#1e222a) to change the level of translucency; the terminal's own opacity settings will also affect this.
highlight Normal guibg=#1e222a
highlight NonText guibg=#1e222a
" Optionally, you can adjust ctermbg if needed:
highlight Normal ctermbg=none
highlight NonText ctermbg=none

" =============================
" Which-Key Plugin Configuration
" =============================
" Initialize which-key to display possible key bindings in a popup.
lua << EOF
require("which-key").setup {}
EOF

" =============================
" End of init.vim
" =============================

