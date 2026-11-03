
# CafeFlow — Project Management Documentation

## 1. Project Overview

CafeFlow is a Cafe Management System developed to organise menu management, customer orders, billing, payments and analytics.

The project is managed using Jira to practise Agile project management.

## 2. Project Management Approach

The project follows an iterative development approach inspired by Agile and Scrum.

Work is divided into manageable tasks, prioritised according to business value and organised around development goals.

## 3. Product Goal

Develop a functional cafe management application that allows staff to manage menu items, process customer orders, calculate bills and track payments.

## 4. Product Backlog

| Backlog Item | Priority |
|---|---|
| Gather Requirements | Must Have |
| Design Database | Must Have |
| Create Menu Management Feature | Must Have |
| Develop Order Management Feature | Must Have |
| Implement Billing Feature | Must Have |
| Record Payments | Must Have |
| Develop Sales Analytics | Should Have |
| Customise Dashboard Themes | Could Have |

## 5. User Stories

### Menu Management

As a cafe manager, I want to manage menu items so that I can maintain accurate product information and prices.

Acceptance Criteria:
- Users can add menu items.
- Users can edit menu information.
- Users can manage item availability.

### Customer Orders

As a cafe staff member, I want to create customer orders so that orders can be processed efficiently.

Acceptance Criteria:
- Staff can create an order.
- Staff can select menu items.
- Staff can enter quantities.
- The system calculates the order total.
- Staff can review order details.

### Billing

As a cashier, I want to generate accurate bills so that customers are charged correctly.

Acceptance Criteria:
- The bill displays ordered items.
- Quantities and prices are shown.
- The total is calculated accurately.

### Payments

As a cashier, I want to record full and partial payments so that outstanding balances can be tracked.

Acceptance Criteria:
- Payments are associated with orders.
- Payment amounts are recorded.
- Remaining balances can be calculated.

### Analytics

As a cafe owner, I want to view sales reports so that I can understand business performance.

Acceptance Criteria:
- Revenue information is displayed.
- Popular menu items can be identified.
- Payment summaries are available.

## 6. Sprint Planning

### Sprint Goal

Prepare the customer-order feature so that cafe staff can create orders, select menu items, enter quantities and calculate totals.

### Planned Work

- Design order form.
- Implement menu item selection.
- Implement quantity selection.
- Calculate order total.
- Validate order details.
- Test order creation.

### Dependencies

- Menu information must be available.
- Order totals depend on selected items and quantities.
- Testing follows implementation.

## 7. Definition of Done

A task is considered complete when:
- Its acceptance criteria are satisfied.
- The implementation works as expected.
- Relevant tests have been performed.
- No known blocking defect remains.
- Work has been reviewed.

## 8. Risk Management

| Risk | Mitigation |
|---|---|
| Incorrect order totals | Validate calculations |
| Incorrect menu prices | Preserve historical price snapshots |
| Development delays | Prioritise essential features |
| Data loss | Maintain backups |

## 9. Project Tracking

Jira is used to organise tasks, monitor progress and maintain visibility of development work.

## 10. Conclusion

CafeFlow provides a practical environment for applying Agile planning, backlog management, prioritisation, task tracking and software delivery practices.
