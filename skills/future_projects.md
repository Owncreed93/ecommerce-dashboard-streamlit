# Future Project: Unified Engineering Portfolio

## 1. Project Objective

Develop a professional-grade hub to showcase technical expertise, architectural patterns, and project delivery speed. The portfolio will be built using Python 3.13 and Streamlit, serving as a "Metadata-Driven" application.

## 2. Technical Strategy: Metadata-Driven UI

To maintain Clean Architecture principles, the portfolio should decouple data (project details) from the presentation (Streamlit).

### 2.1 Project Catalog Structure

Store project details in a `projects.json` or `projects.yaml` file. This allows the dashboard to scale without code modifications.

- **Attributes:** Name, Description, Primary Stack (e.g., Next.js, FastAPI), Architecture (e.g., DDD, Microservices), Design Patterns (e.g., Observer, Repository), Live URL, and GitHub Link (optional).

### 2.2 Visual Hierarchy (UX Strategy)

Apply the **Von Restorff effect** to highlight the most complex project (e.g., the high-performance dashboard). (Comprar con Leyes Frontend y UX/UI)

- **Cards for Projects:** Use interactive cards to display high-level metadata.
- **Deep Dive Modals:** Use `st.expander` or dedicated pages to explain the "Why" behind technical choices (e.g., "Why Polars over Pandas?").

## 3. Analysis: Is the KPI Dashboard an ETL?

### 3.1 Definition

ETL stands for **Extract, Transform, Load**.

### 3.2 Classification

Today's project is technically a **"Lightweight Hibrid ETL + BI Dashboard"**.

- **Extract:** Currently reading from local CSV; Phase 6 will implement OCI Object Storage extraction via HTTPS PAR.
- **Transform:** Massive transformation logic implemented in the Polars Lazy API (Date parsing, absolute value conversions for returns, alphanumeric ID cleaning).
- **Load:** The "Load" phase in this context is the **Materialization** of processed data into the Streamlit UI state.

### 3.3 Competitive Edge

Traditional ETLs move data into a database. Your implementation is a **Stateless ETL**, which is more efficient for real-time analytics on cloud-stored files without the cost of a persistent SQL instance.

## 4. Highlighting Experience

To maximize the impact on LinkedIn, the portfolio must explicitly tag projects with:

- **Architectural Paradigms:** Clean Architecture, Domain-Driven Design (DDD).
- **Engineering Standards:** TDD (Pytest), Strict Linting (Ruff), Financial Precision (Decimal).
- **Optimization Tech:** Lazy Evaluation, Parallel Processing, Caching.

## 5. Implementation Roadmap

1. **Infrastructure:** Define the JSON schema for project metadata.
2. **Application Layer:** Create a `PortfolioService` to filter and sort projects by technology or architecture.
3. **Presentation Layer:** Build a reactive Streamlit UI with a "Cloud-Native" look and feel.
