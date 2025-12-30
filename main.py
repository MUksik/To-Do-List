import streamlit as st
from db import init_db, add_task, get_tasks, delete_task, toggle_done

st.set_page_config(page_title="📝 To-Do List", page_icon="📝", layout="centered")

st.markdown("""
<style>
body { background-color: #fef9f5; }
h1 { color: #6c5b7b; }
.stButton>button { background-color: #f67280; color: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("To-Do List")

# Inicjalizacja stanu
if 'initialized' not in st.session_state:
    init_db()
    st.session_state.initialized = True
    st.session_state.task_input = ""
    st.session_state.sort_by = "date"

# -----------------
# SORT + LICZNIK
# -----------------
st.subheader("🔧 Sortowanie")
col1, col2 = st.columns(2)

with col1:
    sort_option = st.selectbox("Sortuj wg:", ["date", "name", "status"], 
                              index=["date", "name", "status"].index(st.session_state.sort_by),
                              key="sort_select")
    if sort_option != st.session_state.sort_by:
        st.session_state.sort_by = sort_option
        st.rerun()

with col2:
    tasks = get_tasks()
    st.metric("Zadań", len(tasks))

# -----------------
# Dodawanie zadania
# -----------------
st.subheader("Dodaj nowe zadanie")
col1, col2 = st.columns([3,1])

with col1:
    new_task = st.text_input("Wpisz zadanie:", value=st.session_state.task_input, key="task_input_field")

with col2:
    if st.button("Dodaj", use_container_width=True):
        if new_task.strip():
            add_task(new_task)
            st.session_state.task_input = ""
            st.rerun()

st.markdown("---")

# -----------------
# Lista zadań
# -----------------
st.subheader("Twoje zadania")

tasks = get_tasks()

# SORT
if st.session_state.sort_by == "date":
    tasks = sorted(tasks, key=lambda x: x[0])
elif st.session_state.sort_by == "name":
    tasks = sorted(tasks, key=lambda x: x[1].lower())
elif st.session_state.sort_by == "status":
    tasks = sorted(tasks, key=lambda x: x[2], reverse=True)

if not tasks:
    st.info("Brak zadań!")
else:
    for task in tasks:
        task_id, desc, done = task
        col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
        
        with col1:
            st.checkbox(desc, value=bool(done), key=f"chk_{task_id}")
        
        with col2:
            st.caption(f"ID: {task_id}")
        
        with col3:
            pass
        
        with col4:
            if st.button("🗑️", key=f"del_{task_id}"):
                delete_task(task_id)
                st.rerun()

st.markdown("---")

# -----------------
# BUTTONY SZYBKIE (POPRAWIONE!)
# -----------------
st.subheader("⚡ Szybkie akcje")
col1, col2 = st.columns(2)


with col1:
    if st.button("🗑️ Wyczyść wszystkie", use_container_width=True, key="clear_all"):
        all_tasks = get_tasks()
        for task in all_tasks:
            delete_task(task[0])
        st.success("🗑️ Wszystkie zadania usunięte!")
        st.rerun()

with col2:
    if st.button("🔄 Odśwież", use_container_width=True, key="refresh"):
        st.rerun()
