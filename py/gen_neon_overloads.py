#!/usr/bin/env python

from __future__ import print_function
from collections import namedtuple

Func = namedtuple('Func','name result_type args')


suffixes = set('f32 u8 s8 p8 u16 s16 p16 u32 s32 p32 u64 s64 p64'.split(' '))

arg_names = 'a b c d e f g h j k'.split(' ')


def base_func_name(name):
    def unQ(s):
        if s[-1] == 'q': return s[:-1]
        return s

    return '_'.join([unQ(s) for s in name.split('_') if not s in suffixes])

def group_by_x(dd, get_key ):
    ''' Given a list of items and a key generation function,
        returns a dictionary of lists of items.
    '''
    ff = {}

    def register(k,v):
        if k in ff:
            ff[k].append(v)
        else:
            ff[k] = [v]

    for d in dd:
        register( get_key(d), d)

    return ff

def group_by_name(dd):
    return group_by_x(dd, lambda d: base_func_name(d.name))

def full_sig(f):
    return arg_sig(f) + ' -> ' + f.result_type

def arg_sig(f):
    return ' -> '.join(f.args)

def has_overload_clash(ff):
    ''' Given a group of functions with the same "base" name
        returns True if any two functions or more in the set
        share the same input signature (return types might differ)
    '''
    sigs = set([arg_sig(f) for f in ff])
    return len(sigs) < len(ff)

def has_type_clash(ff):
    ''' Given a group of functions with the same "base" name
        returns True if any two functions or more in the set
        share exactly the same signature including return types
    '''
    sigs = set([full_sig(f) for f in ff])
    return len(sigs) < len(ff)

def has_imm_args(f):
    ''' Returns True if function has immediate argument.
        Currently assumes last 'const int' arguments is an immediate
    '''

    if type(f) == list: #Group
        return has_imm_args(f[0])

    if len(f.args) > 1 and f.args[-1] == 'const int':
        return True
    return False


def render_cpp(cpp_name, f, tpl):
    import cpp_render
    args = [{'type':t, 'name':n} for t,n in zip(f.args, arg_names)]
    return cpp_render.render(tpl, cpp_name=cpp_name, args=args, c_name=f.name, result_type=f.result_type)



def render_group(cpp_name, funcs, tpl):
    return '\n'.join([render_cpp(cpp_name, f, tpl) for f in funcs])


def render_template_decl(cpp_name, funcs, tpl):
    gg = group_by_x(funcs, arg_sig)
    return '\n'.join( render_cpp(cpp_name, g[0], tpl) for g in gg.values() )


def load_hdr_data(json_file):
    try:
        import simplejson as json
    except ImportError:
        import json

    def to_func(d):
        n,r,a = d[:3]
        return Func(name=n, result_type=r, args=tuple(a))

    with open(json_file,'r') as f:
        return [to_func(d) for d in json.load(f)]

def strip_last_arg(ff):
    def strip(f):
        return Func(name=f.name, result_type=f.result_type, args=f.args[:-1])

    return [ strip(f) for f in ff ]

if __name__ == '__main__':
    import sys

    def msg(*objs):
        print(*objs, file=sys.stderr)

    def dump(*objs):
        print(*objs, file=sys.stdout)

    json_file = 'neon_header.json'

    msg('Loading json file: %s'%(json_file))
    dd = load_hdr_data(json_file)
    msg('Loaded %d functions\n'%(len(dd) ))

    ff = group_by_name(dd)
    msg('Found %d function groups'%(len(ff)))

    clash_data = [ (k,has_overload_clash(v), has_type_clash(v), has_imm_args(v) ) for k,v in ff.iteritems() ]


    f_simple   = sorted( n for (n,c,_ , imm) in clash_data if c == False and imm == False)
    f_tpl      = sorted( n for (n,c,tc, imm) in clash_data if c == True and tc == False and imm == False)
    f_bad      = sorted( n for (n,_,tc, _  ) in clash_data if tc == True )

    f_imm      = sorted( n for (n,c,_ , imm) in clash_data if c == False and imm == True)
    f_tpl_imm  = sorted( n for (n,c,tc, imm) in clash_data if c == True and tc == False and imm == True)


    msg('Of that\n  %4d groups can be trivially overloaded in C++'%(len(f_simple)))
    msg('  %4d groups will be templated on return type'%(len(f_tpl)))
    msg('  %4d groups will be templated due to use of immediate arg'%(len(f_imm)))
    msg('  %4d groups will be templated on return type and immediate arg'%(len(f_tpl_imm)))


    if len(f_bad) > 0:
        msg('Found %d bad groups that have clashing types'%(len(f_bad)))

    dump('#include <arm_neon.h>')

    #do template declarations first
    for n in f_tpl:
        s = render_template_decl(n, ff[n], 'tpl_decl')
        dump('\n\n//%s'%(n))
        dump(s)

    #do template declarations first
    for n in f_tpl_imm:
        s = render_template_decl(n, strip_last_arg(ff[n]), 'tpl_decl_imm')
        dump('\n\n//%s'%(n))
        dump(s)

    #do template specialisations
    for n in f_tpl:
        s = render_group(n, ff[n], 'tpl_inst')
        dump('\n\n//%s'%(n))
        dump(s)

    #do template specialisations
    for n in f_tpl_imm:
        s = render_group(n, strip_last_arg(ff[n]), 'tpl_inst_imm')
        dump('\n\n//%s'%(n))
        dump(s)

    for n in f_imm:
        s = render_template_decl(n, strip_last_arg(ff[n]), 'basic_imm')
        dump('\n\n//%s'%(n))
        dump(s)

    # do vanila overloads
    for n in f_simple:
        s = render_group(n, ff[n], 'basic')
        dump('\n\n//%s'%(n))
        dump(s)
