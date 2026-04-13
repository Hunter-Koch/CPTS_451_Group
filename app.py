import streamlit as st
import pandas as pd
import numpy as np
from database import get_connection, init_database, new_insert_query, new_update_query, new_delete_querey
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

# to anyone reading this, yes there are a lot of unnecessary if statments and hard coded 
# operators. Ill refactor this later.
if st.session_state.show_sidebar:

    st.sidebar.header("New Query")
    
    lookup_button = st.sidebar.button("Lookup")
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

        if table == "users":
            with st.sidebar.container():
                columns = st.multiselect("select which columns to update", ["user_id", "username"])
            update_users_form = st.sidebar.form(key = "update_users_form")

            
            values = []

            if "user_id" in columns:
                user_id = update_users_form.text_input("user_id")
                values.append(user_id)
            if "username" in columns:
                username = update_users_form.text_input("username")
                values.append(username)
            where_exp = update_users_form.text_input("Where")
            
            submit = update_users_form.form_submit_button("submit")
            
            if submit:
                error = new_update_query("users", columns, values, where_exp)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")
        
        if table == "vehicles":
            with st.sidebar.container():
                columns = st.multiselect("select which columns to update", ["user_id", "make", "model", "plate", "v_size"])
            update_vehicle_form = st.sidebar.form(key = "update_vehicle_form")

            values = []

            if "user_id" in columns:
                user_id = update_vehicle_form.text_input("user_id")
                values.append(user_id)
            if "make" in columns:
                username = update_vehicle_form.text_input("username")
                values.append(username)
            if "model" in columns:
                model =  update_vehicle_form.text_input("model")
                values.append(model)
            if "plate" in columns:
                plate =  update_vehicle_form.text_input("plate")
                values.append(plate)
            if "v_size" in columns:
                v_size =  update_vehicle_form.text_input("v_size")
                values.append(v_size)
            
                
            where_exp = update_vehicle_form.text_input("Where")
            
            submit = update_vehicle_form.form_submit_button("submit")
            
            if submit:
                error = new_update_query("vehicles", columns, values, where_exp)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")
        
        if table == "available_slots":
            with st.sidebar.container():
                columns = st.multiselect("select which columns to update", ["slot_id", "lot_id", "slot_number", "slot_type"])
            update_slot_form = st.sidebar.form(key = "update_slot_form")

            values = []

            if "slot_id" in columns:
                slot_id = update_slot_form.text_input("slot_id")
                values.append(slot_id)
            if "lot_id" in columns:
                lot_id = update_slot_form.text_input("lot_id")
                values.append(lot_id)
            if "slot_number" in columns:
                slot_number =  update_slot_form.number_input("slot_number", min_value = 1, step = 1)
                values.append(slot_number)
            if "slot_type" in columns:
                slot_type =  update_slot_form.text_input("slot_type")
                values.append(slot_type)
            
                
            where_exp = update_slot_form.text_input("Where")
            
            submit = update_slot_form.form_submit_button("submit")
            
            if submit:
                error = new_update_query("available_slots", columns, values, where_exp)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")

        if table == "reservations":
            with st.sidebar.container():
                columns = st.multiselect("select which columns to update", ["transaction_id", "user_id", "slot_id", "vehicle_plate", "time_start", "time_end"])
            update_reservations_form = st.sidebar.form(key = "update_reservations_form")

            values = []

            if "transaction_id" in columns:
                transaction_id = update_reservations_form.text_input("transaction_id")
                values.append(transaction_id)
            if "user_id" in columns:
                user_id = update_reservations_form.text_input("user_id")
                values.append(user_id)
            if "slot_id" in columns:
                slot_id =  update_reservations_form.text_input("slot_id")
                values.append(slot_id)
            if "vehicle_plate" in columns:
                vehicle_plate =  update_reservations_form.text_input("vehicle_plate")
                values.append(vehicle_plate)
            if "time_start" in columns:
                time_start =  update_reservations_form.datetime_input("time_start")
                values.append(time_start)
            if "time_end" in columns:
                time_end =  update_reservations_form.datetime_input("time_end")
                values.append(time_end)
            
            
                
            where_exp = update_reservations_form.text_input("Where")
            
            submit = update_reservations_form.form_submit_button("submit")
            
            if submit:
                error = new_update_query("reservations", columns, values, where_exp)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")

    if delete_button:
        st.session_state.sidebar_action = "delete"

    if st.session_state.sidebar_action == "delete":
        table = st.sidebar.selectbox("What table would you like to delete from", ("users", "vehicles", "available_slots", "reservations"))

        delete_user_form = st.sidebar.form(key = "delete_user_form")
        if table == "users":
            where_exp = delete_user_form.text_input("Where")
            submit = delete_user_form.form_submit_button("submit")

            if submit:
                error = new_delete_querey("users", where_exp)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")

        if table == "vehicles":
            delete_vehicle_form = st.sidebar.form(key = "delete_vehicles_form")
            where_exp = delete_vehicle_form.text_input("Where")
            submit = delete_vehicle_form.form_submit_button("submit")


            if submit:
                error = new_delete_querey("vehicles", where_exp)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")
        
        if table == "available_slots":
            delete_slots_form = st.sidebar.form(key = "delete_slots_form")
            where_exp = delete_slots_form.text_input("Where")
            submit = delete_slots_form.form_submit_button("submit")
            

            if submit:
                error = new_delete_querey("available_slots", where_exp)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")
        
        if table == "reservations":
            delete_reservations_form = st.sidebar.form(key = "delete_reservations_form")
            where_exp = delete_reservations_form.text_input("Where")
            submit = delete_reservations_form.form_submit_button("submit")
            

            if submit:
                error = new_delete_querey("reservations", where_exp)
                if error: 
                    st.sidebar.error(error)
                else:
                    st.success("Success")



if dummy_values:
    set_dummy_values()
if all_button:
    display_all_tables()
if delete_all_button:
    clear_all_tables()


    
   
