import streamlit as st
import pandas as pd
import numpy as np
from database import get_connection, init_database, new_insert_query
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False
if "sidebar_action" not in st.session_state:
    st.session_state.sidebar_action = None
if "sucessful_write" not in st.session_state:
    st.session_state.successful_write = False

st.title("Smart Parking App")

init_database()
new_query = st.button("Make query")
quick_action_container = st.container(border = True)

col1, col2, col3 = quick_action_container.columns(3)
dummy_values = col1.button("set dummy values")

delete_all_button = col3.button("Clear Tables")
all_button = col2.button("See all tables")

def set_dummy_values():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""INSERT INTO users VALUES
                ('u101', 'Ashly'),
                ('u102', 'Jacob');""")
    cur.execute("""INSERT INTO vehicles VALUES
                ('u101', 'Honda', 'Civic', '7KX-4921', 'COMPACT'),
                ('u102', 'Ford', 'F-150', 'BQ3 8LZ', 'LARGE'),
                ('u102', 'Yamaha', 'YZF-R3', '4MX7K92', 'MOTORCYCLE');""")
    cur.execute("""INSERT INTO available_slots VALUES
                ('s201', 'A', 10, 'MOTORCYCLE'),
                ('s202', 'A', 11, 'COMPACT'),
                ('s203', 'A', 12, 'COMPACT'),
                ('s204', 'B', 15, 'LARGE'),
                ('s205', 'B', 16, 'LARGE');""")
    cur.execute("""INSERT INTO reservations VALUES
                ('t1001', 'u101', 's202', '7KX-4921', datetime('now'), datetime('now', '+6 hours')),
                ('t1002', 'u101', 's201', '4MX7K92', '2026-05-04 12:00:00', '2026-05-04 20:00:00'),
                ('t1003', 'u101', 's204', 'BQ3 8LZ', '2026-05-06 09:00:00', '2026-05-06 12:00:00');""")
    con.commit()
    cur.close()
    con.close()

def display_all_tables():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    tables = [row[0] for row in cur.fetchall()]

    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table} ", con)
        st.subheader(table)
        st.dataframe(df)
    cur.close()
    con.close()


def clear_all_tables():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    tables = [row[0] for row in cur.fetchall()]

    for table in tables:
        cur.execute(f"DELETE FROM {table}")
    con.commit()
    cur.close()
    con.close()



if new_query:
    if st.session_state.show_sidebar:
        st.session_state.show_sidebar = False
    else:
        st.session_state.show_sidebar = True

if st.session_state.show_sidebar:

    st.sidebar.header("New Query")
    
    insert_button = st.sidebar.button("Insert")
    update_button = st.sidebar.button("Update")
    delete_button = st.sidebar.button("Delete")
    if insert_button:
        st.session_state.sidebar_action = "insert"
    
    if st.session_state.sidebar_action == "insert":
        table = st.sidebar.selectbox("What table would you like to insert to?", ("users", "vehicles", "available_slots", "reservations"))

        if table == "users":
            insert_users_form = st.sidebar.form(key="insert_users_form")
            insert_users_form.header("Enter values")
            values = []
            user_id = insert_users_form.text_input("user_id", key = "user_id")
            values.append(user_id)
            username = insert_users_form.text_input("username", key = "username")
            values.append(username)
            submit = insert_users_form.form_submit_button("submit")

            if submit:
                error = new_insert_query("users", values)
                if error:
                    st.sidebar.error(error)
                else: 
                    st.success("Success")
                    
            #st.write(f"{user_id}")

        if table == "vehicles":
            insert_vehicles_form = st.sidebar.form(key="insert_vehicles_form")
            insert_vehicles_form.header("Enter values")
            values = []
            user_id = insert_vehicles_form.text_input("user_id", key = "user_id")
            values.append(user_id)
            make =  insert_vehicles_form.text_input("make")
            values.append(make)
            model =  insert_vehicles_form.text_input("model")
            values.append(model)
            plate = insert_vehicles_form.text_input("License plate")
            values.append(plate)
            v_size = insert_vehicles_form.text_input("Vehicle size")
            values.append(v_size)
            submit = insert_vehicles_form.form_submit_button("submit")

            if submit:
                
                error = new_insert_query("vehicles", values) 
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")

        if table == "available_slots":
            insert_slots_form = st.sidebar.form(key="insert_slots_form")
            insert_slots_form.header("Enter values")
            values = []
            slot_id = insert_slots_form.text_input("slot_id")
            values.append(slot_id)
            lot_id = insert_slots_form.text_input("lot_id")
            values.append(lot_id)
            slot_number = insert_slots_form.number_input("slot_number", min_value = 1, step = 1)
            values.append(slot_number)
            slot_type =  insert_slots_form.text_input("slot_type")
            values.append(slot_type)
            submit = insert_slots_form.form_submit_button("submit")
            
            if submit:
                
                error = new_insert_query("available_slots", values)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")

        if table == "reservations":
            insert_reservations_form = st.sidebar.form(key = "insert_reservations_form")
            insert_reservations_form.header("Enter values")
            values = []
            transaction_id = insert_reservations_form.text_input("transaction_id")
            values.append(transaction_id)
            user_id = insert_reservations_form.text_input("user_id")
            values.append(user_id)
            slot_id = insert_reservations_form.text_input("slot_id")
            values.append(slot_id)
            plate = insert_reservations_form.text_input("license plate")
            values.append(plate)
            time_start = insert_reservations_form.datetime_input("time_start")
            values.append(time_start)
            time_end = insert_reservations_form.datetime_input("time_end")
            values.append(time_end)
            submit = insert_reservations_form.form_submit_button("submit")

            if submit:
                
                error = new_insert_query("reservations", values)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")



    if update_button:
        st.session_state.sidebar_action = "update"
    
    if st.session_state.sidebar_action == "update":
         table = st.sidebar.selectbox("What table would you like to update?", ("users", "vehicles", "available_slots", "reservations"))


if dummy_values:
    set_dummy_values()
if all_button:
    display_all_tables()
if delete_all_button:
    clear_all_tables()


    
   
