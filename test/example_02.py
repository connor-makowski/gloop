# Blink
import gloop


################### DATA ######################
# Transportation data
transport = [
    {
        "origin_name": "A1",
        "destination_name": "R1",
        "distance": 105,
        "cost_per_mile": 0.12,
    },
    {
        "origin_name": "A1",
        "destination_name": "R2",
        "distance": 256,
        "cost_per_mile": 0.12,
    },
    {
        "origin_name": "A1",
        "destination_name": "R3",
        "distance": 108,
        "cost_per_mile": 0.12,
    },
    {
        "origin_name": "A2",
        "destination_name": "R1",
        "distance": 240,
        "cost_per_mile": 0.12,
    },
    {
        "origin_name": "A2",
        "destination_name": "R2",
        "distance": 136,
        "cost_per_mile": 0.12,
    },
    {
        "origin_name": "A2",
        "destination_name": "R3",
        "distance": 198,
        "cost_per_mile": 0.12,
    },
]

# Loop through the transport data to create variable and calculate cost
for t in transport:
    # Create decision variables for each item in transport
    t["amt"] = gloop.Variable(
        name=f"{t['origin_name']}__{t['destination_name']}__amt", lowBound=0
    )
    # Calculate the variable cost of shipping for each item in tranport
    t["cost"] = t["distance"] * t["cost_per_mile"]


# Demand data
demand = [
    {"name": "R1", "demand": 2500},
    {"name": "R2", "demand": 4350},
    {"name": "R3", "demand": 3296},
]


################### Model #####################
# Initialize the model
my_model = gloop.Model(name="transportation_example", sense="minimize")


# Add the Objective Fn
my_model.add_objective(fn=gloop.Sum([t["amt"] * t["cost"] for t in transport]))

# Add Constraints
## Demand Constraint
for d in demand:
    my_model.add_constraint(
        name=f"{d['name']}__demand",
        fn=gloop.Sum(
            [t["amt"] for t in transport if t["destination_name"] == d["name"]]
        )
        >= d["demand"],
    )

# Solve the model
my_model.solve()

################### OUTPUT #####################

# Show the outputs
# my_model.show_outputs() #=>
# {'objective': 145208.16,
#  'status': 'Optimal',
#  'variables': {'A1__R1__amt': 2500.0,
#                'A1__R2__amt': 0.0,
#                'A1__R3__amt': 3296.0,
#                'A2__R1__amt': 0.0,
#                'A2__R2__amt': 4350.0,
#                'A2__R3__amt': 0.0}}
