import streamlit as st
import pandas as pd
import numpy as np
from database import get_connection, init_database

st.title("Smart Parking App")

init_database()

col1, col2, col3 = st.columns(3)
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
        df = pd.read_sql_query(f"SELECT* FROM {table} ", con)
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


if dummy_values:
    set_dummy_values()
if all_button:
    display_all_tables()
if delete_all_button:
    clear_all_tables()


    
   
