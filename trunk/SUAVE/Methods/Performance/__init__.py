## @defgroup Methods-Performance Performance
# This is a set of basic aircraft performance estimation functions. It
# includes field length and range calculations.
# @ingroup Methods

from .estimate_take_off_field_length   import estimate_take_off_field_length
from .payload_range                    import payload_range
from .estimate_landing_field_length    import estimate_landing_field_length
from .find_take_off_weight_given_tofl  import find_take_off_weight_given_tofl 
from .V_n_diagram                      import V_n_diagram
from .propeller_range_endurance_speeds import propeller_range_endurance_speeds, stall_speed

