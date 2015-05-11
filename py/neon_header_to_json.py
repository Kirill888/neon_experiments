#!/usr/bin/env python

from collections import namedtuple

Arg  = namedtuple('Arg','name t')
Func = namedtuple('Func','name result_type args')

def clang_init(lib_path = '/usr/lib/llvm-3.6/lib/libclang.so.1'):
    try:
        import clang
        import clang.cindex

        clang.cindex.Config.set_library_file(lib_path)

        return clang.cindex.Index.create()
    except:
        return None


def traverse(cursor, func, level = 0):
    func(cursor, level)
    for c in cursor.get_children():
        traverse(c,func, level+1)

def dump_tree(cursor):
    def printer(c, lvl):
        pp = " "*lvl
        print(pp, c.kind, c.displayname)

    traverse(cursor, printer)


def describe_type(t):
    return t.spelling


def describe_func(c, skip_arg_names = False):
    from clang.cindex import CursorKind

    assert(c.kind == CursorKind.FUNCTION_DECL)

    if skip_arg_names:
        args = [describe_type(x.type) for x in c.get_arguments()]
    else:
        args = [ Arg(name=x.spelling, t=describe_type(x.type) ) for x in c.get_arguments() ]

    return Func(name=c.spelling,
                result_type=describe_type(c.result_type),
                args=args)


def collect_funcs(cursor, skip_arg_names=False):
    from clang.cindex import CursorKind
    dd = []

    def proc(c, level):
        if c.kind == CursorKind.FUNCTION_DECL:
           dd.append(describe_func(c, skip_arg_names))

    traverse(cursor, proc)

    return dd


if __name__ == '__main__':
    import json
    import sys

    clang_args='--target=armv7-linux-gnueabihf -mfpu=neon -I/usr/arm-linux-gnueabi/include/'.split(' ')

    index = clang_init()

    if index == None:
        print("Failed to init clang library is it installed?")
        sys.exit(1)

    tu = index.parse('t.c',
                     args=clang_args,
                     unsaved_files=[('t.c','#include <arm_neon.h>')])

    dd = collect_funcs(tu.cursor, skip_arg_names=True)
    print(json.dumps(dd,indent=1))
    sys.exit(0)
