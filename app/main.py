import base64
import streamlit as st

from app.db import (
    add_task,
    clear_tasks,
    delete_task,
    get_tasks,
    init_db,
    toggle_done,
)

st.set_page_config(
    page_title="To Do List",
    page_icon="📝",
    layout="wide",
)

st.markdown(
    f"""
    <style>
        @font-face {{
            font-family: "ROG";
            src: url(
                "data:font/ttf;base64,{base64.b64encode(
                    open("assets/ROG.ttf", "rb").read()
                ).decode()}"
            ) format("truetype");
        }}

        .stApp,
        .stApp * {{
            font-family: "ROG" !important;
        }}

        header[data-testid="stHeader"],
        div[data-testid="stToolbar"] {{
            display: none;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

ss = st.session_state

if "initialized" not in ss:
    init_db()
    ss.initialized = True
    ss.task_input = ""
    ss.sort_by = "date"

st.subheader("Dodaj nowe zadanie")

with st.form("add_task_form", clear_on_submit=True):
    st.text_input("wpisz treść:", key="task_input")
    submitted = st.form_submit_button("DODAJ", use_container_width=True)

if submitted:
    desc = ss.task_input.strip()
    if desc:
        add_task(desc)
        st.rerun()

tasks = get_tasks()

st.subheader("Lista zadań")

sort_options = [
    "data utworzenia (rosnąco)",
    "data utworzenia (malejąco)",
    "treść zadania (A-Z)",
    "treść zadania (Z-A)",
]
filter_options = ["wszystkie", "ukończone", "nieukończone"]

col1, col2 = st.columns([2, 3])

with col1:
    st.selectbox("wyświetl:", filter_options, key="filter_by")

with col2:
    st.selectbox("sortuj wg:", sort_options, key="sort_by")

sort_config = {
    "data utworzenia (rosnąco)": (lambda x: x[3], False),
    "data utworzenia (malejąco)": (lambda x: x[3], True),
    "treść zadania (A-Z)": (lambda x: x[1].lower(), False),
    "treść zadania (Z-A)": (lambda x: x[1].lower(), True),
}

key_func, reverse = sort_config[ss.sort_by]

if ss.filter_by == "ukończone":
    tasks = [t for t in tasks if t[2] == 1]
elif ss.filter_by == "nieukończone":
    tasks = [t for t in tasks if t[2] == 0]

tasks = sorted(tasks, key=key_func, reverse=reverse)

if not tasks:
    st.info("Aktualnie nie masz żadnych zadań!")
else:
    for task_id, desc, done, created_at in tasks:
        c1, c2, c3, c4 = st.columns([1, 3, 19, 1])

        with c1:
            new_val = st.checkbox(
                "",
                value=bool(done),
                key=f"chk_{task_id}",
                label_visibility="collapsed",
            )

            if new_val != bool(done):
                toggle_done(task_id, new_val)
                st.rerun()

        with c2:
            st.caption("data utworzenia:")
            st.caption(created_at)

        with c3:
            st.subheader(desc)

        with c4:
            if st.button("🗑️", key=f"del_{task_id}"):
                delete_task(task_id)
                st.rerun()

    if st.button("WYCZYŚĆ WSZYSTKIE", use_container_width=True):
        clear_tasks()
        st.rerun()
