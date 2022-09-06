#include "op_vector_def.h"

#include <cmath>


template<typename t>
void ado_gen::vector::op_add<t>::exec(call_data& data)
{
    data.result_x_write(data.lh_x_read() + data.rh_x_read());
    data.result_y_write(data.lh_y_read() + data.rh_y_read());
}