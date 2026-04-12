import sqlite3

def get_connection():
    con = sqlite3.connect('parking.db')
    con.execute("PRAGMA foreign_keys = ON")
    return con


def init_database():
    con = get_connection()
    cur = con.cursor()
  
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
                user_id TEXT PRIMARY KEY,
                username TEXT   
                );
        """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS vehicles(
                user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
                make TEXT,
                model TEXT,
                plate TEXT PRIMARY KEY,
                v_size TEXT NOT NULL,
                CHECK (v_size IN ('COMPACT', 'LARGE', 'MOTORCYCLE'))
                );
            """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS available_slots (
                slot_id TEXT PRIMARY KEY,
                lot_id TEXT NOT NULL,
                slot_number NUMBER NOT NULL,
                slot_type TEXT NOT NULL,
                CHECK (slot_type IN ('COMPACT', 'LARGE', 'MOTORCYCLE'))
                );
            """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservations(
                transaction_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                slot_id TEXT NOT NULL REFERENCES available_slots(slot_id),
                vehicle_plate TEXT NOT NULL REFERENCES vehicles(plate) ON DELETE CASCADE,
                time_start TEXT DEFAULT (datetime('now')),
                time_end TEXT DEFAULT (datetime('now', '+8 hours')),
                check (time_end > time_start),
                check (
                (julianday(time_end) - julianday(time_start)) * 24 <= 48
                )
                );"""
                )
    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS no_overlap_reservation
                BEFORE INSERT ON reservations
                FOR EACH ROW
                BEGIN

                    -- Check for slot double-booking
                    SELECT RAISE(ABORT, 'Reservation times cannot overlap.')
                    WHERE EXISTS (
                        SELECT 1 FROM reservations
                        WHERE slot_id = NEW.slot_id
                        AND transaction_id != NEW.transaction_id
                        AND NEW.time_start < time_end
                        AND NEW.time_end > time_start
                    );
                
                    --Check for user overlapping booking
                    SELECT RAISE(ABORT, 'Users cannot have two reservations at the same time.')
                    WHERE EXISTS (
                        SELECT 1 FROM reservations
                        WHERE user_id = NEW.user_id
                        AND NEW.time_start < time_end
                        AND NEW.time_end > time_start
                    );
                END;
            """)
    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS ensure_vehicle_size_match
            BEFORE INSERT ON reservations
            FOR EACH ROW
            BEGIN
                --motorcyle only slots
                SELECT RAISE(ABORT, 'Only motorcycles can park in motorcycle slots.')
                WHERE EXISTS (
                    SELECT 1
                    FROM available_slots a
                    JOIN vehicles v ON v.plate = NEW.vehicle_plate
                    WHERE a.slot_id = NEW.slot_id
                    AND a.slot_type = 'MOTORCYCLE'
                    AND v.v_size != 'MOTORCYCLE'
                );
                -- compact slots
                SELECT RAISE(ABORT, 'Vehicle too big')
                WHERE EXISTS (
                    Select 1
                    FROM available_slots a
                    JOIN vehicles v ON v.plate = NEW.vehicle_plate
                    WHERE a.slot_id = NEW.slot_id
                    and a.slot_type = 'COMPACT'
                    AND v.v_size = 'LARGE' 
                );
            END;
                """)
    con.commit()
    cur.close()

def new_insert_query(table, values):
    con = get_connection()
    cur = con.cursor()
    placeholders = ",".join(["?"] * len(values))
    statement = f"INSERT INTO {table} VALUES ({placeholders})"
    try:
        
        cur.execute(statement, values)
        con.commit()
        return None #?
    except sqlite3.IntegrityError as e:
        return str(e)
    finally:
        cur.close()
        con.close()
   
    
