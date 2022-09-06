#include "op_optional_write_def.h"

#include <cmath>


template<typename t>
void ado_gen::optional_write::op_set_with_threshold<t>::exec(call_data& data)
{
    t::scalar target = data.target_read();

    if (std::abs(data.current_read() - target) > data.threshold_read())
      data.result_write(target);
}