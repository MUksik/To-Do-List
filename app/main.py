import base64
import streamlit as st
from app.i18n import DEFAULT_LANG, LANG_OPTIONS, t

from app.db import (
    add_task,
    clear_tasks,
    delete_task,
    get_tasks,
    init_db,
    toggle_done,
)

FILTER_OPTIONS = ("all", "done", "not_done")
SORT_OPTIONS = ("created_asc", "created_desc", "desc_asc", "desc_desc")


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
    ss.sort_by = "created_asc"
    ss.filter_by = "all"

if "lang" not in ss:
    ss.lang = DEFAULT_LANG

lang = ss.lang

header_column, language_column = st.columns([7, 2])

with header_column:
    st.subheader(t(lang, "add_task_header"))

with language_column:
    st.selectbox(
        t(lang, "choose_language"),
        LANG_OPTIONS,
        key="lang",
    )

with st.form("add_task_form", clear_on_submit=True):
    st.text_input(t(lang, "task_input_label"), key="task_input")
    submitted = st.form_submit_button(
        t(lang, "add_button_label"),
        use_container_width=True,
    )

if submitted:
    desc = ss.task_input.strip()
    if desc:
        add_task(desc)
        st.rerun()

tasks = get_tasks()

st.subheader(t(lang, "task_list_header"))

filter_column, sort_column = st.columns([2, 3])

with filter_column:
    st.selectbox(
        t(lang, "filter_label"),
        FILTER_OPTIONS,
        key="filter_by",
        format_func=lambda x: t(lang, f"filter_{x}"),
    )

with sort_column:
    st.selectbox(
        t(lang, "sort_label"),
        SORT_OPTIONS,
        key="sort_by",
        format_func=lambda x: t(lang, f"sort_{x}"),
    )

sort_config = {
    "created_asc": (lambda task: task[3], False),
    "created_desc": (lambda task: task[3], True),
    "desc_asc": (lambda task: task[1].lower(), False),
    "desc_desc": (lambda task: task[1].lower(), True),
}

key_func, reverse = sort_config[ss.sort_by]

if ss.filter_by == "done":
    tasks = [t for t in tasks if t[2] == 1]
elif ss.filter_by == "not_done":
    tasks = [t for t in tasks if t[2] == 0]

tasks = sorted(tasks, key=key_func, reverse=reverse)

if not tasks:
    st.info(t(lang, "empty_tasks_info"))
else:
    for task_id, desc, done, created_at in tasks:
        status_cell, date_cell, content_cell, delete_cell = st.columns([1, 3, 19, 1])

        with status_cell:
            new_val = st.checkbox(
                "",
                value=bool(done),
                key=f"chk_{task_id}",
                label_visibility="collapsed",
            )
            if new_val != bool(done):
                toggle_done(task_id, new_val)
                st.rerun()

        with date_cell:
            st.caption(t(lang, "created_at_label"))
            st.caption(created_at)

        with content_cell:
            st.subheader(desc)

        with delete_cell:
            if st.button(t(lang, "delete_icon_label"), key=f"del_{task_id}"):
                delete_task(task_id)
                st.rerun()

    if st.button(t(lang, "clear_all_button_label"), use_container_width=True):
        clear_tasks()
        st.rerun()
