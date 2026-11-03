
# CafeFlow — Software Testing Documentation

**Version:** 2.0  
**Testing Type:** Manual Functional Testing  
**Application:** Cafe Management System

## 1. Introduction

This document describes the functional test cases designed to verify the main features of CafeFlow.

Testing focuses on menu management, order processing, billing, payment tracking and analytics.

## 2. Testing Objectives

- Verify that application features work as expected.
- Check order total calculations.
- Verify payment and outstanding balance calculations.
- Identify unexpected application behaviour.
- Confirm that existing records remain accessible.

## 3. Test Environment

| Component | Environment |
|---|---|
| Operating System | Windows |
| Language | Python |
| Framework | Streamlit |
| Database | SQLite |
| Data Processing | Pandas |
| Charts | Plotly |
| Execution | Google Colab prototype |

## 4. Test Cases

### TC-01: View Dashboard

**Module:** Overview

Steps:
1. Open CafeFlow.
2. Navigate to Overview.
3. Observe the dashboard metrics and charts.

Expected Result: Dashboard metrics and visualisations are displayed.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-02: Add Menu Item

**Module:** Menu Studio

Steps:
1. Open Menu Studio.
2. Enter a menu item name.
3. Enter its category and price.
4. Save the item.

Expected Result: The new menu item appears in the menu list.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-03: Edit Menu Item

**Module:** Menu Studio

Steps:
1. Select an existing menu item.
2. Change its information.
3. Save the changes.

Expected Result: Updated information is displayed.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-04: Create Customer Order

**Module:** Order Desk

Steps:
1. Open Order Desk.
2. Enter customer information.
3. Select menu items.
4. Enter quantities.
5. Create the order.

Expected Result: Order is created and appears in the order register.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-05: Calculate Order Total

**Module:** Order Desk

Steps:
1. Create an order containing menu items.
2. Select quantities.
3. Review the calculated total.

Expected Result: Total equals the sum of each item's quantity multiplied by its unit price.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-06: Update Order Status

**Module:** Order Desk

Steps:
1. Select an existing order.
2. Change its status.
3. Save the update.

Expected Result: The new order status is displayed.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-07: Record Partial Payment

**Module:** Payments

Steps:
1. Select an order with an outstanding balance.
2. Enter an amount smaller than the remaining balance.
3. Record the payment.

Expected Result: Payment is saved and the outstanding balance is updated.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-08: Record Full Payment

**Module:** Payments

Steps:
1. Select an order with an outstanding balance.
2. Enter the remaining amount.
3. Record the payment.

Expected Result: Outstanding balance becomes zero and payment status is updated.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-09: View Invoice

**Module:** Billing & Invoices

Steps:
1. Open Billing & Invoices.
2. Select an order.
3. Review its itemised details.

Expected Result: Invoice displays the correct order items, quantities and prices.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-10: View Analytics

**Module:** Analytics & Reports

Steps:
1. Open Analytics & Reports.
2. Select the reporting date range.
3. Review the charts and metrics.

Expected Result: Analytics are displayed for the selected period.

Actual Result: To be recorded during testing.

Status: Not Recorded

### TC-11: Export Sales Report

**Module:** Analytics & Reports

Steps:
1. Open Analytics & Reports.
2. Select the sales report export option.
3. Download the CSV file.

Expected Result: A CSV report is generated and downloaded.

Actual Result: To be recorded during testing.

Status: Not Recorded

## 5. Testing Summary

| Result | Count |
|---|---:|
| Passed | To be updated |
| Failed | To be updated |
| Not Recorded | 11 |

## 6. Defect Reporting

Any unexpected behaviour should be recorded with:

- Defect ID
- Related test case
- Description
- Steps to reproduce
- Expected result
- Actual result
- Severity
- Resolution status

## 7. Conclusion

These test cases provide a structured approach to validating CafeFlow's main functional modules.

Testing results will be updated after execution of each test case.
