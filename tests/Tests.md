# Running Tests for The-AI-Engineer-Challenge

This project uses **pytest** for automated testing and also provides some test scripts that can be run directly with Python.

## 1. Running Pytest-based Tests

To run all tests in the `tests/` folder, use:

```bash
PYTHONPATH=. pytest tests/
```

- The `PYTHONPATH=.` ensures that the local `aimakerspace` package is found by the test runner.
- You must run this command from the project root directory.

To run a specific test file, for example `test_loaders_pytest.py`:

```bash
PYTHONPATH=. pytest tests/test_loaders_pytest.py
```

## 2. Running Individual Test Scripts

Some test scripts can be run directly with Python. For example:

```bash
python -m tests.test_docx_loader
python -m tests.test_markdown_loader
python -m tests.test_pdf_loader
```

This will print the loaded documents or test results to the terminal.

## 3. Troubleshooting

- If you see `ModuleNotFoundError: No module named 'aimakerspace'`, make sure to set `PYTHONPATH=.` and run from the project root.
- If you want to run all tests and see detailed output, add the `-v` flag:
  ```bash
  PYTHONPATH=. pytest -v tests/
  ```
- If you want to run a single test function, use:
  ```bash
  PYTHONPATH=. pytest tests/test_loaders_pytest.py -k test_function_name
  ```

## 4. Installing Pytest

If you do not have pytest installed, add it to your environment:

```bash
pip install pytest
```

---

**Summary:**
- Use `PYTHONPATH=. pytest tests/` to run all tests.
- Use `python -m tests.test_xxx_loader` to run individual test scripts.
- Always run commands from the project root. 