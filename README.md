# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform for regional clubs. It aims to simplify the management of club competitions and improve accessibility.



2. Getting Started
   This project uses the following technologies:
   - Python v3.x+
   - [Flask](https://flask.palletsprojects.com/en/1.1.x/)
   - [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

3. Installation
   - [Current setup instructions already provided here]

4. Branching & Naming Conventions
   - **Main Branch**: `master` - Contains production-ready code.
   - **Feature Branches**: Start with `feature/` followed by a descriptive name (e.g., `feature/initial-setup`).
   - **Bug Fixes**: Start with `bug/` followed by a description of the issue (e.g., `bug/unknown-email-crash`).
   - **Improvement Branches**: Start with `improvement/` and a descriptive name.
   - **Merging**: Only merge to `master` after thorough testing and approval.

5. Testing
   - **Frameworks**: Feel free to use pytest, unittest, or Morelia.
   - **Types of Tests**: We follow a structure with unit, integration, and functional tests.
     - Unit tests are written for individual functions.
     - Integration tests verify the correct interaction between components.
     - Functional tests simulate user actions across the application.
   - **Running Tests**:
     ```bash
     pytest tests/
     ```
   - **Coverage**: 
     ```bash
     coverage run -m pytest tests/
     coverage report
     ```

6. Performance Testing
   - **Locust**: To simulate load tests, ensure Locust is installed. Run Locust with:
     ```bash
     locust -f locustfile.py
     ```

7. Current Setup
   [Maintained as-is]
