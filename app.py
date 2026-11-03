import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta
from contextlib import contextmanager

st.set_page_config(page_title="CafeFlow 2.0", page_icon="☕", layout="wide")
DB_NAME = "cafeflow.db"
GOLD, COPPER, BG, TEXT = "#E7B77A", "#B87945", "#111315", "#F4EFE8"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def setup_database():
    # Safe, non-destructive setup: never drops or replaces existing tables.
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            category TEXT, price REAL NOT NULL, available INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT NOT NULL,
            order_date TEXT, total REAL NOT NULL, status TEXT DEFAULT 'Placed'
        );
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER,
            menu_item_id INTEGER, item_name TEXT, quantity INTEGER,
            unit_price REAL, line_total REAL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER,
            amount REAL NOT NULL, payment_method TEXT, payment_date TEXT,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );
        CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
        CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
        CREATE INDEX IF NOT EXISTS idx_payments_order ON payments(order_id);
        """)

setup_database()

def df(query, params=()):
    with get_db() as conn:
        return pd.read_sql_query(query, conn, params=params)

def scalar(query, params=()):
    result = df(query, params)
    return result.iloc[0, 0] if not result.empty else 0

def money(value):
    return f"Rs. {float(value or 0):,.2f}"

def payment_summary(order_id, total):
    paid = float(scalar("SELECT COALESCE(SUM(amount),0) FROM payments WHERE order_id=?", (int(order_id),)))
    balance = max(float(total or 0) - paid, 0)
    status = "Unpaid" if paid <= .009 else ("Paid" if balance <= .009 else "Partially Paid")
    return paid, balance, status

def orders_df():
    return df("SELECT id,customer_name,order_date,total,status FROM orders ORDER BY id DESC")

def items_df(order_id):
    return df("""SELECT item_name AS Item, quantity AS Quantity,
                 unit_price AS [Unit Price], line_total AS [Line Total]
                 FROM order_items WHERE order_id=? ORDER BY id""", (int(order_id),))

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
.stApp{background:#111315;color:#F4EFE8;font-family:'DM Sans',sans-serif}
[data-testid="stSidebar"]{background:#191B1D;border-right:1px solid #39332D}
[data-testid="stSidebar"] *{color:#F4EFE8}
.brand{font-family:'Playfair Display',serif;font-size:32px;color:#E7B77A;font-weight:700}
.brand-sub{font-size:10px;letter-spacing:2px;color:#A9A29A;margin-bottom:25px}
.eyebrow{font-size:10px;letter-spacing:2px;color:#C18D5D;font-weight:800}
.page-title{font-family:'Playfair Display',serif;font-size:38px;font-weight:700;color:#F4EFE8}
.page-subtitle{color:#A9A29A;margin-bottom:24px}
.metric-card,.surface{background:linear-gradient(145deg,#242321,#1A1D1F);border:1px solid #494035;border-radius:15px;padding:18px;min-height:125px}
.metric-label{font-size:11px;letter-spacing:1px;color:#B8AA98;font-weight:700}
.metric-value{font-size:24px;font-weight:800;color:#E7B77A;margin-top:12px;overflow-wrap:anywhere}
.metric-note{font-size:11px;color:#8E8982;margin-top:5px}
.stButton>button,.stFormSubmitButton>button{background:#B87945;color:white;border:0;border-radius:9px;min-height:42px;font-weight:700}
.stButton>button:hover,.stFormSubmitButton>button:hover{background:#D0925B;color:white}
.stDownloadButton>button{background:#302B25;color:#F4EFE8;border:1px solid #806345;border-radius:9px}
div[data-baseweb="input"] input,div[data-baseweb="select"]>div,div[data-baseweb="textarea"] textarea{background:#242729}
hr{border-color:#39332D}
</style>
""", unsafe_allow_html=True)

def heading(title, subtitle, label="CAFÉ OPERATIONS"):
    st.markdown(f'<div class="eyebrow">{label}</div><div class="page-title">{title}</div><div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def metric(label, value, note=""):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

def chart_style(fig, height=330):
    fig.update_layout(height=height,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),margin=dict(l=10,r=10,t=30,b=10))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#343638")
    return fig

with st.sidebar:
    st.markdown('<div class="brand">☕ CafeFlow</div><div class="brand-sub">CAFE MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
    page = st.radio("WORKSPACE", ["Overview","Menu Studio","Order Desk","Billing & Invoices","Payments","Analytics & Reports"])
    st.divider()
    st.caption("CafeFlow 2.0 · Portfolio prototype")
    st.caption(f"Today · {date.today():%d %b %Y}")

# DASHBOARD
if page == "Overview":
    heading("Good day. Here's your café.","A clear snapshot of orders, revenue and daily operations.","OVERVIEW")
    total_orders = int(scalar("SELECT COUNT(*) FROM orders"))
    menu_count = int(scalar("SELECT COUNT(*) FROM menu_items"))
    order_value = float(scalar("SELECT COALESCE(SUM(total),0) FROM orders"))
    received = float(scalar("SELECT COALESCE(SUM(amount),0) FROM payments"))
    today = date.today().isoformat()
    today_sales = float(scalar("SELECT COALESCE(SUM(total),0) FROM orders WHERE substr(order_date,1,10)=?",(today,)))
    today_count = int(scalar("SELECT COUNT(*) FROM orders WHERE substr(order_date,1,10)=?",(today,)))
    cols=st.columns(4)
    for col,(label,value,note) in zip(cols,[
        ("TODAY'S SALES",money(today_sales),f"{today_count} orders today"),
        ("TOTAL ORDERS",f"{total_orders:,}","All recorded orders"),
        ("MENU ITEMS",f"{menu_count:,}","Catalogue size"),
        ("PAYMENTS RECEIVED",money(received),"Collected to date")]):
        with col: metric(label,value,note)
    st.write("")
    left,right=st.columns([1.5,1])
    with left:
        st.subheader("Revenue performance")
        trend=df("""SELECT substr(order_date,1,10) Day,SUM(total) Revenue FROM orders
                    WHERE order_date>=? GROUP BY substr(order_date,1,10) ORDER BY Day""",
                 ((date.today()-timedelta(days=13)).isoformat(),))
        if trend.empty: st.info("Your revenue trend will appear after orders are recorded.")
        else:
            fig=px.area(trend,x="Day",y="Revenue",markers=True)
            fig.update_traces(line_color=GOLD,fillcolor="rgba(231,183,122,.14)",marker_color=COPPER)
            st.plotly_chart(chart_style(fig),use_container_width=True)
    with right:
        st.subheader("Order pipeline")
        status=df("SELECT status Status,COUNT(*) Orders FROM orders GROUP BY status")
        if status.empty: st.info("No orders yet.")
        else:
            fig=px.pie(status,names="Status",values="Orders",hole=.65)
            st.plotly_chart(chart_style(fig),use_container_width=True)
        metric("OUTSTANDING BALANCE",money(max(order_value-received,0)),"Order value less payments")
    st.subheader("Latest orders")
    recent=orders_df().head(8).rename(columns={"id":"Order #","customer_name":"Customer","order_date":"Date","total":"Total (Rs.)","status":"Status"})
    if recent.empty: st.info("Create your first order in Order Desk.")
    else: st.dataframe(recent,use_container_width=True,hide_index=True)

# MENU
elif page == "Menu Studio":
    heading("Menu Studio","Curate your catalogue, pricing and item availability.","PRODUCT MANAGEMENT")
    with st.expander("＋ Add a menu item"):
        with st.form("add_menu",clear_on_submit=True):
            a,b,c=st.columns([1.4,1,1])
            name=a.text_input("Item name",placeholder="e.g. Spanish Latte")
            category=b.selectbox("Category",["Coffee","Tea","Snacks","Desserts","Meals","Other"])
            price=c.number_input("Price (Rs.)",min_value=0.0,step=50.0)
            if st.form_submit_button("Add item",use_container_width=True):
                if not name.strip() or price<=0: st.error("Enter an item name and a price above zero.")
                else:
                    with get_db() as conn: conn.execute("INSERT INTO menu_items(name,category,price,available) VALUES(?,?,?,1)",(name.strip(),category,price))
                    st.success("Menu item added."); st.rerun()
    menu=df("SELECT id,name,category,price,available FROM menu_items ORDER BY name")
    if menu.empty: st.info("Your menu is empty. Add your first item above.")
    else:
        a,b,c=st.columns([1.4,1,1])
        search=a.text_input("Search menu")
        cats=["All"]+sorted(menu.category.dropna().astype(str).unique().tolist())
        cat=b.selectbox("Category",cats)
        availability=c.selectbox("Availability",["All","Available","Unavailable"])
        shown=menu.copy()
        if search: shown=shown[shown.name.str.contains(search,case=False,na=False)]
        if cat!="All": shown=shown[shown.category==cat]
        if availability!="All": shown=shown[shown.available==(1 if availability=="Available" else 0)]
        st.caption(f"Showing {len(shown)} of {len(menu)} items")
        cards=st.columns(3)
        for i,(_,r) in enumerate(shown.iterrows()):
            with cards[i%3]:
                state="AVAILABLE" if int(r.available) else "UNAVAILABLE"
                st.markdown(f'<div class="surface"><div class="eyebrow">{r.category or "OTHER"}</div><h3>{r["name"]}</h3><div class="metric-value">{money(r.price)}</div><div class="metric-note">{state} · ID {int(r.id)}</div></div>',unsafe_allow_html=True)
        st.divider(); st.subheader("Edit or remove an item")
        choices={f'{r["name"]} · ID {int(r.id)}':int(r.id) for _,r in menu.iterrows()}
        selected=st.selectbox("Choose item",list(choices),key="edit_item_choice")
        item=menu[menu.id==choices[selected]].iloc[0]
        with st.form("edit_menu"):
            x,y,z=st.columns([1.4,1,1])
            new_name=x.text_input("Name",str(item["name"]))
            categories=["Coffee","Tea","Snacks","Desserts","Meals","Other"]
            old_cat=str(item.category)
            new_cat=y.selectbox("Category",categories,index=categories.index(old_cat) if old_cat in categories else 5)
            new_price=z.number_input("Price",min_value=0.0,value=float(item.price),step=50.0)
            available=st.checkbox("Available for ordering",bool(item.available))
            if st.form_submit_button("Save changes"):
                if not new_name.strip() or new_price<=0: st.error("Enter a valid name and price.")
                else:
                    with get_db() as conn: conn.execute("UPDATE menu_items SET name=?,category=?,price=?,available=? WHERE id=?",(new_name.strip(),new_cat,new_price,int(available),int(item.id)))
                    st.success("Item updated."); st.rerun()
        with st.form("delete_menu"):
            confirm=st.checkbox("I confirm that I want to remove this item.")
            if st.form_submit_button("Delete item"):
                if not confirm: st.error("Please confirm deletion.")
                else:
                    with get_db() as conn: conn.execute("DELETE FROM menu_items WHERE id=?",(int(item.id),))
                    st.success("Item deleted."); st.rerun()

# ORDERS
elif page == "Order Desk":
    heading("Order Desk","Create customer orders and follow each order through its lifecycle.","ORDER OPERATIONS")
    menu=df("SELECT id,name,category,price FROM menu_items WHERE available=1 ORDER BY category,name")
    if menu.empty: st.warning("No available menu items. Add items in Menu Studio first.")
    else:
        with st.form("create_order",clear_on_submit=True):
            customer=st.text_input("Customer or table name")
            st.caption("Enter quantities. Leave items at zero if they are not required.")
            quantities={}
            for start in range(0,len(menu),3):
                cols=st.columns(3)
                for j,(_,r) in enumerate(menu.iloc[start:start+3].iterrows()):
                    with cols[j]:
                        quantities[int(r.id)]=st.number_input(f'{r["name"]} · {money(r.price)}',min_value=0,max_value=50,value=0,key=f"qty_{int(r.id)}")
            lines=[]
            for _,r in menu.iterrows():
                q=int(quantities.get(int(r.id),0))
                if q: lines.append((int(r.id),str(r["name"]),q,float(r.price)))
            total=sum(q*p for _,_,q,p in lines)
            st.markdown(f"### Order total: **{money(total)}**")
            if st.form_submit_button("Create customer order",use_container_width=True):
                if not customer.strip(): st.error("Enter a customer name.")
                elif not lines: st.error("Select at least one item.")
                else:
                    with get_db() as conn:
                        cur=conn.execute("INSERT INTO orders(customer_name,order_date,total,status) VALUES(?,?,?,'Placed')",(customer.strip(),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),total))
                        oid=cur.lastrowid
                        for mid,n,q,p in lines:
                            conn.execute("INSERT INTO order_items(order_id,menu_item_id,item_name,quantity,unit_price,line_total) VALUES(?,?,?,?,?,?)",(oid,mid,n,q,p,q*p))
                    st.success(f"Order #{oid} created · {money(total)}"); st.rerun()
    st.divider(); all_orders=orders_df(); st.subheader("Order register")
    if all_orders.empty: st.info("No orders yet.")
    else:
        a,b=st.columns([1.5,1])
        search=a.text_input("Find customer or order number")
        status=b.selectbox("Status filter",["All","Placed","Preparing","Ready","Completed","Cancelled"])
        visible=all_orders.copy()
        if search:
            visible=visible[visible.customer_name.astype(str).str.contains(search,case=False,na=False)|visible.id.astype(str).str.contains(search)]
        if status!="All": visible=visible[visible.status==status]
        st.dataframe(visible.rename(columns={"id":"Order #","customer_name":"Customer","order_date":"Date","total":"Total (Rs.)","status":"Status"}),use_container_width=True,hide_index=True)
        opts={f'Order #{int(r.id)} · {r.customer_name} · {money(r.total)}':int(r.id) for _,r in all_orders.iterrows()}
        st.subheader("Update order status")
        label=st.selectbox("Select order",list(opts),key="status_order")
        oid=opts[label]; selected=all_orders[all_orders.id==oid].iloc[0]
        statuses=["Placed","Preparing","Ready","Completed","Cancelled"]
        current=str(selected.status or "Placed")
        if current not in statuses: statuses.insert(0,current)
        with st.form("status_form"):
            new_status=st.selectbox("New status",statuses,index=statuses.index(current))
            if st.form_submit_button("Update status"):
                paid,_,_=payment_summary(oid,selected.total)
                if new_status=="Cancelled" and paid>.009: st.error("This order has payments. Refund handling is not available, so it cannot be cancelled.")
                elif current=="Cancelled" and new_status!="Cancelled": st.error("Cancelled orders cannot be reopened in this prototype.")
                else:
                    with get_db() as conn: conn.execute("UPDATE orders SET status=? WHERE id=?",(new_status,oid))
                    st.success("Status updated."); st.rerun()
        detail=st.selectbox("View order items",list(opts),key="detail_order")
        detail_id=opts[detail]; details=items_df(detail_id)
        if not details.empty:
            st.subheader("Order details"); st.dataframe(details,use_container_width=True,hide_index=True)
            r=all_orders[all_orders.id==detail_id].iloc[0]; paid,balance,_=payment_summary(detail_id,r.total)
            x,y,z=st.columns(3)
            with x: metric("ORDER TOTAL",money(r.total))
            with y: metric("PAID",money(paid))
            with z: metric("BALANCE",money(balance))

# BILLING
elif page == "Billing & Invoices":
    heading("Billing & Invoices","Review itemised bills, payment status and balances due.","BILLING")
    all_orders=orders_df()
    if all_orders.empty: st.info("Create an order first.")
    else:
        opts={f'Invoice #{int(r.id)} · {r.customer_name}':int(r.id) for _,r in all_orders.iterrows()}
        label=st.selectbox("Choose invoice",list(opts)); oid=opts[label]
        r=all_orders[all_orders.id==oid].iloc[0]; items=items_df(oid)
        paid,balance,pstatus=payment_summary(oid,r.total)
        st.markdown(f'<div class="surface"><div class="eyebrow">CAFÉFLOW · CUSTOMER INVOICE</div><div class="page-title">INVOICE #{oid}</div><p>Customer: {r.customer_name} &nbsp; | &nbsp; Date: {r.order_date}</p><p>Order status: <b>{r.status}</b> &nbsp; | &nbsp; Payment status: <b>{pstatus}</b></p></div>',unsafe_allow_html=True)
        st.write("")
        if items.empty: st.info("No item details recorded for this order.")
        else:
            st.dataframe(items,use_container_width=True,hide_index=True)
            export=items.copy(); export["Order #"]=oid; export["Customer"]=r.customer_name
            export["Invoice Total (Rs.)"]=float(r.total)
            st.download_button("Download itemised invoice CSV",export.to_csv(index=False).encode("utf-8"),file_name=f"cafeflow_invoice_{oid}.csv",mime="text/csv")
        a,b,c=st.columns(3)
        with a: metric("INVOICE TOTAL",money(r.total))
        with b: metric("AMOUNT PAID",money(paid))
        with c: metric("BALANCE DUE",money(balance))
        st.caption("For a printable view, use your browser's Print command (Ctrl + P).")

# PAYMENTS
elif page == "Payments":
    heading("Payments","Record collections, monitor balances and review transactions.","FINANCE")
    all_orders=orders_df(); awaiting=[]
    for _,r in all_orders.iterrows():
        paid,balance,_=payment_summary(r.id,r.total)
        if balance>.009 and r.status!="Cancelled":
            awaiting.append({"id":int(r.id),"customer":r.customer_name,"total":float(r.total),"paid":paid,"balance":balance})
    received=float(scalar("SELECT COALESCE(SUM(amount),0) FROM payments"))
    order_value=float(scalar("SELECT COALESCE(SUM(total),0) FROM orders WHERE status!='Cancelled'"))
    a,b,c=st.columns(3)
    with a: metric("COLLECTED",money(received))
    with b: metric("OUTSTANDING",money(max(order_value-received,0)))
    with c: metric("AWAITING PAYMENT",str(len(awaiting)))
    st.divider(); st.subheader("Record a payment")
    if not awaiting: st.success("No outstanding orders.")
    else:
        opts={f'Order #{o["id"]} · {o["customer"]} · Due {money(o["balance"])}':o["id"] for o in awaiting}
        with st.form("payment_form",clear_on_submit=True):
            label=st.selectbox("Order",list(opts)); oid=opts[label]
            chosen=next(o for o in awaiting if o["id"]==oid)
            x,y=st.columns(2)
            with x: st.write(f'Order total: **{money(chosen["total"])}**'); st.write(f'Already paid: **{money(chosen["paid"])}**')
            with y: st.write(f'Remaining: **{money(chosen["balance"])}**')
            amount=st.number_input("Amount received (Rs.)",min_value=0.0,max_value=float(chosen["balance"]),step=50.0)
            method=st.selectbox("Payment method",["Cash","Card","Bank Transfer","JazzCash","Easypaisa"])
            if st.form_submit_button("Record transaction",use_container_width=True):
                _,latest,_=payment_summary(oid,chosen["total"])
                if amount<=0: st.error("Payment must be greater than zero.")
                elif amount>latest+.009: st.error("Amount exceeds the current balance. Refresh and retry.")
                else:
                    with get_db() as conn: conn.execute("INSERT INTO payments(order_id,amount,payment_method,payment_date) VALUES(?,?,?,?)",(oid,amount,method,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    st.success("Payment recorded."); st.rerun()
    st.divider(); st.subheader("Transaction history")
    payments=df("""SELECT p.id AS [Payment #],p.order_id AS [Order #],o.customer_name AS Customer,
                   p.amount AS [Amount (Rs.)],p.payment_method AS Method,p.payment_date AS Date
                   FROM payments p LEFT JOIN orders o ON o.id=p.order_id ORDER BY p.id DESC""")
    if payments.empty: st.info("No transactions yet.")
    else:
        st.dataframe(payments,use_container_width=True,hide_index=True)
        st.download_button("Export transactions CSV",payments.to_csv(index=False).encode("utf-8"),file_name="cafeflow_transactions.csv",mime="text/csv")

# ANALYTICS
elif page == "Analytics & Reports":
    heading("Analytics & Reports","Explore sales trends, product performance and payment behaviour.","BUSINESS INTELLIGENCE")
    all_orders=orders_df(); payments=df("SELECT * FROM payments"); items=df("SELECT * FROM order_items")
    if all_orders.empty: st.info("Analytics will appear after you record orders.")
    else:
        dated=all_orders.copy(); dated["day"]=pd.to_datetime(dated.order_date,errors="coerce").dt.date
        valid=dated.day.dropna()
        low,high=(min(valid),max(valid)) if not valid.empty else (date.today(),date.today())
        a,b=st.columns(2); start=a.date_input("From",low,min_value=low,max_value=high); end=b.date_input("To",high,min_value=low,max_value=high)
        if start>end: st.error("Start date must be on or before end date."); filtered=dated.iloc[0:0].copy()
        else: filtered=dated[dated.day.between(start,end)&(dated.status!="Cancelled")].copy()
        ids=filtered.id.tolist()
        fp=payments[payments.order_id.isin(ids)] if not payments.empty else payments
        fi=items[items.order_id.isin(ids)] if not items.empty else items
        sales=float(filtered.total.sum()) if not filtered.empty else 0
        collected=float(fp.amount.sum()) if not fp.empty else 0
        a,b,c,d=st.columns(4)
        with a: metric("ORDERS",str(len(filtered)))
        with b: metric("SALES VALUE",money(sales))
        with c: metric("PAYMENTS",money(collected))
        with d: metric("BALANCE",money(max(sales-collected,0)))
        st.divider(); left,right=st.columns(2)
        with left:
            st.subheader("Revenue trend")
            if filtered.empty: st.info("No sales in this period.")
            else:
                daily=filtered.assign(Day=filtered.day.astype(str)).groupby("Day",as_index=False).total.sum()
                fig=px.area(daily,x="Day",y="total",markers=True)
                fig.update_traces(line_color=GOLD,fillcolor="rgba(231,183,122,.14)",marker_color=COPPER)
                fig.update_layout(yaxis_title="Revenue (Rs.)",xaxis_title="")
                st.plotly_chart(chart_style(fig),use_container_width=True)
        with right:
            st.subheader("Payment method mix")
            if fp.empty: st.info("No payments in this period.")
            else:
                methods=fp.groupby("payment_method",as_index=False).amount.sum()
                fig=px.pie(methods,names="payment_method",values="amount",hole=.62)
                st.plotly_chart(chart_style(fig),use_container_width=True)
        st.divider(); left,right=st.columns(2)
        with left:
            st.subheader("Best-selling items")
            if fi.empty: st.info("No item sales in this period.")
            else:
                popular=fi.groupby("item_name",as_index=False).agg(Units=("quantity","sum"),Revenue=("line_total","sum")).sort_values("Units")
                fig=px.bar(popular,x="Units",y="item_name",orientation="h",text="Units")
                fig.update_traces(marker_color=COPPER,textposition="outside")
                fig.update_layout(xaxis_title="Units sold",yaxis_title="")
                st.plotly_chart(chart_style(fig,max(300,42*len(popular))),use_container_width=True)
        with right:
            st.subheader("Payment status")
            if filtered.empty: st.info("No orders in this period.")
            else:
                rows=[]
                for _,r in filtered.iterrows():
                    _,_,status=payment_summary(r.id,r.total); rows.append({"Status":status})
                status_df=pd.DataFrame(rows).value_counts("Status").rename("Orders").reset_index()
                fig=px.pie(status_df,names="Status",values="Orders",hole=.62)
                st.plotly_chart(chart_style(fig),use_container_width=True)
        st.divider(); st.subheader("Sales report")
        if filtered.empty: st.info("No report rows in this period.")
        else:
            report=filtered[["id","customer_name","order_date","total","status"]].rename(columns={"id":"Order #","customer_name":"Customer","order_date":"Date","total":"Order value (Rs.)","status":"Order status"})
            st.dataframe(report,use_container_width=True,hide_index=True)
            st.download_button("Download sales report CSV",report.to_csv(index=False).encode("utf-8"),file_name="cafeflow_sales_report.csv",mime="text/csv")

st.markdown("---")
st.caption("☕ CafeFlow 2.0 · Café operations, billing and business intelligence · Portfolio prototype")
!grep -oE 'https://[a-zA-Z0-9.-]+\.trycloudflare\.com' /content/cloudflared.log | tail -1
