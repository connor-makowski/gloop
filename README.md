# Gloop
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/gloop.svg)](https://badge.fury.io/py/gloop)
[![Github](https://img.shields.io/badge/--red?logo=github)](https://github.com/connor-makowski/gloop)
[![Documentation](https://img.shields.io/badge/-Docs-blue?logo=read-the-docs)](https://connor-makowski.github.io/gloop/index.html)


Generalized Linear Object Oriented Programming (GLOOP) as a simple pythonic interface for OOP access to [PULP](https://coin-or.github.io/pulp/). It features simple objects, helpful methods, and additional error checking that simplifies code and streamlines development.

Gloop also happens to be synonymous with the word "pulp" in the English language.

## Why use Gloop?
- **Simple**: Gloop is simple and easy to use.
- **Object Oriented**: Gloop is object oriented by design.
- **Error Checking**: Gloop has additional error checking to help you catch mistakes early.
    - This includes checking for duplicate names, invalid constraints, passed types, and more.
- **Intuitive**: Gloop is intuitive
- **Unique**: Gloops is unique in nature and can help you think differently about how you code for linear programming.

# Setup

```
pip install gloop
```

# Getting Started

`gloop` is a package designed for object oriented linear programming access to pulp. [Technical docs can be found here](https://connor-makowski.github.io/gloop/index.html).

## Bare Bones Example
```py
import gloop

# Create a variable
my_variable = gloop.Variable(name='my_variable_name', lowBound=0)

# Create a model
my_model = gloop.Model(name="my_model_name", sense="maximize")
# Add an objective for the model
my_model.add_objective(fn=my_variable)
# Add a constraint to the model
my_model.add_constraint(name="my_constraint_name", fn=my_variable <= 5)

# Solve the model
my_model.solve()

# Get the results
# my_model.show_outputs()
#=> {'status': 'Optimal', 'objective': 5.0, 'variables': {'my_variable_name': 5.0}}
```

## Example

<h2>Transportation Problem</h2>
<p>A product is manufactured in two assembly plants and sold in three regions. Monthly demand per region is shared in Table 1. Currently, assembly plants have no capacity restrictions and can source as many items as needed. Transportation costs (USD)0.12 per unit per mile.</p>
<p><b>Table 1: Demand in units</b></p>
<table width="90%">
<tbody>
<tr>
<td width="20%" style="text-align: center; border: 1px solid black;">Demand</td>
<td width="10%" style="text-align: center; border: 1px solid black;">Region 1</td>
<td width="10%" style="text-align: center; border: 1px solid black;">Region 2</td>
<td width="10%" style="text-align: center; border: 1px solid black;">Region 3</td>
</tr>
<tr>
<td width="15%" style="text-align: center; border: 1px solid black;">Units per month</td>
<td width="10%" style="text-align: center; border: 1px solid black;">2500</td>
<td width="10%" style="text-align: center; border: 1px solid black;">4350</td>
<td width="10%" style="text-align: center; border: 1px solid black;">3296</td>
</tr>
</tbody>
</table>
<p><b>Table 2: Distance in Miles</b></p>
<table width="90%" style="height: 76.7814px;">
<tbody>
<tr style="height: 25.5938px;">
<td width="15%" style="text-align: center; border: 1px solid black; height: 25.5938px;">Miles</td>
<td width="10%" style="text-align: center; border: 1px solid black; height: 25.5938px;">Region 1</td>
<td width="10%" style="text-align: center; border: 1px solid black; height: 25.5938px;">Region 2</td>
<td width="10%" style="text-align: center; border: 1px solid black; height: 25.5938px;">Region 3</td>
</tr>
<tr style="height: 25.5938px;">
<td width="15%" style="text-align: center; border: 1px solid black; height: 25.5938px;">Assembly Plant 1</td>
<td width="10%" style="text-align: center; border: 1px solid black; height: 25.5938px;">105</td>
<td width="10%" style="text-align: center; border: 1px solid black; height: 25.5938px;">256</td>
<td width="10%" style="text-align: center; border: 1px solid black; height: 25.5938px;">108</td>
</tr>
<tr style="height: 25.5938px;">
<td width="15%" style="text-align: center; border: 1px solid black; height: 25.5938px;">Assembly Plant 2</td>
<td width="10%" style="text-align: center; border: 1px solid black; height: 25.5938px;">240</td>
<td width="10%" style="text-align: center; border: 1px solid black; height: 25.5938px;">136</td>
<td width="10%" style="text-align: center; border: 1px solid black; height: 25.5938px;">198</td>
</tr>
</tbody>
</table>
<p></p>
<p><strong>Formulate a model using the available information. Your goal is to minimize the total transportation cost.</strong></p>

```py
# Transportation Problem
import gloop


################### DATA ######################
# Transportation data
transport = [
    {"origin_name": "A1", "destination_name": "R1", "distance": 105},
    {"origin_name": "A1", "destination_name": "R2", "distance": 256},
    {"origin_name": "A1", "destination_name": "R3", "distance": 108},
    {"origin_name": "A2", "destination_name": "R1", "distance": 240},
    {"origin_name": "A2", "destination_name": "R2", "distance": 136},
    {"origin_name": "A2", "destination_name": "R3", "distance": 198},
]

# Loop through the transport data to create variables and calculate cost
for t in transport:
    # Create decision variables for each item in transport
    t["amt"] = gloop.Variable(
        name=f"{t['origin_name']}__{t['destination_name']}__amt", lowBound=0
    )
    # Calculate the variable cost of shipping for each item in tranport
    t["cost"] = t["distance"] * 0.12


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
```
