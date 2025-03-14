# syntax = docker/dockerfile:1

## Uncomment the version of python you want to test against
# FROM python:3.11-slim
# FROM python:3.12-slim
FROM python:3.13-slim
# FROM python:3.14-rc-slim

# Set the working directory to /app
WORKDIR /app/

# Install the GLPK solver for testing alternative solvers
RUN apt update
RUN apt install glpk-utils -y
ENV GLPK_SOLVER_PATH=/usr/bin/glpsol

# Copy and install the requirements
# This includes egg installing the gloop package
COPY gloop/__init__.py /app/gloop/__init__.py
COPY pyproject.toml /app/pyproject.toml
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Drop into a shell by default
CMD ["/bin/bash"]
