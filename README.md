# ShopTrack

   **Python inventory and sales tracker for Koozie Corner, a small shop in Taif, Saudi Arabia**

Course project for **SEN0414 Advanced Programming**, Istanbul Kültür University, 2026–2027 Fall.

---

## The problem

The shop keeps its stock and sales in a paper notebook. Popular products run out without warning, reordering is guesswork, and adding up the week's sales by hand takes hours and is often wrong.

## The solution

ShopTrack is a simple web app that staff can use from a phone at the counter:

- **Products and stock**: one product list with live stock levels
- **Sales recording**: staff record a sale in a few taps, and stock goes down automatically
- **Low-stock alerts**: products at or below their reorder level are flagged
- **Dashboard**: weekly sales total, daily chart and best sellers
- **CSV import and export**: bring in the shop's existing product list, with validation; export as CSV or JSON-LD

## Users

| User | What they do |
|---|---|
| Shop owner | Manages products, checks the dashboard and alerts, decides what to reorder |
| Shop staff | Record sales and register stock arriving from suppliers |

## Architecture

```
┌──────────────────────────────────────────────┐
│  Presentation: Flask routes + Jinja pages    │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│  Services: SaleService, ImportService,       │
│            ReportService, AlertService       │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│  Data: repositories over SQLAlchemy + SQLite │
└──────────────────────────────────────────────┘
   Validation of imported rows: RDFLib + pySHACL
```

## Repository structure

```
shoptrack/
├── app/
│   ├── models/        Product, Sale, SaleItem, StockMovement, User
│   ├── services/      sale, import, report and alert logic
│   ├── routes/        Flask pages and forms
│   ├── templates/     HTML pages
│   └── validation/    SHACL shape and validator
├── tests/             pytest unit tests
├── data/              sample CSV files for testing
├── docs/              diagrams, user guide, meeting notes
├── proposal/          proposal files saved from the Proposal Workbench
└── requirements.txt
```

## Tech stack

| Purpose | Library |
|---|---|
| Web app | Flask |
| Database | SQLAlchemy + SQLite |
| CSV and data | pandas |
| Charts | matplotlib |
| Validation and export | RDFLib, pySHACL, JSON-LD (schema.org terms) |
| Security | werkzeug.security (password hashing) |
| Testing | pytest |

## Course topics applied

Object-oriented programming (classes, inheritance, encapsulation), modules and packages, exception handling, file I/O (CSV, JSON), decorators (`login_required`, role checks), generators for large CSV files, and unit testing with pytest.

## Getting started

> The code is not written yet; these steps will be completed as the project is built.

```bash
git clone https://github.com/<owner>/shoptrack.git
cd shoptrack
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
pytest
```

You need Python 3.11 or newer.

## Team

| Member | Role | Owns |
|---|---|---|
| Malak Alfakavi | Team lead | Product and stock module, dashboard and alerts |
| Raghd Alfakavi | Release and quality lead | Sales recording, CSV import and export |

## Milestones

| Date | Milestone |
|---|---|
| 2026-10-24 | Proposal handed in, repository created, meeting with the shop owner |
| 2026-11-14 | Product and stock module with database and tests |
| 2026-11-28 | Sales recording and CSV import with validation |
| 2026-12-12 | Dashboard with charts and alerts; test report |
| 2026-12-19 | Release v1.0, trial at the shop, final submission |

## How we work

- Each member commits from their **own GitHub account**.
- New work goes on a branch and is merged into `main` through a pull request.
- Every work-log entry in the Proposal Workbench links the commit that shows the work.
- Code follows PEP 8, and all tests must pass before merging.

## License

MIT
