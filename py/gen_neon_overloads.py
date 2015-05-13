#!/usr/bin/env python

from __future__ import print_function
from string import Template

suffixes = set('f32 u8 s8 p8 u16 s16 p16 u32 s32 p32 u64 s64 p64'.split(' '))

arg_names = 'a b c d e f g h j k'.split(' ')
tpl_cpp_overload = Template('''static inline __attribute__((always_inline)) $result_type $cpp_name($args_decl){return $c_name($args);}''')
tpl_cpp_template_decl=Template('template<typename R> R $cpp_name($args_decl);')
tpl_cpp_templated_overload = Template('''template<> inline __attribute__((always_inline)) $result_type $cpp_name<$result_type>($args_decl){return $c_name($args);}''')


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




def render_cpp(cpp_name, f, tpl):
    arg_types = f.args
    args = [(t,n) for t,n in zip(arg_types, arg_names)]
    args_decl = ', '.join([ '%s %s'%(t,n)  for t,n in args ])
    args_list = ', '.join([n for _,n in args])

    return tpl.substitute(result_type=f.result_type,
                          cpp_name=cpp_name,
                          args_decl=args_decl,
                          args=args_list,
                          c_name=f.name )

def render_group(cpp_name, funcs, tpl):
    return '\n'.join([render_cpp(cpp_name, f, tpl) for f in funcs])


def render_template_decl(cpp_name, ff, tpl = tpl_cpp_template_decl):
    def render(g):
        args_decl = ','.join(g[0].args)
        return tpl.substitute(cpp_name=cpp_name, args_decl=args_decl)

    gg = group_by_x(ff, arg_sig)
    return '\n'.join(render(g) for g in gg.values())


def load_hdr_data(json_file):
    try:
        import simplejson as json
    except ImportError:
        import json

    def to_func(d):
        from collections import namedtuple
        Func = namedtuple('Func','name result_type args')

        n,r,a = d[:3]
        return Func(name=n, result_type=r, args=tuple(a))

    with open(json_file,'r') as f:
        return [to_func(d) for d in json.load(f)]


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

    clash_data = [ (k,has_overload_clash(v), has_type_clash(v)) for k,v in ff.iteritems() ]

    f_simple = sorted( n for (n,c,_ ) in clash_data if c == False )
    f_tpl    = sorted( n for (n,c,tc) in clash_data if c == True and tc == False )
    f_bad    = sorted( n for (n,_,tc) in clash_data if tc == True )

    msg('Of that\n  %4d groups can be trivially overloaded in C++'%(len(f_simple)))
    msg('  %4d groups will be templated on return type'%(len(f_tpl)))

    if len(f_bad) > 0:
        msg('Found %d bad groups that have clashing types'%(len(f_bad)))

    dump('#include <arm_neon.h>')

    #do template declarations first
    for n in f_tpl:
        dump('\n\n//%s'%(n))
        dump( render_template_decl(n, ff[n]) )

    #do template specialisations
    for n in f_tpl:
        s = render_group(n, ff[n], tpl_cpp_templated_overload)
        dump('\n\n//%s'%(n))
        dump(s)

    # do vanila overloads
    for n in f_simple:
        s = render_group(n, ff[n], tpl_cpp_overload)
        dump('\n\n//%s'%(n))
        dump(s)
