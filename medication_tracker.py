import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import sqlite3
from database import DatabaseManager
from medication_config import MEDICATIONS
import pytz

# Page configuration
st.set_page_config(
    page_title="💊 Medicine Tracker",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def init_database():
    return DatabaseManager()

db = init_database()

# Custom CSS for better UI
st.markdown("""
<style>
    .medication-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .taken-card {
        border-left-color: #2ca02c !important;
        background-color: #e8f5e8;
    }
    .missed-card {
        border-left-color: #d62728 !important;
        background-color: #ffeaea;
    }
    .pending-card {
        border-left-color: #ff7f0e !important;
        background-color: #fff3e0;
    }
    .big-button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        margin: 5px 0;
    }
    .status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        text-align: center;
    }
    .taken { background-color: #d4edda; color: #155724; }
    .pending { background-color: #fff3cd; color: #856404; }
    .missed { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

def get_status_color(status):
    colors = {
        'taken': '🟢',
        'pending': '🟡', 
        'missed': '🔴'
    }
    return colors.get(status, '⚪')

def main():
    st.title("💊 Medicine Tracker")
    st.markdown("### Stay healthy by tracking your daily medications")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page:", ["Today's Medicines", "History", "Add Medicine"])
    
    if page == "Today's Medicines":
        today_page()
    elif page == "History":
        history_page()
    elif page == "Add Medicine":
        add_medicine_page()

def today_page():
    st.header("📅 Today's Medications")
    
    today = date.today()
    current_time = datetime.now().time()
    
    # Get today's medication status
    today_status = db.get_daily_status(today)
    
    # Create columns for layout
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.subheader("📊 Today's Summary")
        total_doses = sum(len(med['times']) for med in MEDICATIONS.values())
        taken_count = len([s for s in today_status.values() if s == 'taken'])
        pending_count = len([s for s in today_status.values() if s == 'pending'])
        missed_count = len([s for s in today_status.values() if s == 'missed'])
        
        st.metric("Total Doses", total_doses)
        st.metric("✅ Taken", taken_count)
        st.metric("⏳ Pending", pending_count)
        st.metric("❌ Missed", missed_count)
        
        # Progress bar
        progress = taken_count / total_doses if total_doses > 0 else 0
        st.progress(progress)
        st.write(f"{progress:.0%} Complete")
    
    with col1:
        st.subheader("💊 Your Medications")
        
        # Group medications by time
        morning_meds = []
        evening_meds = []
        
        for med_id, med_info in MEDICATIONS.items():
            for dose_time in med_info['times']:
                dose_key = f"{med_id}_{dose_time.strftime('%H:%M')}"
                status = today_status.get(dose_key, 'pending')
                
                # Determine if missed (2 hours past scheduled time)
                scheduled_datetime = datetime.combine(today, dose_time)
                current_datetime = datetime.now()
                if current_datetime > scheduled_datetime and status == 'pending':
                    time_diff = (current_datetime - scheduled_datetime).total_seconds() / 3600
                    if time_diff > 2:  # 2 hours grace period
                        status = 'missed'
                
                med_item = {
                    'id': med_id,
                    'name': med_info['name'],
                    'time': dose_time,
                    'status': status,
                    'dose_key': dose_key,
                    'instructions': med_info.get('instructions', '')
                }
                
                if dose_time.hour < 15:  # Before 3 PM is morning
                    morning_meds.append(med_item)
                else:
                    evening_meds.append(med_item)
        
        # Display morning medications
        if morning_meds:
            st.markdown("#### 🌅 Morning & Afternoon")
            for med in sorted(morning_meds, key=lambda x: x['time']):
                display_medication_card(med, today)
        
        # Display evening medications
        if evening_meds:
            st.markdown("#### 🌙 Evening & Night")
            for med in sorted(evening_meds, key=lambda x: x['time']):
                display_medication_card(med, today)

def display_medication_card(med, today):
    status = med['status']
    status_emoji = get_status_color(status)
    
    card_class = f"{status}-card"
    
    with st.container():
        st.markdown(f'<div class="medication-card {card_class}">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{med['name']}**")
            st.markdown(f"⏰ {med['time'].strftime('%I:%M %p')}")
            if med['instructions']:
                st.markdown(f"📝 {med['instructions']}")
        
        with col2:
            st.markdown(f'<div class="status-badge {status}">{status_emoji} {status.title()}</div>', 
                       unsafe_allow_html=True)
        
        with col3:
            if status == 'pending':
                if st.button("✅ Take", key=f"take_{med['dose_key']}", help="Mark as taken"):
                    db.record_medication(today, med['dose_key'], 'taken')
                    st.rerun()
            elif status == 'taken':
                if st.button("↩️ Undo", key=f"undo_{med['dose_key']}", help="Mark as not taken"):
                    db.record_medication(today, med['dose_key'], 'pending')
                    st.rerun()
            elif status == 'missed':
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅", key=f"take_missed_{med['dose_key']}", help="Mark as taken"):
                        db.record_medication(today, med['dose_key'], 'taken')
                        st.rerun()
                with col_b:
                    if st.button("⏭️", key=f"skip_{med['dose_key']}", help="Skip this dose"):
                        db.record_medication(today, med['dose_key'], 'skipped')
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def history_page():
    st.header("📈 Medication History")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today().replace(day=1))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    if start_date <= end_date:
        # Get history data
        history_data = db.get_medication_history(start_date, end_date)
        
        if history_data:
            df = pd.DataFrame(history_data)
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # Summary statistics
            st.subheader("📊 Summary Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            total_records = len(df)
            taken_records = len(df[df['status'] == 'taken'])
            missed_records = len(df[df['status'] == 'missed'])
            compliance_rate = (taken_records / total_records * 100) if total_records > 0 else 0
            
            col1.metric("Total Doses", total_records)
            col2.metric("Taken", taken_records)
            col3.metric("Missed", missed_records)
            col4.metric("Compliance Rate", f"{compliance_rate:.1f}%")
            
            # Display history table
            st.subheader("📋 Detailed History")
            
            # Format the dataframe for display
            display_df = df.copy()
            display_df['Medicine'] = display_df['medication_key'].apply(lambda x: x.split('_')[0])
            display_df['Time'] = display_df['medication_key'].apply(lambda x: x.split('_')[1])
            display_df['Status'] = display_df['status'].apply(lambda x: f"{get_status_color(x)} {x.title()}")
            display_df = display_df[['date', 'Medicine', 'Time', 'Status', 'timestamp']]
            display_df.columns = ['Date', 'Medicine', 'Time', 'Status', 'Recorded At']
            
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No medication records found for the selected date range.")
    else:
        st.error("Start date must be before or equal to end date.")

def add_medicine_page():
    st.header("➕ Add New Medicine")
    st.info("This is a preview of the add medicine feature. In the current version, medications are configured in the code.")
    
    st.subheader("🔧 Current Medications Configuration")
    
    for med_id, med_info in MEDICATIONS.items():
        with st.expander(f"💊 {med_info['name']}"):
            st.write(f"**Times:** {', '.join([t.strftime('%I:%M %p') for t in med_info['times']])}")
            if med_info.get('instructions'):
                st.write(f"**Instructions:** {med_info['instructions']}")
    
    st.markdown("---")
    st.markdown("**Note:** To add new medications, update the `medication_config.py` file and redeploy the application.")

if __name__ == "__main__":
    main()