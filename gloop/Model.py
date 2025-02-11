import pulp, type_enforced
from pprint import pprint
from .__constants__ import SENSE_ALIAS_MAP, SENSE_OPTIONS
from .__helpers__ import Error
from .Variable import Variable
from .Sum import Sum


@type_enforced.Enforcer
class Model(Error):
    def __init__(self, name: str, sense: [str, None]):
        """
        Initialize a new optimization model object.

        Requires:

        - `name`:
            - Type: str
            - What: The name of this optimization model
        - `sense`:
            - Type: str
            - What: The type of optimization to perform
            - Options: ['maximize','minimize',None]
            - Note: If None, no optimization is performed, but a feasible solution is searched for given the constraints
            - Note: This is cleaned such that common aliases are accepted. An error is thrown if the sense is not recognized.
        """
        # Standard attributes
        self.__name__ = name
        self.__sense__ = self.__sense_cleaner__(sense)
        self.outputs = {"status": "Not Solved"}

        # Validation Attributes
        self.__solved__ = False
        self.__objective_added__ = self.__sense__ is None

        # Create PuLP Model
        __model_kwargs__ = {"name": self.__name__}
        if self.__sense__ != None:
            __model_kwargs__["sense"] = self.__sense__
        self.model = pulp.LpProblem(**__model_kwargs__)

    def add_objective(self, fn):
        """
        Add the objective function to the current model object. Each model can only have one objective function.

        Requires:

        - `fn`:
            - Type: function
            - What: The pythonic version of the objective function
            - Note: This function should **not** have any pythonic [comparison operators](https://docs.python.org/3/reference/expressions.html#comparisons)
        """
        # Validity Checks
        if self.__objective_added__:
            if self.__sense__ == None:
                self.exception(
                    "Models with `sense=None` should not have an objective function."
                )
            else:
                self.exception(
                    "An objective function has already been added to this model."
                )
        if not isinstance(
            fn, (pulp.LpAffineExpression, pulp.LpVariable, Variable)
        ):
            self.exception(
                "The objective function is not properly configured, consult the documentation for more information on how to add an objective function."
            )

        # Add the objective function to the model
        self.model += fn

        # Update the __objective_added__ validation attribute
        self.__objective_added__ = True

    def add_constraint(self, fn, name: [str, None] = None):
        """
        Add a constraint function to the current model object. Each model can have unlimited constraints.

        Requires:

        - `fn`:
            - Type: function
            - What: The pythonic version of a constraint function
            - Note: This function should have pythonic [comparison operators](https://docs.python.org/3/reference/expressions.html#comparison)

        Optional:

        - `name`:
            - Type: str
            - What: The name of this constraint
            - Default: None


        """
        # Validity Checks
        if not self.__objective_added__:
            self.exception(
                "An objective function should be added to this model before adding constraints."
            )
        if self.__solved__:
            self.exception(
                "This model has already been solved. You can not add any more constraints."
            )
        if not isinstance(fn, pulp.LpConstraint):
            self.exception(
                f"This constraint (Name:{name}) function is not properly configured, consult the documentation for more information on how to add constraints."
            )

        # Add the constraint to the model
        if name != None:
            self.model += (fn, name)
        else:
            self.model += fn

    def solve(
        self,
        solver: str = "PULP_CBC_CMD",
        solver_path: str = "",
        solver_kwargs: dict = {},
        warm_start: bool = False,
        pulp_log: bool = False,
        except_on_infeasible: bool = True,
        get_duals: bool = False,
        get_slacks: bool = False,
    ):
        """
        Solve the current model object.

        Optional:

        - `solver`:
            - Type: str
            - What: The solver to use for this optimization model
            - Default: 'PULP_CBC_CMD'
        - `solver_path`:
            - Type: str
            - What: The path to the solver to use for this optimization model
            - Default: Empty String
            - Note: This is only necessary if pulp is not able to find your solver location. For many solvers, this is not necessary.
        - `solver_kwargs`:
            - Type: dict
            - What: A dictionary of keyword arguments to pass to the solver
            - Default: {}
            - Note: This can be used to pass additional arguments to the solver
            - EG: `solver_kwargs={'msg': 3, 'timeLimit':10}` would set the solver to log all messages and have a time limit of 10 seconds
        - `warm_start`:
            - Type: bool
            - What: A flag to indicate if the solver should use the initial values of the variables
            - Default: False
        - `pulp_log`:
            - Type: bool
            - What: A flag to indicate if the relevant pulp / coinOr solver log should be logged in the console. This can be helpful for debugging.
            - Default: False
        - `except_on_infeasible`:
            - Type: bool
            - What: A flag to indicate if the model should throw an exception if the optimization model is infeasible. If false, the model will automatically relax constraints to generate an infeasible solution.
            - Default: True
        - `get_duals`:
            - Type: bool
            - What: A flag to indicate if the dual values for constraints should be added to the normal `outputs`.
            - Default: False
            - Note: Dual values will be None for solvers that do not support them
        - `get_slacks`:
            - Type: bool
            - What: A flag to indicate if the slack values for constraints should be added to the normal `outputs`.
            - Default: False
            - Note: Slack values will be None for solvers that do not support them
        """
        # Check the model validity
        self.__validity_checks__()
        # Simplified messaging logging
        if "msg" not in solver_kwargs:
            solver_kwargs["msg"] = 3 if pulp_log else 0
        # Warm Start
        if "warmStart" not in solver_kwargs and warm_start:
            solver_kwargs["warmStart"] = warm_start
        # Generic path for solver
        if solver_path != "":
            solver_kwargs["path"] = solver_path
        # Check to see if the solver is available
        if not hasattr(pulp, solver):
            self.exception(
                f"The solver {solver} is not available. Use Model.show_solvers() to see available solvers."
            )
        # Solve the model
        self.model.solve(pulp.getSolver(solver, **solver_kwargs))

        # Check if the model is infeasible
        if self.model.status == -1:
            if except_on_infeasible:
                self.exception(
                    "The current model is infeasible and can not be solved."
                )
            else:
                self.warn(
                    "The current model is infeasible and can not be solved. Constraints have been relaxed to provide a solution anyway."
                )
        self.__solved__ = True
        self.outputs = {
            "status": f"{pulp.LpStatus[self.model.status]}",
            "objective": (
                self.model.objective.value() if self.__sense__ != None else None
            ),
            "variables": {i.name: i.value() for i in self.model.variables()},
        }
        if get_duals:
            self.get_duals()
        if get_slacks:
            self.get_slacks()

    def get_slacks(self):
        """
        Adds slack values to the model outputs dictionary as `slacks` and also returns those slack values as an dictonary.

        Notes:

            - The model must be solved before this method can be used
            - Slack values might not be avaialable depending on the solver that is used
        """
        if not self.__solved__:
            self.exception(
                "The current model must be solved before getting slacks."
            )
        self.outputs["slacks"] = {
            key: value.slack for key, value in self.model.constraints.items()
        }
        return self.outputs["slacks"]

    def get_duals(self):
        """
        Adds dual values to the model outputs dictionary as `duals` and also returns those dual values as an dictonary.

        Notes:

            - The model must be solved before this method can be used
            - Dual values will be 0 or None for non LP models (EG MILPs)
            - Dual values might not be avaialable depending on the solver that is used
        """
        if not self.__solved__:
            self.exception(
                "The current model must be solved before getting duals."
            )
        self.outputs["duals"] = {
            key: value.pi for key, value in self.model.constraints.items()
        }
        return self.outputs["duals"]

    def get_model(self):
        """
        Returns the current model object.

        Note: This is a PuLP model object.
        """
        return self.model

    def get_formulation(self):
        """
        Returns the current model formulation as a string in a human readable form.

        Note: This aggregates variables where possible such that

        - `variable_1*2 + variable_1*1` => `variable_1*3`
        """
        return str(self.model)

    def show_formulation(self):
        """
        Shows the current model's formulation in the terminal (from self.get_formulation())
        """
        print(self.get_formulation())

    def get_outputs(self):
        """
        Returns a solved model's outputs.

        Note: A model must be solved before getting these outputs
        """
        if not self.__solved__:
            self.exception(
                "The current model must be solved before getting outputs."
            )
        return self.outputs

    def show_outputs(self, pretty=True):
        """
        Shows a solved model's outputs in the terminal (from self.get_outputs())

        Optional:

            - `pretty`:
                - Type: bool
                - What: Show the outputs in a pretty format
                - Default: True
        """
        outputs = self.get_outputs()
        if pretty:
            pprint(outputs)
        else:
            print(outputs)

    # Static Methods
    @staticmethod
    def variable(**kwargs):
        """
        A staticmethod to create a gloop.Variable.

        Returns a Variable object to be used in an gloop.Model object.

        See gloop.Variable for more information.
        """
        return Variable(**kwargs)

    @staticmethod
    def sum(vector: list):
        """
        A staticmethod to create a gloop.utils.Sum that is included for backwards compatability.

        Returns a Sum function to be used in an gloop.Model object.

        See gloop.Sum for more information.
        """
        return Sum(vector)

    @staticmethod
    def get_solvers(available: bool = True, show: bool = True):
        """
        Gets solvers that can be used.

        Optional:

        - `available`:
            - Type: bool
            - What: A flag to indicate if only available solvers should be shown
            - Default: True
        - `show`:
            - Type: bool
            - What: A flag to indicate if the solvers should be printed in the console
            - Default: True
        """
        return pulp.listSolvers(onlyAvailable=available)

    @staticmethod
    def show_solvers(available: bool = True, pretty: bool = True):
        """
        Shows solvers that can be used.

        Optional:

        - `available`:
            - Type: bool
            - What: A flag to indicate if only available solvers should be shown
            - Default: True
        """
        if pretty:
            pprint(Model.get_solvers(available=available))
        else:
            print(Model.get_solvers(available=available))

    # Utility Methods
    def __validity_checks__(self):
        """
        Runs validity checks on the model before solving it

        - Checks to make sure the model has not already been solved
        - Ensures that variables each have unique names
        - Note: PuLP automatically verifies constraint name uniqueness
        """
        # Ensure model is not solved
        if self.__solved__:
            self.exception(
                "This model has already been solved. You can not add any more constraints."
            )
        # Ensure Variable Names are Unique
        variable_names = [i.name for i in self.model.variables()]
        if len(set(variable_names)) < len(variable_names):
            self.exception("Overlapping variable names exist in the model.")

    def __sense_cleaner__(self, sense):
        """
        Cleans a passed sense to ensure it is valid and return the appropriate PuLP sense.
        """
        if sense is not None:
            sense = SENSE_ALIAS_MAP.get(sense.lower(), "Invalid")
            if sense == "Invalid":
                self.exception(
                    f"Sense '{sense}' is not a valid sense. Please use one of the following: {SENSE_OPTIONS}"
                )
        return sense
