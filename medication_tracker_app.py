import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta, time
import json

# Page configuration
st.set_page_config(
    page_title="Medication Tracker",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    
    .medication-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .medication-name {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .medication-schedule {
        font-size: 1rem;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    .status-taken {
        background-color: #28a745;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .status-missed {
        background-color: #dc3545;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .status-pending {
        background-color: #ffc107;
        color: black;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .taken-button {
        background-color: #28a745 !important;
        color: white !important;
    }
    
    .missed-button {
        background-color: #dc3545 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

class DatabaseManager:
    def __init__(self, db_name="medication_tracker.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create medications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                schedule TEXT NOT NULL,
                times_per_day INTEGER NOT NULL,
                special_instructions TEXT
            )
        ''')
        
        # Create medication_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medication_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medication_id INTEGER,
                date TEXT NOT NULL,
                time_slot TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (medication_id) REFERENCES medications (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialize with default medications
        self.init_default_medications()
    
    def init_default_medications(self):
        """Initialize with the medications from your list"""
        medications = [
            ("Cervitam", "Twice per day", 2, ""),
            ("Tebonina Forte", "Once per day and once per night", 2, ""),
            ("Symbicort Inhaler", "Twice per day - once per day and once per night", 2, ""),
            ("Fast Freeze Gel", "Same as before", 2, "Topical application"),
            ("Movxir", "Same as before", 2, ""),
            ("Potassium Drink", "Same as before", 1, ""),
            ("Milga Advance", "For diabetics", 1, "Diabetes management"),
            ("Januvia", "After lunch", 1, "Take with food"),
            ("Lipostat", "Once per night", 1, "Before bedtime"),
            ("Controloc", "Once per morning", 1, "Before breakfast"),
            ("Dermovate Cream", "Once per day and once per night for 10 days", 2, "10-day course"),
            ("Sandocal Vitamin D", "Once per morning", 1, "With breakfast"),
            ("Magnesium", "Once per morning", 1, "")
        ]
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Check if medications already exist
        cursor.execute("SELECT COUNT(*) FROM medications")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.executemany(
                "INSERT INTO medications (name, schedule, times_per_day, special_instructions) VALUES (?, ?, ?, ?)",
                medications
            )
            conn.commit()
        
        conn.close()
    
    def get_all_medications(self):
        """Get all medications"""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM medications ORDER BY name", conn)
        conn.close()
        return df
    
    def log_medication(self, medication_id, date, time_slot, status):
        """Log medication intake"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Check if entry already exists
        cursor.execute('''
            SELECT id FROM medication_logs 
            WHERE medication_id = ? AND date = ? AND time_slot = ?
        ''', (medication_id, date, time_slot))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing entry
            cursor.execute('''
                UPDATE medication_logs 
                SET status = ?, timestamp = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, existing[0]))
        else:
            # Insert new entry
            cursor.execute('''
                INSERT INTO medication_logs (medication_id, date, time_slot, status)
                VALUES (?, ?, ?, ?)
            ''', (medication_id, date, time_slot, status))
        
        conn.commit()
        conn.close()
    
    def get_medication_status(self, medication_id, date, time_slot):
        """Get the status of a specific medication for a specific date and time slot"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT status FROM medication_logs 
            WHERE medication_id = ? AND date = ? AND time_slot = ?
            ORDER BY timestamp DESC LIMIT 1
        ''', (medication_id, date, time_slot))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else "pending"
    
    def get_daily_summary(self, date):
        """Get summary of all medications for a specific date"""
        conn = sqlite3.connect(self.db_name)
        
        query = '''
            SELECT m.name, m.times_per_day, m.schedule,
                   COALESCE(l.morning_status, 'pending') as morning_status,
                   COALESCE(l.evening_status, 'pending') as evening_status
            FROM medications m
            LEFT JOIN (
                SELECT medication_id,
                       MAX(CASE WHEN time_slot = 'morning' THEN status END) as morning_status,
                       MAX(CASE WHEN time_slot = 'evening' THEN status END) as evening_status
                FROM medication_logs
                WHERE date = ?
                GROUP BY medication_id
            ) l ON m.id = l.medication_id
            ORDER BY m.name
        '''
        
        df = pd.read_sql_query(query, conn, params=(date,))
        conn.close()
        return df

def main():
    # Initialize database
    db = DatabaseManager()
    
    # Header
    st.markdown('<div class="main-header">💊 Medication Tracker</div>', unsafe_allow_html=True)
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Sidebar for date selection
    with st.sidebar:
        st.header("Settings")
        selected_date = st.date_input("Select Date", datetime.now())
        selected_date_str = selected_date.strftime("%Y-%m-%d")
        
        if st.button("View History"):
            st.session_state.show_history = True
        
        if st.button("Today's Overview"):
            st.session_state.show_history = False
    
    # Main content
    if hasattr(st.session_state, 'show_history') and st.session_state.show_history:
        show_history_view(db, selected_date_str)
    else:
        show_daily_tracker(db, selected_date_str)

def show_daily_tracker(db, date):
    """Show the daily medication tracker interface"""
    st.subheader(f"Today's Medications - {date}")
    
    medications = db.get_all_medications()
    
    # Create columns for better mobile layout
    col1, col2 = st.columns([3, 1])
    
    for _, med in medications.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="medication-card">
                <div class="medication-name">{med['name']}</div>
                <div class="medication-schedule">{med['schedule']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create time slots based on times_per_day
            if med['times_per_day'] == 1:
                time_slots = ['morning']
            else:
                time_slots = ['morning', 'evening']
            
            # Create buttons for each time slot
            cols = st.columns(len(time_slots))
            
            for i, time_slot in enumerate(time_slots):
                with cols[i]:
                    current_status = db.get_medication_status(med['id'], date, time_slot)
                    
                    # Status display
                    if current_status == "taken":
                        st.markdown(f'<span class="status-taken">✓ {time_slot.title()}: Taken</span>', 
                                  unsafe_allow_html=True)
                    elif current_status == "missed":
                        st.markdown(f'<span class="status-missed">✗ {time_slot.title()}: Missed</span>', 
                                  unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="status-pending">⏳ {time_slot.title()}: Pending</span>', 
                                  unsafe_allow_html=True)
                    
                    # Action buttons
                    col_taken, col_missed = st.columns(2)
                    
                    with col_taken:
                        if st.button(f"✓ Taken", key=f"taken_{med['id']}_{time_slot}"):
                            db.log_medication(med['id'], date, time_slot, "taken")
                            st.rerun()
                    
                    with col_missed:
                        if st.button(f"✗ Missed", key=f"missed_{med['id']}_{time_slot}"):
                            db.log_medication(med['id'], date, time_slot, "missed")
                            st.rerun()
            
            st.markdown("---")

def show_history_view(db, date):
    """Show medication history"""
    st.subheader(f"Medication History - {date}")
    
    summary = db.get_daily_summary(date)
    
    if not summary.empty:
        # Create a visual summary
        for _, row in summary.iterrows():
            st.markdown(f"**{row['name']}**")
            
            if row['times_per_day'] == 1:
                status = row['morning_status']
                if status == "taken":
                    st.success("✓ Taken")
                elif status == "missed":
                    st.error("✗ Missed")
                else:
                    st.warning("⏳ Pending")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Morning:**")
                    if row['morning_status'] == "taken":
                        st.success("✓ Taken")
                    elif row['morning_status'] == "missed":
                        st.error("✗ Missed")
                    else:
                        st.warning("⏳ Pending")
                
                with col2:
                    st.write("**Evening:**")
                    if row['evening_status'] == "taken":
                        st.success("✓ Taken")
                    elif row['evening_status'] == "missed":
                        st.error("✗ Missed")
                    else:
                        st.warning("⏳ Pending")
            
            st.markdown("---")
    else:
        st.info("No medication records found for this date.")

if __name__ == "__main__":
    main()