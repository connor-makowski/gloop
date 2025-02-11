import pulp

CAT_OPTIONS = ["Continuous", "Binary", "Integer"]
CAT_ALIAS_MAP = {
    "binary": "Binary",
    "bin": "Binary",
    "bool": "Binary",
    "int": "Integer",
    "integer": "Integer",
    "continuous": "Continuous",
    "cont": "Continuous",
    "real": "Continuous",
    "float": "Continuous",
}

SENSE_OPTIONS = ["maximize", "minimize"]
SENSE_ALIAS_MAP = {
    "max": pulp.LpMaximize,
    "maximize": pulp.LpMaximize,
    "min": pulp.LpMinimize,
    "minimize": pulp.LpMinimize,
}
