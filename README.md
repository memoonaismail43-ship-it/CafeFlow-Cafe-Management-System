# CafeFlow — Cafe Management System

**A web-based cafe management prototype built with Python, Streamlit, SQLite, Pandas, and Plotly.**

CafeFlow is designed to organise everyday cafe operations through a single application, bringing menu management, customer orders, billing, payment tracking, and business analytics together.

## 1. Project Overview

Managing a cafe involves several connected activities, including maintaining menu items, recording customer orders, preparing bills, tracking payments, and reviewing sales.

CafeFlow provides a centralised application to help organise these activities and simplify basic cafe management operations.

## 2. Main Features

### 1. Dashboard
- View key business metrics.
- Monitor revenue and order summaries.
- Review recent orders.
- Track outstanding payments.

### 2. Menu Studio
- Add new menu items.
- Edit item names, categories, and prices.
- Delete menu items.
- Manage item availability.

### 3. Order Desk
- Create customer orders.
- Select menu items.
- Record item quantities.
- Calculate order totals.
- View and update order statuses.

### 4. Billing & Invoices
- Generate itemised invoices.
- Display customer and order details.
- Calculate item totals and grand totals.
- View payment status.
- Export invoice information.

### 5. Payments
- Record full and partial payments.
- Track payment methods.
- Calculate outstanding balances.
- View payment records.

### 6. Analytics & Reports
- View revenue trends.
- Identify popular menu items.
- Analyse payment methods.
- Filter reports by date.
- Export sales reports as CSV files.

## 3. Screenshots

### Dashboard
![CafeFlow Dashboard](ss/overview.png)

### Menu Studio
![CafeFlow Menu Studio](ss/-menu-studio.png)

### Order Desk
![CafeFlow Order Desk](ss/order-desk.png)

### Billing & Invoices
![CafeFlow Billing](ss/billing.png)

### Payments
![CafeFlow Payments](ss/payments.png)

### Analytics & Reports
![CafeFlow Analytics](ss/analytics.png)

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web application interface |
| SQLite | Database management |
| Pandas | Data handling |
| Plotly | Interactive charts and visualisations |

## 5. Database Design

CafeFlow uses SQLite to store and manage application data.

The database includes tables for:
- Menu items
- Customer orders
- Order items
- Payments

Order item records preserve item names and prices at the time an order is created, helping maintain historical order information.

## 6. Project Management

The project also demonstrates practical project management activities using Jira.

Project planning and documentation include:
- Project overview and scope
- Requirements documentation
- Product backlog
- User stories and acceptance criteria
- Task breakdown and subtasks
- Proposed sprint planning
- Definition of Done
- Risk identification

**Sprint planning note:** Sprint 1 is documented as a proposed plan. An actual sprint was not created or started.

## 7. Testing

Manual functional testing was performed across all six application modules.

Tested areas included:
- Menu item creation, editing, and deletion
- Order creation and status updates
- Invoice calculations
- Full and partial payment recording
- Outstanding balance calculations
- Dashboard metrics and analytics
- Date filtering and CSV exports

See the [Functional Testing Report](TESTING.md) and [Detailed Test Cases](docs/TEST_CASES.md).

Testing was manual. Automated, security, performance, and multi-user testing remain future improvements.

## 8. Project Documentation

- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Software Requirements Specification](docs/SRS.md)
- [Database Design](docs/DATABASE_DESIGN.md)
- [Detailed Test Cases](docs/TEST_CASES.md)
- [Project Roadmap](docs/PROJECT_ROADMAP.md)
- [Jira Project Management](docs/JIRA_PROJECT_MANAGEMENT.md)
- [Functional Testing Report](TESTING.md)

## 9. Installation and Setup

### Prerequisites
- Python 3.10 or later
- pip

### Step 1: Clone the repository

```bash
git clone https://github.com/memoonaismail43-ship-it/CafeFlow-Cafe-Management-System.git
```

### Step 2: Open the project directory

```bash
cd CafeFlow-Cafe-Management-System
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 10. Future Improvements

Potential future enhancements include:
- User authentication and role-based access
- Improved inventory management
- Automated testing
- Enhanced security
- Cloud deployment
- Multi-user support
- Additional business reports

## 11. Project Status

**Status: Portfolio Prototype — Functional development and manual testing completed across six modules.**

CafeFlow is an educational and portfolio project. It is not presented as a production-ready commercial system.

## 12. Author

**Memoona Ismail**

BS Software Engineering Student

This project represents practical learning and work in software development, database management, project planning, and Agile project management.

## Repository

[View CafeFlow on GitHub](https://github.com/memoonaismail43-ship-it/CafeFlow-Cafe-Management-System)

---

*Built as a learning and portfolio project.*
