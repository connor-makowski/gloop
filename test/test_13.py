import gloop

# Create variables
i1 = gloop.Variable(
    name="i1", cat="Binary", initialValue=0, fixInitialValue=True
)
i2 = gloop.Variable(name="i2", cat="Binary", initialValue=1)

# Initialize the model
model = gloop.Model(name="WarmStartTest", sense="maximize")

# Add the Objective Fn
model.add_objective(fn=i1 + i2)

model.add_constraint(name="c1", fn=i1 + i2 <= 1)

# Solve the model
model.solve(
    warm_start=True,
)

if (
    round(model.outputs.get("objective"), 2) != 1.00
    or round(model.outputs.get("variables").get("i1"), 2) != 0.00
):
    print("test_13.py failed")
