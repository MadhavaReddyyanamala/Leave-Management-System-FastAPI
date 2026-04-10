import streamlit as st
import requests
import pandas as pd
from datetime import date, datetime

# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LeaveDesk — HR Portal",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Global CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Layout ── */
[data-testid="stAppViewContainer"] { background: #f5f4f1; }
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5e3dc;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1300px; }

/* ── Brand ── */
.brand-block {
    display: flex; align-items: center; gap: 12px;
    padding: 0 0 20px; border-bottom: 1px solid #e5e3dc; margin-bottom: 20px;
}
.brand-icon {
    width: 38px; height: 38px; border-radius: 10px;
    background: #E6F1FB; border: 1px solid #B5D4F4;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.brand-name { font-size: 16px; font-weight: 700; color: #0C447C; line-height: 1.1; }
.brand-sub  { font-size: 11px; color: #888780; margin-top: 2px; }

/* ── Section label in sidebar ── */
.nav-section {
    font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #888780;
    padding: 6px 10px 4px; margin-top: 8px;
}

/* ── Metric cards ── */
.metric-row  { display: flex; gap: 14px; margin-bottom: 1.8rem; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 120px; background: #ffffff;
    border: 1px solid #e5e3dc; border-radius: 12px;
    padding: 16px 18px; position: relative; overflow: hidden;
}
.metric-card::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0;
    width: 4px; border-radius: 4px 0 0 4px;
}
.mc-blue::before  { background: #378ADD; }
.mc-amber::before { background: #BA7517; }
.mc-green::before { background: #639922; }
.mc-red::before   { background: #E24B4A; }
.metric-label { font-size: 11px; font-weight: 600; letter-spacing: 0.06em;
                text-transform: uppercase; color: #888780; margin-bottom: 6px; }
.metric-val   { font-size: 32px; font-weight: 700; line-height: 1; }
.mc-blue  .metric-val { color: #185FA5; }
.mc-amber .metric-val { color: #854F0B; }
.mc-green .metric-val { color: #3B6D11; }
.mc-red   .metric-val { color: #A32D2D; }

/* ── Status badges ── */
.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 99px; font-size: 12px; font-weight: 600;
}
.badge-pending  { background: #FAEEDA; color: #854F0B; }
.badge-approved { background: #EAF3DE; color: #3B6D11; }
.badge-rejected { background: #FCEBEB; color: #A32D2D; }

/* ── Info / warning boxes ── */
.info-box {
    background: #E6F1FB; border: 1px solid #B5D4F4;
    border-radius: 10px; padding: 12px 16px;
    color: #0C447C; font-size: 13px; margin-bottom: 1rem;
}
.warn-box {
    background: #FAEEDA; border: 1px solid #FAC775;
    border-radius: 10px; padding: 12px 16px;
    color: #633806; font-size: 13px; margin-bottom: 1rem;
}

/* ── Divider ── */
.section-divider { border: none; border-top: 1px solid #e5e3dc; margin: 1.4rem 0; }

/* ── Table tweaks ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
thead tr th { background: #f5f4f1 !important; font-size: 12px !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 13px !important; padding: 0.45rem 1.2rem !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { transform: translateY(-1px); }

/* ── Form controls ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    border-radius: 8px !important; font-size: 13.5px !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-weight: 600; font-size: 14px; border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# API helpers
# ──────────────────────────────────────────────
def api_get(path: str):
    try:
        r = requests.get(f"{API_URL}{path}", timeout=8)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Make sure the FastAPI server is running on port 8000."
    except Exception as e:
        return None, str(e)


def api_post(path: str, payload: dict):
    try:
        r = requests.post(f"{API_URL}{path}", json=payload, timeout=8)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return {"detail": "Cannot connect to API server."}, 503
    except Exception as e:
        return {"detail": str(e)}, 500


def api_put(path: str, payload: dict = None):
    try:
        r = requests.put(f"{API_URL}{path}", json=payload or {}, timeout=8)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return {"detail": "Cannot connect to API server."}, 503
    except Exception as e:
        return {"detail": str(e)}, 500


def api_delete(path: str):
    try:
        r = requests.delete(f"{API_URL}{path}", timeout=8)
        return r.json(), r.status_code
    except requests.exceptions.ConnectionError:
        return {"detail": "Cannot connect to API server."}, 503
    except Exception as e:
        return {"detail": str(e)}, 500


# ──────────────────────────────────────────────
# Shared utilities
# ──────────────────────────────────────────────
def days_between(start: str, end: str) -> int:
    try:
        d1 = datetime.strptime(str(start), "%Y-%m-%d")
        d2 = datetime.strptime(str(end), "%Y-%m-%d")
        return max(1, (d2 - d1).days + 1)
    except Exception:
        return 1


def metric_html(label: str, value: int, cls: str) -> str:
    return f"""
    <div class="metric-card {cls}">
        <div class="metric-label">{label}</div>
        <div class="metric-val">{value}</div>
    </div>"""


def status_badge(status: str) -> str:
    cls = {"Pending": "badge-pending", "Approved": "badge-approved",
           "Rejected": "badge-rejected"}.get(status, "badge-pending")
    return f'<span class="badge {cls}">{status}</span>'


def get_employees_cached():
    """Fetch employees, cache in session state."""
    if "employees" not in st.session_state:
        st.session_state.employees = []
    data, err = api_get("/employees/")
    if err:
        st.error(err)
        return []
    return data or []


def employee_selectbox(label: str, key: str, employees: list):
    if not employees:
        st.warning("No employees registered yet. Please add an employee first.")
        return None
    emp_map = {f"{e['id']} — {e['name']}": e["id"] for e in employees}
    choice = st.selectbox(label, list(emp_map.keys()), key=key)
    return emp_map[choice]


def build_leaves_df(leaves: list) -> pd.DataFrame:
    if not leaves:
        return pd.DataFrame()
    df = pd.DataFrame(leaves)
    df["days"] = df.apply(lambda r: days_between(r["start_date"], r["end_date"]), axis=1)
    cols = ["id", "employee_name", "leave_type", "start_date", "end_date", "days", "reason", "status"]
    existing = [c for c in cols if c in df.columns]
    return df[existing].rename(columns={
        "id": "ID", "employee_name": "Employee", "leave_type": "Type",
        "start_date": "From", "end_date": "To", "days": "Days",
        "reason": "Reason", "status": "Status"
    })


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-block">
        <div class="brand-icon">📋</div>
        <div>
            <div class="brand-name">LeaveDesk</div>
            <div class="brand-sub">HR Management Portal</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Role switcher — primary control
    st.markdown('<div class="nav-section">Role</div>', unsafe_allow_html=True)
    role = st.radio(
        "Active role",
        ["Employee", "Admin"],
        horizontal=True,
        key="role_toggle",
        label_visibility="collapsed",
    )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Show only the nav items relevant to the selected role
    if role == "Employee":
        st.markdown('<div class="nav-section">Employee</div>', unsafe_allow_html=True)
        emp_page = st.radio(
            "Employee menu",
            ["Register Employee", "Apply for Leave", "My Leaves"],
            label_visibility="collapsed",
        )
    else:
        emp_page = None
        st.markdown('<div class="nav-section">Admin</div>', unsafe_allow_html=True)
        st.radio("Admin menu", ["Admin Panel"], label_visibility="collapsed")


# ──────────────────────────────────────────────
# PAGES
# ──────────────────────────────────────────────

# ── EMPLOYEE PANEL ──────────────────────────
if role == "Employee":
    active = emp_page

    # ── Register Employee ─────────────────────
    if active == "Register Employee":
        st.title("Register Employee")
        st.caption("Add a new member to the workforce directory")
        st.write("")

        col_form, col_table = st.columns([1, 1.8], gap="large")

        with col_form:
            with st.form("reg_form", clear_on_submit=True):
                st.subheader("New Employee")
                name  = st.text_input("Full Name", placeholder="e.g. Ananya Krishnan")
                email = st.text_input("Work Email", placeholder="ananya@company.com")
                submitted = st.form_submit_button("✚  Register Employee", use_container_width=True, type="primary")

            if submitted:
                if not name.strip() or not email.strip():
                    st.error("Name and email are required.")
                else:
                    data, code = api_post("/employees/", {"name": name.strip(), "email": email.strip()})
                    if code == 200:
                        st.success(f"✅ **{name}** registered successfully!")
                    else:
                        detail = data.get("detail", data) if isinstance(data, dict) else data
                        st.error(f"Error: {detail}")

        with col_table:
            st.subheader("All Employees")
            employees, err = api_get("/employees/")
            if err:
                st.error(err)
            elif not employees:
                st.markdown('<div class="info-box">No employees registered yet.</div>', unsafe_allow_html=True)
            else:
                df = pd.DataFrame(employees)[["id", "name", "email"]].rename(
                    columns={"id": "ID", "name": "Name", "email": "Email"}
                )
                st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Apply for Leave ───────────────────────
    elif active == "Apply for Leave":
        st.title("Apply for Leave")
        st.caption("Submit a new leave request")
        st.write("")

        employees = get_employees_cached()

        with st.form("apply_form"):
            st.subheader("Leave Request")
            employee_id = employee_selectbox("Select Employee", "apply_emp_sel", employees)

            col1, col2 = st.columns(2)
            with col1:
                leave_type = st.selectbox("Leave Type", ["Sick Leave", "Casual Leave", "Annual Leave"])
            with col2:
                pass  # spacer

            col3, col4 = st.columns(2)
            with col3:
                start_date = st.date_input("Start Date", min_value=date.today())
            with col4:
                end_date = st.date_input("End Date", min_value=date.today())

            reason = st.text_area("Reason", placeholder="Briefly describe your reason for leave…", height=100)

            submitted = st.form_submit_button("Submit Request", use_container_width=True, type="primary")

        if submitted and employee_id:
            if not reason.strip():
                st.error("Please enter a reason for leave.")
            elif end_date < start_date:
                st.error("End date cannot be before start date.")
            else:
                duration = days_between(str(start_date), str(end_date))
                payload = {
                    "employee_id": employee_id,
                    "leave_type": leave_type,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "reason": reason.strip(),
                }
                data, code = api_post("/leaves/", payload)
                if code == 200:
                    st.success(f"✅ Leave request submitted for **{duration} day(s)** ({leave_type}).")
                else:
                    detail = data.get("detail", data) if isinstance(data, dict) else data
                    st.error(f"Error: {detail}")

    # ── My Leaves ─────────────────────────────
    elif active == "My Leaves":
        st.title("My Leaves")
        st.caption("View, edit, and manage your leave history")
        st.write("")

        employees = get_employees_cached()
        employee_id = employee_selectbox("Select Employee", "mine_emp_sel", employees)

        if employee_id:
            leaves, err = api_get(f"/employees/{employee_id}/leaves")
            if err:
                st.error(err)
            else:
                leaves = leaves or []

                # Metrics
                total    = len(leaves)
                pending  = sum(1 for l in leaves if l["status"] == "Pending")
                approved = sum(1 for l in leaves if l["status"] == "Approved")
                rejected = sum(1 for l in leaves if l["status"] == "Rejected")

                st.markdown(
                    '<div class="metric-row">'
                    + metric_html("Total", total, "mc-blue")
                    + metric_html("Pending", pending, "mc-amber")
                    + metric_html("Approved", approved, "mc-green")
                    + metric_html("Rejected", rejected, "mc-red")
                    + "</div>",
                    unsafe_allow_html=True,
                )

                if not leaves:
                    st.markdown('<div class="info-box">No leave requests found for this employee.</div>',
                                unsafe_allow_html=True)
                else:
                    # Filter tabs
                    tab_all, tab_pending, tab_approved, tab_rejected = st.tabs(
                        [f"All ({total})", f"Pending ({pending})",
                         f"Approved ({approved})", f"Rejected ({rejected})"]
                    )

                    def render_leaves_tab(filtered):
                        if not filtered:
                            st.info("No records in this category.")
                            return
                        df = build_leaves_df(filtered)
                        st.dataframe(df, use_container_width=True, hide_index=True)

                    with tab_all:
                        render_leaves_tab(leaves)
                    with tab_pending:
                        render_leaves_tab([l for l in leaves if l["status"] == "Pending"])
                    with tab_approved:
                        render_leaves_tab([l for l in leaves if l["status"] == "Approved"])
                    with tab_rejected:
                        render_leaves_tab([l for l in leaves if l["status"] == "Rejected"])

                    # Edit / Delete section
                    pending_leaves = [l for l in leaves if l["status"] == "Pending"]
                    if pending_leaves:
                        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
                        st.subheader("✏️  Edit / Delete Pending Request")

                        leave_labels = {
                            f"#{l['id']} — {l['leave_type']} ({l['start_date']} → {l['end_date']})": l
                            for l in pending_leaves
                        }
                        selected_label = st.selectbox("Select a pending leave", list(leave_labels.keys()))
                        sel = leave_labels[selected_label]

                        with st.expander("Edit this request", expanded=True):
                            with st.form("edit_form"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    new_type = st.selectbox(
                                        "Leave Type",
                                        ["Sick Leave", "Casual Leave", "Annual Leave"],
                                        index=["Sick Leave", "Casual Leave", "Annual Leave"].index(sel["leave_type"]),
                                    )
                                    new_start = st.date_input(
                                        "Start Date",
                                        value=datetime.strptime(sel["start_date"], "%Y-%m-%d").date(),
                                        min_value=date.today(),
                                    )
                                with col2:
                                    new_end = st.date_input(
                                        "End Date",
                                        value=datetime.strptime(sel["end_date"], "%Y-%m-%d").date(),
                                        min_value=date.today(),
                                    )
                                new_reason = st.text_area("Reason", value=sel["reason"], height=90)

                                col_save, col_del = st.columns(2)
                                with col_save:
                                    save = st.form_submit_button("💾  Save Changes", use_container_width=True, type="primary")
                                with col_del:
                                    delete = st.form_submit_button("🗑  Delete Request", use_container_width=True)

                            if save:
                                if new_end < new_start:
                                    st.error("End date cannot be before start date.")
                                else:
                                    payload = {
                                        "leave_type": new_type,
                                        "start_date": str(new_start),
                                        "end_date": str(new_end),
                                        "reason": new_reason.strip(),
                                    }
                                    data, code = api_put(f"/leaves/{sel['id']}", payload)
                                    if code == 200:
                                        st.success("✅ Leave updated successfully.")
                                        st.rerun()
                                    else:
                                        detail = data.get("detail", data) if isinstance(data, dict) else data
                                        st.error(f"Error: {detail}")

                            if delete:
                                data, code = api_delete(f"/leaves/{sel['id']}")
                                if code == 200:
                                    st.success("🗑️  Leave request deleted.")
                                    st.rerun()
                                else:
                                    detail = data.get("detail", data) if isinstance(data, dict) else data
                                    st.error(f"Error: {detail}")
                    else:
                        st.markdown('<div class="info-box">No pending requests available to edit or delete.</div>',
                                    unsafe_allow_html=True)


# ── ADMIN PANEL ──────────────────────────────
else:
    st.title("Admin Panel")
    st.caption("Review and action all employee leave requests")
    st.write("")

    leaves, err = api_get("/leaves/")
    if err:
        st.error(err)
    else:
        leaves = leaves or []

        # Metrics row
        total    = len(leaves)
        pending  = sum(1 for l in leaves if l["status"] == "Pending")
        approved = sum(1 for l in leaves if l["status"] == "Approved")
        rejected = sum(1 for l in leaves if l["status"] == "Rejected")

        st.markdown(
            '<div class="metric-row">'
            + metric_html("Total Requests", total, "mc-blue")
            + metric_html("Awaiting Review", pending, "mc-amber")
            + metric_html("Approved", approved, "mc-green")
            + metric_html("Rejected", rejected, "mc-red")
            + "</div>",
            unsafe_allow_html=True,
        )

        if not leaves:
            st.markdown('<div class="info-box">No leave requests in the system yet.</div>',
                        unsafe_allow_html=True)
        else:
            # Filter tabs
            tab_all, tab_pending, tab_approved, tab_rejected = st.tabs(
                [f"All ({total})", f"Pending ({pending})",
                 f"Approved ({approved})", f"Rejected ({rejected})"]
            )

            def admin_tab(filtered):
                if not filtered:
                    st.info("No records in this category.")
                    return
                df = build_leaves_df(filtered)
                st.dataframe(df, use_container_width=True, hide_index=True)

            with tab_all:
                admin_tab(leaves)
            with tab_pending:
                admin_tab([l for l in leaves if l["status"] == "Pending"])
            with tab_approved:
                admin_tab([l for l in leaves if l["status"] == "Approved"])
            with tab_rejected:
                admin_tab([l for l in leaves if l["status"] == "Rejected"])

            # Approve / Reject section
            pending_leaves = [l for l in leaves if l["status"] == "Pending"]
            if pending_leaves:
                st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
                st.subheader("⚖️  Approve / Reject a Request")

                leave_labels = {
                    f"#{l['id']} — {l['employee_name']} | {l['leave_type']} ({l['start_date']} → {l['end_date']})": l
                    for l in pending_leaves
                }
                selected_label = st.selectbox("Select pending request", list(leave_labels.keys()))
                sel = leave_labels[selected_label]

                # Detail card
                duration = days_between(sel["start_date"], sel["end_date"])
                with st.container(border=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Employee", sel["employee_name"])
                    c2.metric("Type", sel["leave_type"])
                    c3.metric("Duration", f"{duration} day(s)")
                    c4.metric("Status", sel["status"])
                    st.caption(f"📝 **Reason:** {sel['reason']}")
                    st.caption(f"📅 {sel['start_date']}  →  {sel['end_date']}")

                col_approve, col_reject, _ = st.columns([1, 1, 3])

                with col_approve:
                    if st.button("✅  Approve", use_container_width=True, type="primary"):
                        data, code = api_put(f"/leaves/{sel['id']}/approve")
                        if code == 200:
                            st.success(f"✅ Leave #{sel['id']} approved.")
                            st.rerun()
                        else:
                            detail = data.get("detail", data) if isinstance(data, dict) else data
                            st.error(f"Error: {detail}")

                with col_reject:
                    if st.button("❌  Reject", use_container_width=True):
                        data, code = api_put(f"/leaves/{sel['id']}/reject")
                        if code == 200:
                            st.warning(f"❌ Leave #{sel['id']} rejected.")
                            st.rerun()
                        else:
                            detail = data.get("detail", data) if isinstance(data, dict) else data
                            st.error(f"Error: {detail}")
            else:
                st.markdown('<div class="info-box">All caught up — no pending requests require action.</div>',
                            unsafe_allow_html=True)
