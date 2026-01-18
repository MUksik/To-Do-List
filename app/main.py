import base64
import streamlit as st

from db import (
    init_db,
    add_task,
    get_tasks,
    delete_task,
    toggle_done,
    clear_tasks,
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

new_task = st.text_input(
    "wpisz treść:",
    value=ss.task_input,
)

if st.button("DODAJ", use_container_width=True) and new_task.strip():
    add_task(new_task.strip())
    ss.task_input = ""
    st.rerun()

tasks = get_tasks()

st.subheader("Lista zadań")

options = ["date", "name", "status"]
st.selectbox("sortuj wg:", options, key="sort_by")

sort_key = {
    "date": lambda x: x[3],
    "name": lambda x: x[1].lower(),
    "status": lambda x: x[2],
}[ss.sort_by]

tasks = sorted(
    tasks,
    key=sort_key,
    reverse=(ss.sort_by == "status"),
)

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
