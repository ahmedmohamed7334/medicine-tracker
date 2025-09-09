import sqlite3
from datetime import datetime, date
import os
from typing import Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "medication_tracker.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create medication_records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medication_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    medication_key TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('taken', 'missed', 'pending', 'skipped')),
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date, medication_key)
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_date_medication 
                ON medication_records(date, medication_key)
            ''')
            
            conn.commit()
    
    def record_medication(self, date: date, medication_key: str, status: str) -> bool:
        """Record a medication status for a specific date"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO medication_records 
                    (date, medication_key, status, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (date, medication_key, status, datetime.now()))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error recording medication: {e}")
            return False
    
    def get_daily_status(self, date: date) -> Dict[str, str]:
        """Get the status of all medications for a specific date"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT medication_key, status 
                    FROM medication_records 
                    WHERE date = ?
                ''', (date,))
                
                results = cursor.fetchall()
                return {medication_key: status for medication_key, status in results}
        except Exception as e:
            print(f"Error getting daily status: {e}")
            return {}
    
    def get_medication_history(self, start_date: date, end_date: date) -> List[Dict]:
        """Get medication history for a date range"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT date, medication_key, status, timestamp
                    FROM medication_records 
                    WHERE date BETWEEN ? AND ?
                    ORDER BY date DESC, timestamp DESC
                ''', (start_date, end_date))
                
                results = cursor.fetchall()
                return [
                    {
                        'date': row[0],
                        'medication_key': row[1],
                        'status': row[2],
                        'timestamp': row[3]
                    }
                    for row in results
                ]
        except Exception as e:
            print(f"Error getting medication history: {e}")
            return []
    
    def get_compliance_rate(self, start_date: date, end_date: date, 
                           medication_key: Optional[str] = None) -> float:
        """Calculate compliance rate for a date range"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if medication_key:
                    cursor.execute('''
                        SELECT 
                            COUNT(*) as total,
                            SUM(CASE WHEN status = 'taken' THEN 1 ELSE 0 END) as taken
                        FROM medication_records 
                        WHERE date BETWEEN ? AND ? AND medication_key = ?
                    ''', (start_date, end_date, medication_key))
                else:
                    cursor.execute('''
                        SELECT 
                            COUNT(*) as total,
                            SUM(CASE WHEN status = 'taken' THEN 1 ELSE 0 END) as taken
                        FROM medication_records 
                        WHERE date BETWEEN ? AND ?
                    ''', (start_date, end_date))
                
                result = cursor.fetchone()
                total, taken = result[0], result[1] or 0
                
                return (taken / total * 100) if total > 0 else 0.0
        except Exception as e:
            print(f"Error calculating compliance rate: {e}")
            return 0.0
    
    def cleanup_old_records(self, days_to_keep: int = 90):
        """Clean up old records to prevent database from growing too large"""
        try:
            cutoff_date = date.today().replace(day=date.today().day - days_to_keep)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM medication_records 
                    WHERE date < ?
                ''', (cutoff_date,))
                deleted_count = cursor.rowcount
                conn.commit()
                return deleted_count
        except Exception as e:
            print(f"Error cleaning up old records: {e}")
            return 0
    
    def get_streak_info(self, medication_key: str = None) -> Dict:
        """Get current streak information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get recent records
                if medication_key:
                    cursor.execute('''
                        SELECT date, status
                        FROM medication_records 
                        WHERE medication_key = ?
                        ORDER BY date DESC
                        LIMIT 30
                    ''', (medication_key,))
                else:
                    cursor.execute('''
                        SELECT date, 
                               CASE 
                                   WHEN AVG(CASE WHEN status = 'taken' THEN 1.0 ELSE 0.0 END) = 1.0 
                                   THEN 'taken' 
                                   ELSE 'missed' 
                               END as daily_status
                        FROM medication_records 
                        GROUP BY date
                        ORDER BY date DESC
                        LIMIT 30
                    ''')
                
                records = cursor.fetchall()
                
                current_streak = 0
                for record_date, status in records:
                    if status == 'taken':
                        current_streak += 1
                    else:
                        break
                
                return {
                    'current_streak': current_streak,
                    'total_days_tracked': len(records)
                }
        except Exception as e:
            print(f"Error getting streak info: {e}")
            return {'current_streak': 0, 'total_days_tracked': 0}