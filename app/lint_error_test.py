# This file intentionally has lint errors for CI testing
import    os      # Multiple spaces - E271
import sys

def bad_function(  ):  # E201, E202
    x=1+2  # E225
    return x
