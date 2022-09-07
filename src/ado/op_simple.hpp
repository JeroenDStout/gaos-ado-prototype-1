#include "op_simple_def.h"

#include <cmath>


template<typename call_data>
void ado_gen::simple::op_add::exec(call_data& d)
{
    result.write(d, lh.read(d) + rh.read(d));
}


template<typename call_data>
void ado_gen::simple::op_sub::exec(call_data& d)
{
    result.write(d, lh.read(d) - rh.read(d));
}


template<typename call_data>
void ado_gen::simple::op_mul::exec(call_data& d)
{
    result.write(d, lh.read(d) * rh.read(d));
}


template<typename call_data>
void ado_gen::simple::op_div::exec(call_data& d)
{
    result.write(d, lh.read(d) / rh.read(d));
}


template<typename call_data>
void ado_gen::simple::op_diff::exec(call_data& d)
{
    result.write(d, std::abs(lh.read(d) - rh.read(d)));
}