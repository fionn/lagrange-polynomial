DIR = lagrange_polynomial
SRC = $(DIR)/
TEST = test.py

.PHONY: install
install: $(SRC)
	@pip install --user --no-deps .

.PHONY: install_dev
install_dev:
	@pip install -e .[dev]

build: $(SRC)
	@python -m build

tags: $(SRC) $(TEST)
	@ctags --languages=python --python-kinds=-i $(SRC) $(TEST)

.PHONY: test
test:
	@python -m unittest

coverage: $(SRC) $(TEST)
	@coverage run --source=. --branch --concurrency=thread $(TEST)
	@coverage report -m
	@coverage html -d ./coverage
	@coverage erase

.PHONY: lint
lint:
	@pylint -f colorized $(SRC) $(TEST)

.PHONY: typecheck
typecheck:
	@mypy $(SRC) $(TEST)

.PHONY: clean
clean:
	@$(RM) -r coverage
	@$(RM) -r .mypy_cache
	@$(RM) -r __pycache__
	@$(RM) -r dist
	@$(RM) tags
