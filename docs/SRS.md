# CafeFlow — Software Requirements Specification (SRS)

**Version:** 2.0  
**Project:** Cafe Management System  
**Document Type:** Software Requirements Specification  
**Status:** Working Prototype

## 1. Introduction

### 1.1 Purpose
This document defines the functional and non-functional requirements of CafeFlow, a web-based Cafe Management System.

### 1.2 Project Scope
CafeFlow provides a centralised platform for managing cafe operations, including menu management, customer orders, billing, payments and sales analytics.

### 1.3 Intended Users
- Cafe owners
- Cafe managers
- Cashiers
- Cafe staff

## 2. Overall System Description

CafeFlow is developed using Python and Streamlit. It uses SQLite for data storage and Plotly and Pandas for data presentation and processing.

The application provides six main modules:

1. Overview Dashboard
2. Menu Studio
3. Order Desk
4. Billing & Invoices
5. Payments
6. Analytics & Reports

## 3. Functional Requirements

### FR-01: Dashboard
The system shall display key business information, including sales, orders, menu statistics and payment summaries.

### FR-02: Menu Management
The system shall allow users to:
- Add menu items.
- Edit menu item information.
- Delete menu items.
- Set item prices.
- Manage item availability.

### FR-03: Order Management
The system shall allow users to:
- Create customer orders.
- Select menu items.
- Enter item quantities.
- Calculate order totals.
- View order history.
- Update order status.

### FR-04: Billing
The system shall:
- Display itemised order details.
- Calculate bill totals.
- Show payment status.
- Provide invoice information.

### FR-05: Payment Management
The system shall:
- Record payments.
- Support full and partial payments.
- Track outstanding balances.
- Display payment history.
- Export payment records.

### FR-06: Analytics and Reports
The system shall:
- Display sales trends.
- Identify popular menu items.
- Summarise payment methods.
- Display order and payment status.
- Allow report exports.

## 4. Non-Functional Requirements

### NFR-01: Usability
The application should provide a clear and understandable interface.

### NFR-02: Performance
The application should respond efficiently to normal cafe management operations.

### NFR-03: Data Integrity
The system should maintain consistent order, order-item and payment records.

### NFR-04: Reliability
The application should handle invalid inputs and database operations appropriately.

### NFR-05: Maintainability
The application should use organised code and documented dependencies.

### NFR-06: Security
Sensitive business and payment information should be protected. The current prototype does not yet implement production-grade authentication or access control.

## 5. Database Requirements

The system uses SQLite and maintains four main entities:

- Menu Items
- Orders
- Order Items
- Payments

Order item records preserve item names and unit prices at the time of ordering to support historical billing accuracy.

## 6. Assumptions and Constraints

- The application requires Python and its listed dependencies.
- The current prototype uses SQLite.
- The current deployment through a temporary tunnel is intended for demonstration.
- Production deployment requires additional security, authentication and hosting configuration.

## 7. Future Enhancements

- User authentication and role-based access.
- Inventory management.
- Low-stock notifications.
- Cloud database integration.
- Advanced business reporting.
- Automated backups.

## 8. Conclusion

CafeFlow aims to simplify cafe operations by bringing menu management, order processing, billing, payments and analytics into one application.
