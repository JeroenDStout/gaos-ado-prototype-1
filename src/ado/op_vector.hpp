#include "op_vector_def.h"

#include <cmath>


template<typename call_data>
void ado_gen::vector::op_add::exec(call_data& d)
{
    result_x.write(d, lh_x.read(d) + rh_x.read(d));
    result_y.write(d, lh_y.read(d) + rh_y.read(d));
}