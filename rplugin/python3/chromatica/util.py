# ============================================================================
# FILE: util.py
# AUTHOR: Yanfei Guo <yanf.guo at gmail.com>
# License: MIT license
# based on original version by Shougo Matsushita <Shougo.Matsu at gmail.com>
# ============================================================================

import json
import re
import os
import sys
import unicodedata
import glob
import subprocess
import pynvim

util_vim = None

def use_vim(vim):
    util_vim = vim

def set_default(var, val):
    return util_vim.call('chromatica#util#set_default', var, val)

def globruntime(runtimepath, path):
    ret = []
    for rtp in re.split(',', runtimepath):
        ret += glob.glob(rtp + '/' + path)
    return ret

def get_lineno(expr):
    return util_vim.call('line', expr)

def echo(expr):
    if hasattr(util_vim, 'out_write'):
        string = (expr if isinstance(expr, str) else str(expr))
        return util_vim.out_write('[chromatica] ' + string + '\n')
    else:
        util_vim.command("echo '%s'" % expr)

def echomsg(expr):
    if hasattr(util_vim, 'out_write'):
        string = (expr if isinstance(expr, str) else str(expr))
        return util_vim.out_write('[chromatica] ' + string + '\n')
    else:
        util_vim.command("echomsg '%s'" % expr)

def debug(expr):
    if hasattr(util_vim, 'out_write'):
        string = (expr if isinstance(expr, str) else str(expr))
        return util_vim.out_write('[chromatica] ' + string + '\n')
    else:
        util_vim.call('chromatica#util#print_debug', expr)


def error(expr):
    if hasattr(util_vim, 'err_write'):
        string = (expr if isinstance(expr, str) else str(expr))
        return util_vim.err_write('[chromatica] ' + string + '\n')
    else:
        util_vim.call('chromatica#util#print_error', expr)


def error_tb(msg):
    for line in traceback.format_exc().splitlines():
        error(str(line))
    error('%s.  Use :messages for error details.' % msg)


def error_vim(msg):
    throwpoint = vim.eval('v:throwpoint')
    if throwpoint != '':
        error('v:throwpoint = ' + throwpoint)
    exception = vim.eval('v:exception')
    if exception != '':
        error('v:exception = ' + exception)
    error_tb(msg)

def load_external_module(file, module):
    current = os.path.dirname(os.path.abspath(file))
    module_dir = os.path.join(os.path.dirname(current), module)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

def run_external_tool(cmdline):
    cmd_args = cmdline.strip().split(" ")
    proc = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.stdout.read()

def get_libclang_info(libclang_path):
    if os.path.isfile(libclang_path) or os.path.islink(libclang_path):
        real_path = os.path.realpath(libclang_path)
        if os.path.basename(real_path) == "libclang.so":
            cmdline = "readelf -a -W " + real_path
            return run_external_tool(cmdline)
        elif os.path.basename(real_path) == "libclang.dylib":
            cmdline = "otool -L " + real_path
            return run_external_tool(cmdline)
        else:
            debug("Cannot get library info for %s" % libclang_path)
            return None
    else:
        error("libclang path is not a file or a symlink")
        return None

def get_clang_include_path(libclang_path):
    if os.path.isfile(libclang_path) or os.path.islink(libclang_path):
        bin_path = os.path.realpath("/usr/bin/env")
        cmd_args = [bin_path, "clang", "-v", "-E", "-x", "c++", "-"]
        try:
            proc = subprocess.Popen(cmd_args, \
                    stdin=subprocess.PIPE, \
                    stdout=subprocess.PIPE, \
                    stderr=subprocess.STDOUT)
            output = proc.communicate(input=b'')[0]
            return output
        except:
            error("Cannot get clang configuration")
    else:
        error("libclang path is not a file or a symlink")

    return None
