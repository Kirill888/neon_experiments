

def _init():
    common_macros = '''
{%- macro m_comma(loop) -%}
{% if not loop.last %}, {% endif %}
{%- endmacro -%}

{%- macro arg_list(args) -%}
  {%- for v in args -%}
   {{v.type}} {{v.name}}{{m_comma(loop)}}
  {%- endfor %}
{%- endmacro -%}

{%- macro args_call(args) -%}
  {{args | join(', ', 'name')}}
{%- endmacro -%}
'''

    cpp_tpls = {
    'basic'        :'static inline __attribute__((always_inline)) {{result_type}} {{cpp_name}}({{arg_list(args)}}){ return {{c_name}}({{args_call(args)}}); }',
    'basic_imm'    :'template<int I> inline __attribute__((always_inline)) {{result_type}} {{cpp_name}}({{arg_list(args)}}){ return {{c_name}}({{args_call(args)}}, I); }',
    'tpl_decl'     :'template<typename R> R {{cpp_name}}({{arg_list(args)}});',
    'tpl_decl_imm' :'template<typename R, int I> R {{cpp_name}}({{arg_list(args)}});',
    'tpl_inst'     :'template<> inline __attribute__((always_inline)) {{result_type}} {{cpp_name}}<{{result_type}}>({{arg_list(args)}}){ return {{c_name}}({{args_call(args)}}); }',
    'tpl_inst_imm' :'template<int I> inline __attribute__((always_inline)) {{result_type}} {{cpp_name}}({{arg_list(args)}}){ return {{c_name}}({{args_call(args)}}, I); };'
    }


    import jinja2
    return dict( (k,jinja2.Template(common_macros + t)) for k,t in cpp_tpls.iteritems() )


_tpls = _init()

def render(tpl_name, **kwargs):
    return _tpls[tpl_name].render(**kwargs)


if __name__ == '__main__':
    vv = [{'name':n, 'type':t} for n,t in zip('a b c d'.split(' '), 'int char float double'.split(' ')) ]


    for k in _tpls.keys():
        print(render(k, args=vv, cpp_name='foo', c_name='foo_i32', result_type='int8'))



