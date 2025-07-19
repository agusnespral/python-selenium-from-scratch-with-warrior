# python-selenium-from-scratch-with-warrior

1. Create venv
py -m venv ven
2. Activate venv
\venv\Scripts> .\activate (PowerShell) or source ./activate (bash)
3. Create requirements.txt and add main dependencies
4. Install dependencies
pip install -r requirements.txt
5. Create .env for credentials (python-dotenv dependency already installed on p4)
6. Install ruff (Ultra-fast Python linter to check code quality and style)
7. Install pre-commit (Framework to manage Git hooks for running tasks before 
commits), create .pre-commit-config.yaml and run pre-commit install
8. Install PyYAML (Library to parse and write YAML files, commonly used for configs)
9. Create config.yml (YML helper) for browser config
10. conftest.py
10. Create browser_driver_helper.py and add to conftest.py
11. Create logger_helper.py and add to conftest.py
12. Install allure-pytest (Generate Allure reports)
    add pytest.ini `addopts = --alluredir=allure-results` for generating Allure reports
    Generate the report:
    allure serve allure-results
    (this launches a local server with the interactive report)
13. 
