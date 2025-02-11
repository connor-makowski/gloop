import pulp, type_enforced
from .Variable import Variable


@type_enforced.Enforcer
def Sum(
    vector: list[
        Variable | pulp.LpVariable | pulp.LpAffineExpression | int | float
    ],
):
    """
    Creates a Sum object to be used in an gloop.Model object.

    Requires:

    - `vector`:
        - Type: list of Variable objects, pulp.LpVariable objects, pulp.LpAffineExpression objects, ints, or floats
        - What: A vector of items (Variables) to sum together
    """
    return pulp.lpSum(vector)
