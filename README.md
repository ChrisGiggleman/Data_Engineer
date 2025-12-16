# 📘 Data Engineer Projects & Tools

Welcome to the **Data_Engineer** repository — a growing collection of tools, scripts, and portfolio-ready projects focused on **real-world data engineering and analytics solutions**.

This repository serves as both:
- A **personal portfolio** for recruiters and hiring managers
- A **practical sandbox** for building, testing, and refining data pipelines, ETL workflows, SQL systems, and analytics use cases

---

## 🚀 Current Projects

### 📌 1. Natural Language → SQL Query Builder  
📂 `sql_builder/`

A Python-based tool that converts **plain English requests into structured SQL queries**.

Instead of manually writing SQL, a user can type:

> “Show all members' password hashes with no duplicates sorted by join date.”

And the system automatically produces:

```sql
SELECT DISTINCT member_id, username, password_hash, join_date
FROM members
ORDER BY join_date ASC;
```
## 🔧 Features
Entity and field detection via alias matching

Natural language intent parsing (filters, sorting, DISTINCT, etc.)

Schema-driven SQL generation

Extensible rule-based architecture

Cross-platform support (Windows, Linux, macOS)

## 🔜 Planned Enhancements
Date filtering (e.g., “after 2024-01-01”)

Aggregations (“count members per source”)

JOIN detection

GUI interface for business users

Packaging as a pip-installable module

# 📊 2. SQL Data Analytics Portfolio
📂 chris-giggleman-sql-analytics/

A full end-to-end SQL analytics portfolio showcasing data cleaning, transformation, validation, and business-driven analysis using SQLite and PostgreSQL.

This project is designed to mirror real analyst and analytics-engineering workflows, not toy examples.

## 🔍 What’s Included
4 complete analytics case studies:

Retail Sales Analytics

HR Attrition & Pay Equity

Healthcare Appointment No-Show Analysis

SaaS Subscriptions (MRR, Churn, Cohorts)

Raw CSV ingestion → cleaned datasets → analytical queries

Mermaid ERDs and pipeline flow diagrams

Before/After data cleaning validation

Business insights and recommendations

GitHub Pages site for recruiter-friendly viewing

Practice guide for rebuilding and extending each project

## 🛠️ Skills Demonstrated
SQL (CTEs, window functions, cohort analysis)

Data cleaning and quality validation

Schema design and normalization

Analytics engineering patterns

Business-focused insight generation

SQLite & PostgreSQL (Docker)

## 🔗 Portfolio Entry Point:
➡️ See the project README inside chris-giggleman-sql-analytics/ for full documentation and live GitHub Pages link.

📂 Repository Structure
```
Data_Engineer/
│
├── README.md                         # You are here
│
├── sql_builder/                      # Natural language → SQL generation tool
│   ├── main.py
│   ├── schema.py
│   ├── nl_parser.py
│   ├── sql_builder.py
│   ├── query_intent.py
│   └── schema_config.json
│
└── chris-giggleman-sql-analytics/     # End-to-end SQL analytics portfolio
```
## 🎯 Purpose of This Repository
This repository acts as a centralized engineering + analytics workspace for:

Building reusable data engineering tools

Demonstrating portfolio-ready analytics projects

Practicing ETL, SQL, and pipeline logic

Showcasing applied, real-world data skills

It intentionally blends engineering systems (automation, tooling) with analytics execution (cleaning, insights, decision support).

## 🤝 Contributions
This is a personal portfolio project, but suggestions, feature ideas, and improvements are welcome.
Feel free to open issues or submit pull requests.

## 📬 Contact
Created by: Chris Giggleman
GitHub: https://github.com/ChrisGiggleman
Email: C.giggleman@outlook.com


