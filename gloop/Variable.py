import pulp, type_enforced
from .__helpers__ import Error
from .__constants__ import CAT_OPTIONS, CAT_ALIAS_MAP


@type_enforced.Enforcer
class Variable(pulp.LpVariable, Error):
    """
    Creates a variable object to be used in an gloop.Model object.
    """

    def __init__(
        self,
        name: str,
        lowBound: [float, int, None] = None,
        upBound: [float, int, None] = None,
        cat: [str, None] = "Continuous",
        initialValue: [float, int, None] = None,
        fixInitialValue: bool = False,
    ):
        """
        Creates a variable object to be used in an gloop.Model object.

        Requires:

        - `name`:
            - Type: str
            - What: The name of this variable

        Optional:

        - `lowBound`:
            - Type: int | float
            - What: A lower bound for this variable
            - Default: -infinity
        - `upBound`:
            - Type: int | float
            - What: An upper bound for this variable
            - Default: infinity
        - `cat`:
            - Type: str
            - What: The category of this variable
            - Default: `Continuous`
            - Options: ['Continuous','Binary','Integer']
            - Note: This is cleaned such that common aliases are accepted. An error is thrown if the category is not recognized.
        - `initialValue`:
            - Type: int | float
            - What: The initial value of this variable to be used if `warm_start` is set to True
            - Default: None
            - Note: These are only used if `warm_start` is set to True for the solver.
        - `fixInitialValue`:
            - Type: bool
            - What: A flag to indicate if the initial value should be unchangeable
            - Default: False
            - Note: This is only used if an `initialValue` is set and `warm_start` is set to True for the solver.
        """
        self.name = name
        self.cat = self.__cat_cleaner__(cat)
        self.upBound = upBound
        self.lowBound = lowBound
        self.initialValue = initialValue
        self.fixInitialValue = fixInitialValue

        super_kwargs = {"name": name, "cat": cat}
        if lowBound is not None:
            super_kwargs["lowBound"] = lowBound
        if upBound is not None:
            super_kwargs["upBound"] = upBound

        # Initialize the pulp LpVariable
        super().__init__(**super_kwargs)

        # Follow up with any additional steps as needed
        if initialValue is not None:
            self.setInitialValue(initialValue)
            if fixInitialValue:
                self.fixValue()
        elif fixInitialValue:
            self.warn("Cannot fix initial value without an initial value.")

    def __cat_cleaner__(self, cat: str) -> str:
        """
        Cleans the category string to ensure it is one of the accepted values.

        Requires:

        - `cat`:
            - Type: str
            - What: The category of this variable
            - Options: ['Continuous','Binary','Integer']

        Returns:

        - `cat`:
            - Type: str
            - What: The cleaned category string
            - Default: 'Continuous
        """
        cat_item = CAT_ALIAS_MAP.get(cat.lower())
        if cat_item is None:
            self.exception(
                f"Category '{cat}' is not a valid category. Please use one of the following: {CAT_OPTIONS}"
            )
        return cat_item
