" =============================================================================
" File: handlers.vim
" Author: Yanfei Guo <yanf.guo at gmail.com>
" Last Modified: June 18, 2016
" License: MIT License
" based on original version by Shougo Matsushita <Shougo.Matsu at gmail.com>
" =============================================================================

function! chromatica#handlers#_init() abort
    augroup chromatica
        autocmd!
        autocmd BufEnter * call chromatica#handlers#_parse()
        autocmd InsertLeave * call chromatica#handlers#_delayed_parse()
        autocmd TextChanged * call chromatica#handlers#_delayed_parse()
        autocmd CursorMoved * call chromatica#handlers#_highlight()
        if get(g:, 'chromatica#responsive_mode', 0)
            autocmd TextChangedI * call chromatica#handlers#_delayed_parse()
        endif
    augroup END
endfunction

fun! chromatica#handlers#_highlight()
    if exists('b:chromatica_changedtick_old')
        if b:chromatica_changedtick_old >= b:changedtick
            return
        endif
    endif
    if !exists('b:highlight_tick')
        let b:highlight_tick = 0
    endif

    let b:highlight_tick = b:highlight_tick + 1

    if exists('g:chromatica#_channel_id')
        let context = chromatica#init#_context()
        silent! call rpcnotify(g:chromatica#_channel_id, 'chromatica_highlight', context)
    endif
endf

fun! chromatica#handlers#_parse()
    let b:chromatica_changedtick_old = b:changedtick
    if exists('g:chromatica#_channel_id')
        let context = chromatica#init#_context()
        silent! call rpcnotify(g:chromatica#_channel_id, 'chromatica_parse', context)
    endif
endf

fun! chromatica#handlers#_delayed_parse()
    let b:chromatica_changedtick_old = b:changedtick
    if exists('g:chromatica#_channel_id')
        let context = chromatica#init#_context()
        silent! call rpcnotify(g:chromatica#_channel_id, 'chromatica_delayed_parse', context)
    endif
endf

fun! chromatica#handlers#_print_highlight()
    if exists('g:chromatica#_channel_id')
        let context = chromatica#init#_context()
        silent! call rpcnotify(g:chromatica#_channel_id, 'chromatica_print_highlight', context)
    endif
endf

" vim: tw=120:foldmarker={{{,}}}:foldmethod=marker:
