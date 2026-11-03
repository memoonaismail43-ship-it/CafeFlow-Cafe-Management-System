
# ☕ CafeFlow — Cafe Management System

CafeFlow is a web-based cafe management application designed to simplify daily cafe operations through a centralized dashboard.

It helps cafe staff manage menu items, customer orders, billing, payments, and sales analytics.

## 🎯 Project Objective

The objective of CafeFlow is to reduce manual work, organize cafe operations, improve billing accuracy, and provide useful business insights.

## ✨ Key Features

### 1. Overview Dashboard
- Daily sales overview
- Total orders
- Menu item statistics
- Payments received
- Revenue and order status charts

### 2. Menu Studio
- Add menu items
- Edit item details
- Delete menu items
- Manage prices and availability
- Search and filter menu items

### 3. Order Desk
- Create customer orders
- Select menu items
- Enter item quantities
- Calculate order totals
- Track order status
- View order history

### 4. Billing & Invoices
- Generate itemized bills
- View order details
- Track payment status
- Export invoice information

### 5. Payments
- Record full and partial payments
- Track outstanding balances
- View payment history
- Export payment records

### 6. Analytics & Reports
- Revenue trends
- Popular menu items
- Payment method breakdown
- Order and payment status
- CSV report exports

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Plotly

## 🗄️ Database

CafeFlow uses SQLite to store and manage:

- Menu items
- Customer orders
- Order details
- Payment transactions

Order item prices are stored as snapshots to preserve historical billing accuracy when menu prices change.

## 🚀 Run Locally

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd YOUR_REPOSITORY_NAME
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the application

```bash
streamlit run app.py
```


## 📸 Application Screenshots

### 1. Overview Dashboard
![CafeFlow Overview](screenshots/01-overview.png)

### 2. Menu Studio
![CafeFlow Menu Studio](screenshots/02-menu-studio.png)

### 3. Order Desk
![CafeFlow Order Desk](screenshots/03-order-desk.png)

### 4. Billing & Invoices
![CafeFlow Billing](screenshots/04-billing.png)

### 5. Payments
![CafeFlow Payments](screenshots/05-payments.png)

### 6. Analytics & Reports
![CafeFlow Analytics](screenshots/06-analytics.png)

## 🔮 Future Improvements

- User authentication and role-based access
- Inventory management
- Low-stock notifications
- Advanced sales reporting
- Cloud database integration
- Automated report generation

## 👩‍💻 Developer

Developed as a software engineering and project management portfolio project.

**Project:** CafeFlow  
**Version:** 2.0  
**Status:** Working prototype
