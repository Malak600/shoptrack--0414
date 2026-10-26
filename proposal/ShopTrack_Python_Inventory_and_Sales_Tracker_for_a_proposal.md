# ShopTrack: Python Inventory and Sales Tracker for a Small Shop in Taif

SEN0414 Advanced Programming · 2026-2027 Fall · Proposal · Method: BRSF software-development profile · Self-assessed grade 99.5/100

## Team, roles and work distribution

| Member | Student number | E-mail | Administrative roles | Development roles | Planned share |
| --- | --- | --- | --- | --- | --- |
| Malak Alfakavi | 2200002701 | 2200002701@stu.iku.edu.tr | Team lead, Documentation lead, Customer liaison | Back-end developer, Front-end developer, Requirements analyst | 55% |
| Raghd Alfakavi | 2200002698 | 2200002698@stu.iku.edu.tr | Repository and release manager, Quality lead | Data engineer, Test engineer, Architect | 45% |

### Modules and features

| Module or feature | Kind | What it does | Delivers epic | Responsible member | Second member |
| --- | --- | --- | --- | --- | --- |
| Product and stock module | Module | Add, edit and delete products; track stock levels; record stock arriving from suppliers. | E1 Product and stock management | Malak Alfakavi · 2200002701 | Raghd Alfakavi · 2200002698 |
| Reports and alerts dashboard | Feature | Weekly sales charts, best sellers and low-stock alerts on one page. | E3 Reports and alerts | Malak Alfakavi · 2200002701 | Raghd Alfakavi · 2200002698 |
| Sales recording module | Module | Record each sale quickly; stock is reduced automatically. | E2 Sales recording | Raghd Alfakavi · 2200002698 | Malak Alfakavi · 2200002701 |
| CSV import, validation and export | Feature | Import the shop's existing product list from CSV/Excel, validate it, and export data as CSV and JSON-LD. | E4 Data import, validation and export | Raghd Alfakavi · 2200002698 | Malak Alfakavi · 2200002701 |

### Process leads

- Mission analysis: Malak Alfakavi
- Stakeholder needs and requirements: Malak Alfakavi
- System/software requirements definition: Malak Alfakavi
- Architecture definition: Raghd Alfakavi
- Design definition: Malak Alfakavi
- Implementation: Malak Alfakavi
- Integration: Raghd Alfakavi
- Verification: Raghd Alfakavi
- Transition: Raghd Alfakavi
- Validation: Malak Alfakavi

### Work log

6 entries; chain intact; head fingerprint 0fb81d6a3c5c23b0a8d0c1c5cc7dc807fce51cdbb7aaac4b995f33b56c97db26.

| No. | Time (UTC) | Member | Process | Hours | What | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-10-17 14:17 | Malak Alfakavi | Mission analysis | 2 | Chose the ShopTrack idea and prepared mission, scope, goals and backlog in the proposal | https://github.com/Malak600/shoptrack--0414 |
| 2 | 2026-10-17 14:18 | Malak Alfakavi | Architecture definition | 1 | Renamed the GitHub repository to shoptrack and wrote the README with architecture and folders | https://github.com/Malak600/shoptrack--0414 |
| 3 | 2026-10-17 14:18 | Raghd Alfakavi | Stakeholder needs and requirements | 1 | Reviewed the sales and import stories and checked the acceptance criteria with the team | https://github.com/Malak600/shoptrack--0414 |
| 4 | 2026-10-17 14:19 | Raghd Alfakavi | Implementation | 2 | Set up the Flask project structure, requirements file and first pytest test | https://github.com/Malak600/shoptrack--0414 |
| 5 | 2026-10-26 10:51 | Raghd Alfakavi | Implementation | 1.5 | Uploaded the Flask starter code and organized it into app, models, routes and tests packages | https://github.com/Malak600/shoptrack--0414/commits/main |
| 6 | 2026-10-26 11:04 | Raghd Alfakavi | Implementation | 0.1 | Correction: the Flask setup in entry 4 was planned that day and actually committed on 26 October, see entry 5 | https://github.com/Malak600/shoptrack--0414/commits/main |

## 1. Mission

### Customer

| Customer (organisation or role) | Contact person or role | How and when you reached them | Relation | What they get from it |
| --- | --- | --- | --- | --- |
| The Koozie Corner, Taif, Saudi Arabia | Hiyam Yassin, owner of the shop | WhatsApp, 17 October 2026, answered and agreed to test | Owner of the system | One simple web tool that replaces their Excel sheets and notebook: live stock, weekly sales and low-stock alerts in one place. |

### End users

| User group (short name) | Who exactly | What they do with the system | How often | Device or channel |
| --- | --- | --- | --- | --- |
| Shop owner | The owner who runs the shop and orders from suppliers | Checks stock, sees weekly sales reports and decides what to reorder | Daily | Laptop or phone browser |
| Shop staff | Cashiers and helpers working at the shop counter | Record each sale and register new stock when deliveries arrive | Daily | Phone or tablet browser at the counter |

### Problem

The shop tracks its stock and sales in Excel sheets together with a physical notebook for quick daily notes. Sales written in the notebook during the day must be copied into Excel later, so the two often do not match and the real stock level is never certain. When a popular product runs out, the owner usually notices only when a customer asks for it, so the sale is lost. Reordering is based on looking at the shelves rather than on data, which leads both to empty shelves and to products that stay unsold. The shop sells around 25 to 35 different products, and the owner spends about 4 to 5 hours every week counting stock, copying notes into Excel and checking sales (owner's answers by WhatsApp, 17 October 2026). There is no weekly report that shows which products sell best. The shop needs one simple tool that staff can use from a phone at the counter, that updates stock automatically with every sale, and that warns before a product runs out.

### Mission statement

ShopTrack gives the shop owner and shop staff of a small shop in Taif a simple Python web application to record sales, see live stock levels and receive low-stock alerts, so the shop owner stops losing sales to empty shelves and spends minutes, not hours, on weekly stock and sales reports.

Origin: Derived

### Outcome

Once ShopTrack exists, the shop owner opens one page and sees what is in stock, what sold this week and which products must be reordered today. Shop staff record a sale in a few taps on a phone, and the stock updates automatically, which the Excel sheets and notebook can never do.

## 2. Scope

### Areas

| Area | Where it lives | How big it is today |
| --- | --- | --- |
| Product and stock management | Flask web app, products and stock tables in SQLite | Excel sheets and a paper notebook that often do not match |
| Sales recording | Sales page used by shop staff at the counter | Sales noted in a notebook, copied into Excel later |
| Reports and alerts | Dashboard page with charts and alerts | No reports; weekly totals added up by hand |
| Data import, validation and export | CSV import tool, SHACL validation, CSV and JSON-LD export | No machine-readable data |

### Deliverables

| Deliverable | Area | Layer | Kind |
| --- | --- | --- | --- |
| Product list with add, edit, delete and stock-in | Product and stock management | Product layer | Functional |
| Stock can never go below zero; every change is recorded | Product and stock management | Product layer | Non-functional |
| Sales page that records a sale and reduces stock | Sales recording | Product layer | Functional |
| Recording a sale takes under 15 seconds on a phone | Sales recording | Product layer | Non-functional |
| Dashboard with weekly sales chart, best sellers and low-stock alerts | Reports and alerts | Product layer | Functional |
| CSV import with validation and error report; CSV and JSON-LD export | Data import, validation and export | Product layer | Functional |
| Unit tests with pytest and a short user guide for the shop | Data import, validation and export | Work layer | Non-functional |

### Exclusions

| Left out | Why |
| --- | --- |
| Card payments and a cash-register (POS) integration | Payment systems need certification and bank contracts; the shop keeps its existing payment method. |
| E-invoicing (ZATCA Fatoora) and VAT accounting | Official Saudi tax invoices need an approved e-invoicing solution and an accountant; out of reach in one term. |
| Online shop for customers | The problem is inside the shop (stock and sales); selling online is a different project. |
| Customer personal data and loyalty cards | Not needed to solve the stock problem and would bring personal-data obligations. |

### Domain entities

| Entity | What it is | Created? | Used? | Retired? |
| --- | --- | --- | --- | --- |
| Product | An item the shop sells, with name, category, barcode (optional), price and reorder level. | Created — yes | Used — yes | Retired — yes |
| Stock movement | A change in the quantity of a product: stock in from a supplier, a sale, or a correction. | Created — yes | Used — yes | Retired — no |
| Sale | One sale recorded by staff: products, quantities, total and time. | Created — yes | Used — yes | Retired — no |
| User | A person who signs in: the shop owner (all rights) or a staff member (sales and stock-in only). | Created — yes | Used — yes | Retired — yes |

### Project kinds

Semantic automation › Data pipeline automation; Knowledge-graph application › Graph-backed web application. Stack layers they need: Data model, Integration and mapping, Validation, Query, Storage and serving.

### Semantic technologies, by stack layer

- Data model: RDFLib
- Serialisation: JSON-LD 1.1 contexts, RDFLib
- Validation: SHACL shapes, pySHACL
- Vocabularies and taxonomies: schema.org

schema.org gives standard terms for the shop's data (schema:Product, schema:Offer, schema:Order), so we do not invent our own names. JSON-LD lets ShopTrack export the product list in a form other tools and websites understand, while it stays ordinary JSON. RDFLib builds and reads that graph in Python. SHACL shapes, checked with pySHACL, validate every product imported from the shop's CSV (name present, price positive, stock a whole number) before it enters the database, so bad rows are reported instead of silently breaking the stock figures.

## 3. Goals

| Goal | Facing | Covers area | Why this goal |
| --- | --- | --- | --- |
| The shop owner always knows what is in stock and what to reorder, without counting shelves | Mission-facing | Reports and alerts | This is the change the mission promises. |
| Products, sales, reports and data import all work together in one delivered application | Scope-facing | Product and stock management | Every scope area must be finished, not only the easy part. |
| Sales recording stays simple: no payments, invoices or online shop | Containment-facing | Sales recording | Keeps effort inside the named areas so the project fits one term. |
| Only valid product data ever enters the database | Scope-facing | Data import, validation and export | Wrong imported data would make every stock figure and report wrong. |

### Specification

The shop owner signs in and imports the existing product list from a CSV file; each row is checked against a SHACL shape and invalid rows are listed with the reason. Owner and staff can add and edit products and register stock arriving from suppliers. Staff record a sale by choosing products and quantities; the system saves the sale, reduces the stock of each product and refuses a sale larger than the stock. When a product's stock falls to its reorder level, it appears in the low-stock alert list. The dashboard shows this week's sales total, a daily sales chart and the best-selling products. The owner can export products and sales as CSV or JSON-LD.

### Test scenarios

| Kind | Scenario (Given / When / Then) |
| --- | --- |
| Nominal | Given a product with 10 in stock, when staff record a sale of 3, then the sale is saved and the stock shows 7. |
| Rejection | Given a product with 2 in stock, when staff try to record a sale of 5, then the sale is refused with the message Not enough stock and nothing changes. |
| Rejection | Given a CSV row with a negative price, when the owner imports the file, then that row is rejected and shown in the error report with its line number. |
| Boundary | Given a product with reorder level 5 and stock 6, when one unit is sold, then the product appears in the low-stock alerts. |
| Absent | Given no sales recorded this week, when the owner opens the dashboard, then it shows zero sales and a clear empty-state message instead of an error. |

### Use cases

Actors: Shop owner, Shop staff. Use cases: Import products (owner), Manage products (owner), Register stock-in (owner, staff), Record sale (staff, owner), View dashboard and alerts (owner), Export data (owner), Manage users (owner).

## 4. Objectives

| Objective | Goal | Measured by | How exactly it is measured | Now | Target | Direction |
| --- | --- | --- | --- | --- | --- | --- |
| Weekly time the owner spends counting stock and checking records | The shop owner always knows what is in stock and what to reorder, without counting shelves | Judged | Owner's own estimate in hours per week, asked on 17 Oct 2026 and again after 2 weeks of use | 4-5 hours per week (owner's answer, 17 Oct 2026) | under 1 hour | Decrease |
| Share of planned test cases that pass | Products, sales, reports and data import all work together in one delivered application | Derived | Passed pytest cases divided by planned test cases, from the test report | 0% | at least 90% | Increase |
| Work items outside the four scope areas | Sales recording stays simple: no payments, invoices or online shop | Counted | Count of commits or log entries not linked to a story of epics E1-E4 | 0 | 0 | Hold |
| Invalid product rows that reach the database | Only valid product data ever enters the database | Counted | Import a test CSV with 20 known-bad rows; count how many are stored | No validation | 0 | Hold |

### Activity model

Recording a sale: 1. Staff opens the sales page. 2. Searches or scans a product and enters the quantity. 3. System checks stock: if the quantity is larger than the stock, show Not enough stock and return to step 2; otherwise continue. 4. Staff confirms the sale. 5. System saves the sale and a stock movement and reduces stock. 6. If the new stock is at or below the reorder level, add the product to the low-stock alerts. 7. Show the sale receipt on screen. Import branch: owner uploads CSV, each row is validated, valid rows are saved, invalid rows go to the error report.

### Sequence model

Staff -> Sales page: choose product and quantity. Sales page -> Flask route /sales: POST sale. Route -> SaleService: record_sale(items). SaleService -> Product repository: get stock. Product repository -> SaleService: current stock. SaleService -> Database: save Sale and StockMovement, update stock (one transaction). SaleService -> AlertService: check_reorder(product). AlertService -> SaleService: alert or none. SaleService -> Route: result. Route -> Staff: confirmation page with new stock.

## 5. Backlog

Kind of development: Initial development

### Epics

| Epic | Pursues objective |
| --- | --- |
| E1 Product and stock management | Share of planned test cases that pass |
| E2 Sales recording | Share of planned test cases that pass |
| E3 Reports and alerts | Weekly time the owner spends counting stock and checking records |
| E4 Data import, validation and export | Invalid product rows that reach the database |

### Stories

| Epic | As a | I want | So that | Acceptance (Given / When / Then) | Category | Design concern | Value 1–10 | Time 1–10 | Risk 1–10 | Size 1–10 | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 Product and stock management | Shop owner (end user) | to add and edit products with price and reorder level | the shop's product list is in one place | Given I am signed in as owner, when I save a product with name, price and reorder level, then it appears in the product list with stock 0. | New capability | Data | 8 | 6 | 5 | 3 | 6.3 |
| E1 Product and stock management | Shop staff (end user) | to register stock that arrives from a supplier | the stock figures stay correct | Given a product with stock 4, when I register 10 arriving, then the stock shows 14 and a stock movement is recorded. | New capability | Data | 7 | 5 | 4 | 2 | 8 |
| E2 Sales recording | Shop staff (end user) | to record a sale quickly from my phone | I can keep serving customers | Given products in stock, when I choose them with quantities and confirm, then the sale is saved and each product's stock is reduced. | New capability | Interaction | 10 | 8 | 6 | 5 | 4.8 |
| E2 Sales recording | Shop owner (end user) | sales larger than the stock to be refused | stock never goes negative | Given a product with 2 in stock, when a sale of 5 is entered, then it is refused with Not enough stock and nothing is saved. | New capability | Data | 7 | 5 | 8 | 2 | 10 |
| E3 Reports and alerts | Shop owner (end user) | a list of products at or below their reorder level | I reorder before shelves are empty | Given a product with reorder level 5, when its stock falls to 5, then it appears in the low-stock alerts on the dashboard. | New capability | User interface | 9 | 7 | 6 | 3 | 7.3 |
| E3 Reports and alerts | Shop owner (end user) | a weekly sales chart and best-seller list | I know what sells and what does not | Given sales recorded this week, when I open the dashboard, then I see the weekly total, a daily chart and the top 5 products. | New capability | User interface | 8 | 5 | 3 | 5 | 3.2 |
| E4 Data import, validation and export | Shop owner (end user) | to import my existing product list from a CSV file | I do not type hundreds of products by hand | Given a CSV with valid and invalid rows, when I import it, then valid rows are saved and invalid rows are listed with their line number and reason. | New capability | Architecture | 8 | 7 | 7 | 5 | 4.4 |
| E1 Product and stock management | Shop owner (end user) | staff accounts that can only record sales and stock-in | staff cannot change prices or delete products | Given I am signed in as staff, when I open the edit-price page, then access is refused. | New capability | Security | 6 | 4 | 7 | 3 | 5.7 |

### Definition of done

| Criterion | How it is checked |
| --- | --- |
| Code is committed and the work-log entry links the commit | Commit link present in the log entry |
| All pytest tests pass | pytest run shows no failures |
| The story's acceptance criterion is demonstrated | Screenshot or short video attached to the story |
| Code follows PEP 8 and has docstrings | flake8 shows no errors |

### Class model

Product (id, name, category, barcode, price, stock, reorder_level; methods: add_stock(qty), remove_stock(qty), needs_reorder()). StockMovement (id, product, quantity, kind: IN | SALE | CORRECTION, time). Sale (id, time, user, total; has 1..* SaleItem). SaleItem (product, quantity, unit_price). User (id, name, role: OWNER | STAFF, password_hash). Services: SaleService (record_sale), ImportService (import_csv, validate_row), ReportService (weekly_total, best_sellers, low_stock). Product 1 -- 0..* StockMovement; Sale 1 -- 1..* SaleItem; SaleItem * -- 1 Product.

### Test cases

| For story | Test case | Test data |
| --- | --- | --- |
| to add and edit products with price and reorder level | Create a product and check it is listed with stock 0 | Product 'Tea 500g', price 85, reorder level 5 |
| to register stock that arrives from a supplier | Register stock-in and check the new stock and movement | Product with stock 4, add 10 |
| to record a sale quickly from my phone | Record a sale of 2 products and check stock reduced | Tea stock 10 sell 3; Sugar stock 8 sell 1 |
| sales larger than the stock to be refused | Try a sale larger than stock | Product with stock 2, sale of 5 |
| a list of products at or below their reorder level | Sell until reorder level and check the alert | Product stock 6, reorder level 5, sell 1 |
| a weekly sales chart and best-seller list | Check weekly total and top 5 on seeded sales | Fixture with 30 sales over 7 days |
| to import my existing product list from a CSV file | Import a CSV with 18 valid and 2 invalid rows | products_test.csv with a negative price and a missing name |
| staff accounts that can only record sales and stock-in | Staff user opens the edit-price page | Staff test account |

### Architecture — Component diagram

Layers: Flask routes and Jinja templates (presentation) -> service classes SaleService, ImportService, ReportService (business logic) -> repository classes over SQLAlchemy and SQLite (data). Validation module uses RDFLib + pySHACL on imported rows. Charts made with matplotlib and served as images.

### Data — Class diagram

Tables: products, stock_movements, sales, sale_items, users in SQLite through SQLAlchemy. Stock is always changed through a stock movement inside one transaction, so stock = sum of movements and can be rebuilt. Constraint: stock >= 0.

### Interaction — Sequence diagram

Sale sequence: Staff selects products -> page sends POST /sales -> SaleService checks stock for every item -> if all available, saves Sale, SaleItems and StockMovements in one transaction -> AlertService checks reorder levels -> page shows confirmation; if any item is short, nothing is saved and the short items are shown.

### Security — State machine diagram

States of a user session: Signed out -> Signed in as Staff (sales, stock-in only) or Signed in as Owner (everything). Any request to an owner-only page from a staff session is refused (403). Passwords stored only as hashes (werkzeug.security).

### User interface — design model

Screens: 1) Sign in; 2) Dashboard (weekly total, daily chart, top 5, low-stock alerts); 3) Products list with search; 4) Product form; 5) Sales page with large buttons for phone use; 6) Import page with error report; 7) Export page.

## 6. Course-specific

### Python libraries and course topics

Python libraries: Flask (web app and routing), SQLAlchemy with SQLite (database), pandas (reading CSV and Excel, weekly sales calculations), matplotlib (sales charts), RDFLib and pySHACL (JSON-LD export and validation of imported products), werkzeug.security (password hashing), and pytest (unit tests). Course topics applied: object-oriented programming with classes, inheritance and encapsulation (Product, Sale, User, service and repository classes), modules and packages, exception handling (NotEnoughStockError, invalid CSV rows), file I/O for CSV and JSON, decorators (login_required, role checks, timing), generators for reading large CSV files row by row, and automated unit testing with pytest.

## Plan and risks

| Date | Deliverable | Lead |
| --- | --- | --- |
| 2026-10-24 | Proposal handed in; repository created; owner interviewed by WhatsApp | Malak Alfakavi |
| 2026-11-14 | Product and stock module with database and tests | Malak Alfakavi |
| 2026-11-28 | Sales recording and CSV import with validation | Raghd Alfakavi |
| 2026-12-12 | Dashboard with charts and alerts; test report | Malak Alfakavi |
| 2026-12-19 | Tagged release v1.0, online trial with the shop owner, final submission | Raghd Alfakavi |

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| The team has only two members and the workload is large for one term | Medium | High | Split modules clearly; drop export and charts polish first if late. |
| The shop owner is too busy to test the system | Medium | Medium | Agree a 20-minute test date now; prepare a demo with sample data. |
| The shop's existing product list is messy or incomplete | High | Medium | CSV import with validation and an error report; fix rows together with the owner. |
| The shop is in Taif, Saudi Arabia, so testing and feedback happen remotely | Medium | Medium | Host the app online, run the trial over a video call, and collect feedback by WhatsApp. |
| Free hosting is slow or goes down | Low | Medium | Run locally on the owner's laptop as backup; keep a database backup. |

Repository: https://github.com/Malak600/shoptrack--0414 — Confirmed on GitHub 2026-10-17 (public, created 2026-10-17)

## References

1. Python Software Foundation, "The Python Language Reference," https://docs.python.org/3/
2. Pallets, "Flask Documentation," https://flask.palletsprojects.com
3. W. McKinney, Python for Data Analysis, 3rd ed., O'Reilly, 2022.
4. E. Gamma, R. Helm, R. Johnson, J. Vlissides, Design Patterns: Elements of Reusable Object-Oriented Software, Addison-Wesley, 1994.
5. schema.org, "Product" and "Offer" types, https://schema.org/Product
6. W3C, "Shapes Constraint Language (SHACL)," W3C Recommendation, 2017.
7. pytest documentation, https://docs.pytest.org

## Self-assessment

| Part | Weight | Grade | Criteria met |
| --- | --- | --- | --- |
| Team and work | 10% | 95/100 | 11 of 12 |
| Mission | 20% | 100/100 | 7 of 7 |
| Scope | 15% | 100/100 | 8 of 8 |
| Goal | 15% | 100/100 | 7 of 7 |
| Objective | 10% | 100/100 | 3 of 3 |
| Backlog | 20% | 100/100 | 10 of 10 |
| Course-specific | 5% | 100/100 | 1 of 1 |
| Plan and references | 5% | 100/100 | 3 of 3 |
| Overall | 100% | 99.5/100 |  |

### Member grades (Proposal)

Project grade 100 (60%), team grade 95 (20%), individual contribution (20%).

| Member | Student number | Individual | Member grade |
| --- | --- | --- | --- |
| Malak Alfakavi | 2200002701 | 100 | 99 |
| Raghd Alfakavi | 2200002698 | 100 | 99 |

