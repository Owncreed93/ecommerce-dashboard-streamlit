# Technical Instructions for KPI Dashboard Development

## 1. Core Architectural Principles

The assistant must strictly adhere to the following software engineering paradigms:

- **Domain-Driven Design (DDD):** Separate the project into Domain, Application, and Infrastructure layers.
- **Value Objects:** Use immutable objects for domain attributes (e.g., KPI values, dates, identifiers) to ensure business logic validity.
- **Object-Oriented Programming (OOP):** Use classes, inheritance, and interfaces (Abstract Base Classes) appropriately.
- **Principles:** Apply DRY (Don't Repeat Yourself), SOLID (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion), and KISS (Keep It Simple, Stupid).

## 2. Development Workflow (TDD)

Before generating any implementation code, the assistant must provide:

- **Unit Tests:** Define the expected behavior using `pytest`.
- **Red-Green-Refactor:** Ensure the implementation satisfies the written tests.

## 3. Coding Standards and Tooling

- **Language:** Python 3.13.
- **Style Guide:** Strictly follow PEP 8 and Python 3.13 best practices.
- **Linter/Formatter:** Code must be 100% compatible with **Ruff** (Rules: E, W, F, I, D, UP, B, ANN).
- **Mandatory Code Patterns:**
  - **Module Docstrings:** Every `.py` file MUST start with a module-level docstring.
  - **Type Annotations:** All function signatures must have explicit type hints for arguments and return values (e.g., `-> None` for tests).
  - **Sorted Imports:** Imports must be organized (Standard Library > External > Local).
  - **Dataclass Optimization:** Use `@dataclass(frozen=True, slots=True)` for all Value Objects.
  - **Financial Precision:** Use `Decimal` for all monetary calculations.
- **Documentation:** All docstrings must follow the Google Python Style Guide and remain exclusively in technical English. No emojis are allowed.

## 4. Specific KPI Domain Requirements

- Define a `KPI` Entity within the Domain layer.
- Use `ValueObjects` for:
  - `KpiValue`: Must handle numerical validation and scale.
  - `KpiDate`: Must handle ISO 8601 formatting.
  - `KpiTarget`: Must define threshold logic.

## 5. Infrastructure and Deployment

- **Target Platform:** PythonAnywhere.
- Provide a `wsgi.py` configuration template.
- Ensure the web framework (e.g., Flask or FastAPI) is decoupled from the Domain layer via Adapters.

## 6. Output Formatting

- Provide clear file structures.
- Use code blocks for every file.
- Explain the implementation steps in technical English.
