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

ADD_TASK_HEADER = "Dodaj nowe zadanie"
TASK_INPUT_LABEL = "wpisz treść:"
ADD_BUTTON_LABEL = "DODAJ"

TASK_LIST_HEADER = "Lista zadań"

FILTER_LABEL = "wyświetl:"
SORT_LABEL = "sortuj wg:"

EMPTY_TASKS_INFO = "Aktualnie nie masz żadnych zadań!"
CREATED_AT_LABEL = "data utworzenia:"

CLEAR_ALL_BUTTON_LABEL = "WYCZYŚĆ WSZYSTKIE"
DELETE_ICON_LABEL = "🗑️"

FILTER_ALL = "wszystkie"
FILTER_DONE = "ukończone"
FILTER_NOT_DONE = "nieukończone"
FILTER_OPTIONS = [FILTER_ALL, FILTER_DONE, FILTER_NOT_DONE]

SORT_CREATED_ASC = "data utworzenia (rosnąco)"
SORT_CREATED_DESC = "data utworzenia (malejąco)"
SORT_DESC_ASC = "treść zadania (A-Z)"
SORT_DESC_DESC = "treść zadania (Z-A)"
SORT_OPTIONS = [SORT_CREATED_ASC, SORT_CREATED_DESC, SORT_DESC_ASC, SORT_DESC_DESC]


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
    ss.sort_by = SORT_CREATED_ASC
    ss.filter_by = FILTER_ALL

st.subheader(ADD_TASK_HEADER)

with st.form("add_task_form", clear_on_submit=True):
    st.text_input(TASK_INPUT_LABEL, key="task_input")
    submitted = st.form_submit_button(ADD_BUTTON_LABEL, use_container_width=True)

if submitted:
    desc = ss.task_input.strip()
    if desc:
        add_task(desc)
        st.rerun()

tasks = get_tasks()

st.subheader(TASK_LIST_HEADER)

filter_column, sort_column = st.columns([2, 3])

with filter_column:
    st.selectbox(FILTER_LABEL, FILTER_OPTIONS, key="filter_by")

with sort_column:
    st.selectbox(SORT_LABEL, SORT_OPTIONS, key="sort_by")

sort_config = {
    SORT_CREATED_ASC: (lambda x: x[3], False),
    SORT_CREATED_DESC: (lambda x: x[3], True),
    SORT_DESC_ASC: (lambda x: x[1].lower(), False),
    SORT_DESC_DESC: (lambda x: x[1].lower(), True),
}

key_func, reverse = sort_config[ss.sort_by]

if ss.filter_by == FILTER_DONE:
    tasks = [t for t in tasks if t[2] == 1]
elif ss.filter_by == FILTER_NOT_DONE:
    tasks = [t for t in tasks if t[2] == 0]

tasks = sorted(tasks, key=key_func, reverse=reverse)

if not tasks:
    st.info(EMPTY_TASKS_INFO)
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
            st.caption(CREATED_AT_LABEL)
            st.caption(created_at)

        with content_cell:
            st.subheader(desc)

        with delete_cell:
            if st.button(DELETE_ICON_LABEL, key=f"del_{task_id}"):
                delete_task(task_id)
                st.rerun()

    if st.button(CLEAR_ALL_BUTTON_LABEL, use_container_width=True):
        clear_tasks()
        st.rerun()
