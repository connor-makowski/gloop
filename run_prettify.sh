# Change to the script directory
cd $(dirname "$0")
# Lint and Autoformat the code in place
# Remove unused imports
autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports -r ./gloop
# Perform all other steps
black --config pyproject.toml ./gloop
black --config pyproject.toml ./test
