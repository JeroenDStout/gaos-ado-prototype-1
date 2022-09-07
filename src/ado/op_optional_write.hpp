#include "op_optional_write_def.h"

#include <cmath>


template<typename call_data>
void ado_gen::optional_write::op_set_with_threshold::exec(call_data& d)
{
    auto tar = target.read(d);

    if (std::abs(current.read(d) - tar) > threshold.read(d))
      result.write(d, tar);
}