import gloop

# Create a variable
my_variable = gloop.Variable(name="my_variable_name", lowBound=0)

# Create a model
my_model = gloop.Model(name="my_model_name", sense="maximize")
# Add an objective for the model
my_model.add_objective(fn=my_variable)
# Add a constraint to the model
my_model.add_constraint(name="my_constraint_name", fn=my_variable <= 5)

# Solve the model
my_model.solve()

# Show the results
# my_model.show_outputs()
# => {'status': 'Optimal', 'objective': 5.0, 'variables': {'my_variable_name': 5.0}}
