#include "op_simple_def.h"

#include <cmath>


template<typename t>
void ado_gen::simple::op_add<t>::exec(call_data& data)
{
    data.result_write(data.lh_read() + data.rh_read());
}


template<typename t>
void ado_gen::simple::op_sub<t>::exec(call_data& data)
{
    data.result_write(data.lh_read() - data.rh_read());
}


template<typename t>
void ado_gen::simple::op_mul<t>::exec(call_data& data)
{
    data.result_write(data.lh_read() * data.rh_read());
}


template<typename t>
void ado_gen::simple::op_div<t>::exec(call_data& data)
{
    data.result_write(data.lh_read() / data.rh_read());
}


template<typename t>
void ado_gen::simple::op_diff<t>::exec(call_data& data)
{
    data.result_write(std::abs(data.lh_read() - data.rh_read()));
}