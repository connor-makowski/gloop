from gloop import Model
import os

# Create variables
data = [
    {
        "name": "product_1",
        "input_1": 1,
        "input_2": 3,
        "profit": 1,
        "amt": Model.variable(name="product_1", lowBound=0),
    },
    {
        "name": "product_2",
        "input_1": 2,
        "input_2": 1,
        "profit": 1,
        "amt": Model.variable(name="product_2", lowBound=0),
    },
]

constraints = [
    {"name": "input_1", "max_amt": 100},
    {"name": "input_2", "max_amt": 200},
]

# Initialize the model
model = Model(name="Array_Problem", sense="maximize")


# Add the Objective Fn
model.add_objective(fn=Model.sum([i["amt"] * i["profit"] for i in data]))

# Add Constraints
for j in constraints:
    model.add_constraint(
        name=f'{j["name"]}_constraint',
        fn=Model.sum([i["amt"] * i[j["name"]] for i in data]) <= j["max_amt"],
    )

# Solve the model
model.solve(
    solver="GLPK_CMD",
    solver_path=os.environ.get("GLPK_SOLVER_PATH"),
    solver_kwargs={"timeLimit": 10},
    get_duals=True,
    get_slacks=True,
)

if round(model.outputs.get("objective"), 2) != 80.00:
    # Custom solver path is the only difference between test_10.py and test_11.py
    print("test_11.py failed")
