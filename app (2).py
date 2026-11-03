import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime
from contextlib import contextmanager

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CafeFlow | Cafe Management",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_NAME = "cafeflow.db"

# ---------------- DATABASE ----------------
@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def setup_database():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            available INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            order_date TEXT,
            total REAL NOT NULL,
            status TEXT DEFAULT 'Placed'
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            menu_item_id INTEGER,
            item_name TEXT,
            quantity INTEGER,
            unit_price REAL,
            line_total REAL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            amount REAL NOT NULL,
            payment_method TEXT,
            payment_date TEXT,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );

        CREATE INDEX IF NOT EXISTS idx_orders_date
        ON orders(order_date);

        CREATE INDEX IF NOT EXISTS idx_order_items_order
        ON order_items(order_id);

        CREATE INDEX IF NOT EXISTS idx_payments_order
        ON payments(order_id);
        """)


setup_database()


# ---------------- HELPERS ----------------
def read_df(query, params=()):
    with get_db() as conn:
        return pd.read_sql_query(query, conn, params=params)


def money(value):
    return f"Rs. {float(value or 0):,.2f}"


def payment_summary(order_id, total):
    with get_db() as conn:
        row = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) AS paid FROM payments WHERE order_id=?",
            (order_id,)
        ).fetchone()

    paid = float(row["paid"] or 0)
    total = float(total or 0)
    balance = max(total - paid, 0)

    if paid <= 0:
        status = "Unpaid"
    elif balance <= 0.009:
        status = "Paid"
    else:
        status = "Partially Paid"

    return paid, balance, status


def heading(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_order_items(order_id):
    return read_df(
        """SELECT item_name AS Item, quantity AS Quantity,
                  unit_price AS [Unit Price], line_total AS [Line Total]
           FROM order_items WHERE order_id=?""",
        (order_id,)
    )


# ---------------- DESIGN ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background: #111315;
    color: #F4EFE8;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: #191B1D;
    border-right: 1px solid #34302B;
}
[data-testid="stSidebar"] * {
    color: #F4EFE8;
}
.brand {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    font-weight: 700;
    color: #E7B77A;
    padding: 8px 0 0 0;
}
.brand-sub {
    color: #A9A29A;
    font-size: 12px;
    letter-spacing: 2px;
    margin-bottom: 22px;
}
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    color: #F4EFE8;
    font-weight: 700;
    margin-bottom: 2px;
}
.page-subtitle {
    color: #A9A29A;
    margin-bottom: 24px;
    font-size: 14px;
}
.metric-card {
    background: linear-gradient(135deg, #242321, #1B1D1E);
    border: 1px solid #494035;
    border-radius: 14px;
    padding: 19px;
    min-height: 112px;
    margin-bottom: 12px;
}
.metric-label {
    color: #B8AA98;
    font-size: 13px;
    margin-bottom: 9px;
}
.metric-value {
    color: #E7B77A;
    font-size: 25px;
    font-weight: 700;
}
.metric-note {
    color: #8E8982;
    font-size: 11px;
    margin-top: 5px;
}
.stButton > button {
    background: #B87945;
    color: #FFFFFF;
    border: 0;
    border-radius: 8px;
    font-weight: 600;
    min-height: 42px;
}
.stButton > button:hover {
    background: #D0925B;
    color: #FFFFFF;
    border: 0;
}
.stDownloadButton > button {
    background: #34302B;
    color: #F4EFE8;
    border: 1px solid #806345;
    border-radius: 8px;
}
div[data-baseweb="input"] input,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] textarea {
    background: #242729;
}
hr {
    border-color: #39332D;
}
h2, h3 {
    color: #E7B77A;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<div class="brand">☕ CafeFlow</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">CAFE MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "🍽️ Menu Management",
            "🧾 Orders",
            "💳 Payments",
            "📊 Analytics"
        ],
        label_visibility="visible"
    )

    st.divider()
    st.caption("CafeFlow • Portfolio Prototype")
    st.caption("Manage your cafe with clarity.")


# ============================================================
# DASHBOARD
# ============================================================
if page == "🏠 Dashboard":
    heading("Dashboard", "Your cafe at a glance. Welcome back!")

    menu_count = read_df("SELECT COUNT(*) AS n FROM menu_items").iloc[0]["n"]
    order_count = read_df("SELECT COUNT(*) AS n FROM orders").iloc[0]["n"]
    order_value = read_df("SELECT COALESCE(SUM(total),0) AS n FROM orders").iloc[0]["n"]
    received = read_df("SELECT COALESCE(SUM(amount),0) AS n FROM payments").iloc[0]["n"]
    outstanding = max(float(order_value) - float(received), 0)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("MENU ITEMS", f"{int(menu_count)}", "Items in your menu")
    with c2:
        metric_card("TOTAL ORDERS", f"{int(order_count)}", "Orders recorded")
    with c3:
        metric_card("ORDER VALUE", money(order_value), "Total value of orders")
    with c4:
        metric_card("PAYMENTS RECEIVED", money(received), "Money collected")

    st.divider()
    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("Recent Orders")
        recent = read_df("""
            SELECT id AS [Order #], customer_name AS Customer,
                   order_date AS Date, total AS Total, status AS Status
            FROM orders ORDER BY id DESC LIMIT 8
        """)
        if recent.empty:
            st.info("No orders yet. Create your first order from the Orders page.")
        else:
            st.dataframe(recent, use_container_width=True, hide_index=True)

    with right:
        st.subheader("Payment Overview")
        metric_card("OUTSTANDING BALANCE", money(outstanding), "Order value minus payments received")
        status_counts = read_df("""
            SELECT status AS Status, COUNT(*) AS Orders
            FROM orders GROUP BY status
        """)
        if not status_counts.empty:
            st.markdown("**Orders by status**")
            st.bar_chart(status_counts.set_index("Status"))


# ============================================================
# MENU MANAGEMENT
# ============================================================
elif page == "🍽️ Menu Management":
    heading("Menu Management", "Add, update and manage the items your cafe serves.")

    with st.expander("＋ Add a New Menu Item", expanded=True):
        with st.form("add_menu_form", clear_on_submit=True):
            a, b = st.columns(2)
            name = a.text_input("Item name", placeholder="e.g. Caramel Latte")
            category = b.selectbox(
                "Category",
                ["Coffee", "Tea", "Snacks", "Desserts", "Meals", "Other"]
            )
            price = st.number_input("Price (Rs.)", min_value=0.0, step=50.0)
            submitted = st.form_submit_button("Add Menu Item", use_container_width=True)

            if submitted:
                if not name.strip():
                    st.error("Please enter an item name.")
                elif price <= 0:
                    st.error("Price must be greater than zero.")
                else:
                    with get_db() as conn:
                        conn.execute(
                            "INSERT INTO menu_items (name, category, price, available) VALUES (?,?,?,1)",
                            (name.strip(), category, price)
                        )
                    st.success(f"{name.strip()} added to the menu.")
                    st.rerun()

    st.divider()
    st.subheader("Current Menu")

    menu = read_df("""
        SELECT id, name, category, price, available
        FROM menu_items ORDER BY id DESC
    """)

    if menu.empty:
        st.info("Your menu is empty. Add your first item above.")
    else:
        display_menu = menu.copy()
        display_menu["available"] = display_menu["available"].map({1: "Available", 0: "Unavailable"})
        display_menu = display_menu.rename(columns={
            "id": "ID", "name": "Item", "category": "Category",
            "price": "Price (Rs.)", "available": "Availability"
        })
        st.dataframe(display_menu, use_container_width=True, hide_index=True)

        st.subheader("Edit or Remove an Item")
        item_map = {
            f"{row['name']} (ID: {row['id']})": int(row["id"])
            for _, row in menu.iterrows()
        }
        selected_label = st.selectbox("Choose a menu item", list(item_map.keys()))
        selected_id = item_map[selected_label]
        selected = menu[menu["id"] == selected_id].iloc[0]

        with st.form("edit_menu_form"):
            new_name = st.text_input("Name", value=str(selected["name"]))
            categories = ["Coffee", "Tea", "Snacks", "Desserts", "Meals", "Other"]
            current_category = str(selected["category"])
            category_index = categories.index(current_category) if current_category in categories else 5
            new_category = st.selectbox("Category", categories, index=category_index)
            new_price = st.number_input(
                "Price (Rs.)", min_value=0.0, value=float(selected["price"]), step=50.0
            )
            new_available = st.checkbox("Available for ordering", value=bool(selected["available"]))
            save_edit = st.form_submit_button("Save Changes", use_container_width=True)

            if save_edit:
                if not new_name.strip() or new_price <= 0:
                    st.error("Enter a valid name and a price greater than zero.")
                else:
                    with get_db() as conn:
                        conn.execute("""
                            UPDATE menu_items
                            SET name=?, category=?, price=?, available=?
                            WHERE id=?
                        """, (
                            new_name.strip(), new_category, new_price,
                            int(new_available), selected_id
                        ))
                    st.success("Menu item updated.")
                    st.rerun()

        with st.form("delete_menu_form"):
            st.warning("Deleting an item removes it from the current menu. Existing order records retain their saved item names and prices.")
            confirm_delete = st.checkbox("I confirm that I want to delete this menu item.")
            delete_button = st.form_submit_button("Delete Selected Item")

            if delete_button:
                if not confirm_delete:
                    st.error("Please tick the confirmation box first.")
                else:
                    with get_db() as conn:
                        conn.execute("DELETE FROM menu_items WHERE id=?", (selected_id,))
                    st.success("Menu item deleted.")
                    st.rerun()


# ============================================================
# ORDERS
# ============================================================
elif page == "🧾 Orders":
    heading("Orders", "Create customer orders and track their progress.")

    available_menu = read_df("""
        SELECT id, name, category, price
        FROM menu_items WHERE available=1 ORDER BY name
    """)

    if available_menu.empty:
        st.warning("There are no available menu items. Add items in Menu Management first.")
    else:
        st.subheader("Create a New Order")
        with st.form("create_order_form", clear_on_submit=True):
            customer = st.text_input("Customer name", placeholder="Enter customer name")
            st.caption("Enter the quantity for each item. Leave items at zero if not required.")

            order_lines = []
            columns = st.columns(2)

            for index, row in available_menu.iterrows():
                with columns[index % 2]:
                    quantity = st.number_input(
                        f"{row['name']} — {money(row['price'])}",
                        min_value=0, max_value=50, value=0, step=1,
                        key=f"order_qty_{int(row['id'])}"
                    )
                    if quantity > 0:
                        order_lines.append({
                            "id": int(row["id"]),
                            "name": str(row["name"]),
                            "price": float(row["price"]),
                            "quantity": int(quantity)
                        })

            total = sum(line["price"] * line["quantity"] for line in order_lines)
            st.markdown(f"### Order total: **{money(total)}**")
            create_order = st.form_submit_button("Create Order", use_container_width=True)

            if create_order:
                if not customer.strip():
                    st.error("Please enter the customer's name.")
                elif not order_lines:
                    st.error("Select at least one menu item.")
                else:
                    with get_db() as conn:
                        cursor = conn.execute("""
                            INSERT INTO orders (customer_name, order_date, total, status)
                            VALUES (?, ?, ?, 'Placed')
                        """, (
                            customer.strip(),
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            total
                        ))
                        order_id = cursor.lastrowid

                        for line in order_lines:
                            line_total = line["price"] * line["quantity"]
                            conn.execute("""
                                INSERT INTO order_items
                                (order_id, menu_item_id, item_name, quantity, unit_price, line_total)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                order_id, line["id"], line["name"],
                                line["quantity"], line["price"], line_total
                            ))

                    st.success(f"Order #{order_id} created successfully. Total: {money(total)}")
                    st.rerun()

    st.divider()
    st.subheader("Order History")

    orders = read_df("""
        SELECT id, customer_name, order_date, total, status
        FROM orders ORDER BY id DESC
    """)

    if orders.empty:
        st.info("No orders have been created yet.")
    else:
        display_orders = orders.rename(columns={
            "id": "Order #", "customer_name": "Customer",
            "order_date": "Date", "total": "Total (Rs.)", "status": "Order Status"
        })
        st.dataframe(display_orders, use_container_width=True, hide_index=True)

        st.subheader("Update Order Status")
        order_options = {
            f"Order #{int(row['id'])} — {row['customer_name']}": int(row["id"])
            for _, row in orders.iterrows()
        }
        chosen_order_label = st.selectbox("Select an order", list(order_options.keys()))
        chosen_order_id = order_options[chosen_order_label]
        chosen_order = orders[orders["id"] == chosen_order_id].iloc[0]

        statuses = ["Placed", "Preparing", "Ready", "Completed", "Cancelled"]
        current_status = str(chosen_order["status"] or "Placed")
        if current_status not in statuses:
            statuses.insert(0, current_status)

        with st.form("update_order_status_form"):
            new_status = st.selectbox(
                "New status", statuses, index=statuses.index(current_status)
            )
            update_status = st.form_submit_button("Update Status")

            if update_status:
                paid, balance, payment_state = payment_summary(
                    chosen_order_id, chosen_order["total"]
                )
                if new_status == "Cancelled" and paid > 0.009:
                    st.error("This order has received a payment. Refund handling is not available yet, so it cannot be cancelled.")
                elif current_status == "Cancelled" and new_status != "Cancelled":
                    st.error("Cancelled orders cannot be reopened in this prototype.")
                else:
                    with get_db() as conn:
                        conn.execute(
                            "UPDATE orders SET status=? WHERE id=?",
                            (new_status, chosen_order_id)
                        )
                    st.success("Order status updated.")
                    st.rerun()

        st.subheader("Order Details")
        detail_label = st.selectbox(
            "View order details",
            list(order_options.keys()),
            key="details_order_select"
        )
        detail_id = order_options[detail_label]
        details = get_order_items(detail_id)
        if details.empty:
            st.info("No item details were found for this order.")
        else:
            st.dataframe(details, use_container_width=True, hide_index=True)


# ============================================================
# PAYMENTS
# ============================================================
elif page == "💳 Payments":
    heading("Payments", "Record full or partial payments and monitor balances.")

    orders = read_df("""
        SELECT id, customer_name, order_date, total, status
        FROM orders ORDER BY id DESC
    """)

    outstanding_orders = []
    for _, row in orders.iterrows():
        paid, balance, payment_state = payment_summary(int(row["id"]), row["total"])
        if balance > 0.009 and str(row["status"]) != "Cancelled":
            outstanding_orders.append({
                "id": int(row["id"]),
                "customer": str(row["customer_name"]),
                "total": float(row["total"]),
                "paid": paid,
                "balance": balance
            })

    if not outstanding_orders:
        st.info("There are no outstanding orders to receive payment for.")
    else:
        order_labels = {
            f"Order #{o['id']} — {o['customer']} — Balance {money(o['balance'])}": o["id"]
            for o in outstanding_orders
        }

        with st.form("payment_form", clear_on_submit=True):
            chosen_label = st.selectbox("Select order", list(order_labels.keys()))
            chosen_id = order_labels[chosen_label]
            selected_order = next(o for o in outstanding_orders if o["id"] == chosen_id)

            st.write(f"Order total: **{money(selected_order['total'])}**")
            st.write(f"Already paid: **{money(selected_order['paid'])}**")
            st.write(f"Remaining balance: **{money(selected_order['balance'])}**")

            amount = st.number_input(
                "Payment amount (Rs.)",
                min_value=0.0,
                max_value=float(selected_order["balance"]),
                step=50.0
            )
            method = st.selectbox(
                "Payment method",
                ["Cash", "Card", "Bank Transfer", "JazzCash", "Easypaisa"]
            )
            save_payment = st.form_submit_button("Record Payment", use_container_width=True)

            if save_payment:
                if amount <= 0:
                    st.error("Payment amount must be greater than zero.")
                else:
                    # Recheck balance immediately before inserting payment.
                    paid_now, balance_now, _ = payment_summary(
                        chosen_id, selected_order["total"]
                    )
                    if amount > balance_now + 0.009:
                        st.error("This amount exceeds the current outstanding balance. Refresh and try again.")
                    else:
                        with get_db() as conn:
                            conn.execute("""
                                INSERT INTO payments
                                (order_id, amount, payment_method, payment_date)
                                VALUES (?, ?, ?, ?)
                            """, (
                                chosen_id, amount, method,
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ))
                        st.success(f"Payment of {money(amount)} recorded.")
                        st.rerun()

    st.divider()
    st.subheader("Payment History")
    payments = read_df("""
        SELECT p.id AS [Payment #], p.order_id AS [Order #],
               o.customer_name AS Customer, p.amount AS Amount,
               p.payment_method AS Method, p.payment_date AS Date
        FROM payments p
        LEFT JOIN orders o ON o.id = p.order_id
        ORDER BY p.id DESC
    """)

    if payments.empty:
        st.info("No payments have been recorded yet.")
    else:
        st.dataframe(payments, use_container_width=True, hide_index=True)
        st.download_button(
            "Download Payment History CSV",
            data=payments.to_csv(index=False).encode("utf-8"),
            file_name="cafeflow_payments.csv",
            mime="text/csv"
        )


# ============================================================
# ANALYTICS
# ============================================================
elif page == "📊 Analytics":
    heading("Analytics", "Understand sales, popular products and payment performance.")

    orders = read_df("SELECT * FROM orders")
    payments = read_df("SELECT * FROM payments")
    items = read_df("SELECT * FROM order_items")

    total_orders = len(orders)
    total_sales = float(orders["total"].sum()) if not orders.empty else 0
    total_received = float(payments["amount"].sum()) if not payments.empty else 0
    outstanding = max(total_sales - total_received, 0)

    a, b, c, d = st.columns(4)
    with a:
        metric_card("TOTAL ORDERS", str(total_orders))
    with b:
        metric_card("ORDER VALUE", money(total_sales))
    with c:
        metric_card("PAYMENTS RECEIVED", money(total_received))
    with d:
        metric_card("OUTSTANDING", money(outstanding))

    st.divider()
    left, right = st.columns(2)

    with left:
        st.subheader("Daily Order Sales")
        if not orders.empty:
            orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
            daily_sales = (
                orders.dropna(subset=["order_date"])
                .assign(Day=lambda x: x["order_date"].dt.date)
                .groupby("Day", as_index=False)["total"].sum()
                .rename(columns={"total": "Sales (Rs.)"})
                .set_index("Day")
            )
            if not daily_sales.empty:
                st.line_chart(daily_sales)
            else:
                st.info("No dated sales records available.")
        else:
            st.info("Create orders to see sales trends.")

    with right:
        st.subheader("Daily Payments")
        if not payments.empty:
            payments["payment_date"] = pd.to_datetime(payments["payment_date"], errors="coerce")
            daily_payments = (
                payments.dropna(subset=["payment_date"])
                .assign(Day=lambda x: x["payment_date"].dt.date)
                .groupby("Day", as_index=False)["amount"].sum()
                .rename(columns={"amount": "Payments (Rs.)"})
                .set_index("Day")
            )
            if not daily_payments.empty:
                st.bar_chart(daily_payments)
            else:
                st.info("No dated payment records available.")
        else:
            st.info("Record payments to see payment trends.")

    st.divider()
    left, right = st.columns(2)

    with left:
        st.subheader("Popular Menu Items")
        if not items.empty:
            popular = (
                items.groupby("item_name", as_index=False)
                .agg(Units_Sold=("quantity", "sum"), Revenue=("line_total", "sum"))
                .sort_values("Units_Sold", ascending=False)
                .rename(columns={
                    "item_name": "Item",
                    "Units_Sold": "Units Sold",
                    "Revenue": "Revenue (Rs.)"
                })
            )
            st.dataframe(popular, use_container_width=True, hide_index=True)
            st.bar_chart(popular.set_index("Item")[["Units Sold"]])
        else:
            st.info("No order items available yet.")

    with right:
        st.subheader("Payment Methods")
        if not payments.empty:
            methods = (
                payments.groupby("payment_method", as_index=False)["amount"].sum()
                .rename(columns={
                    "payment_method": "Method",
                    "amount": "Amount (Rs.)"
                })
                .set_index("Method")
            )
            st.bar_chart(methods)
        else:
            st.info("No payment data available yet.")

    st.divider()
    st.subheader("Order Payment Status")
    if not orders.empty:
        payment_rows = []
        for _, row in orders.iterrows():
            paid, balance, status = payment_summary(int(row["id"]), row["total"])
            payment_rows.append({"Payment Status": status, "Order": int(row["id"])})
        payment_status_df = pd.DataFrame(payment_rows)
        status_counts = (
            payment_status_df.groupby("Payment Status").size()
            .rename("Number of Orders")
        )
        st.bar_chart(status_counts)
    else:
        st.info("No orders available.")

    # Export report
    if not orders.empty:
        st.download_button(
            "Download Orders CSV",
            data=orders.to_csv(index=False).encode("utf-8"),
            file_name="cafeflow_orders.csv",
            mime="text/csv"
        )

    if not items.empty:
        st.download_button(
            "Download Order Items CSV",
            data=items.to_csv(index=False).encode("utf-8"),
            file_name="cafeflow_order_items.csv",
            mime="text/csv"
        )


# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("☕ CafeFlow | Cafe Management System | Portfolio Prototype")
