import sqlite3
import json
from pathlib import Path
from typing import Dict, Optional

class Database:
    VALID_FIELDS = {
        'full_name', 'email', 'phone', 'location', 'professional_summary',
        'education_degree', 'education_institution', 'education_year', 'education_location',
        'experience_company', 'experience_position', 'experience_period',
        'experience_location', 'experience_description', 'skills', 'languages',
        'additional_info'
    }

    def __init__(self, db_name: str = "user_data.db"):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_data (
                    user_id INTEGER PRIMARY KEY,
                    full_name TEXT,
                    email TEXT,
                    phone TEXT,
                    location TEXT,
                    professional_summary TEXT,
                    education_degree TEXT,
                    education_institution TEXT,
                    education_year TEXT,
                    education_location TEXT,
                    experience_company TEXT,
                    experience_position TEXT,
                    experience_period TEXT,
                    experience_location TEXT,
                    experience_description TEXT,
                    skills TEXT,
                    languages TEXT,
                    additional_info TEXT
                )
            ''')
            conn.commit()

    def update_user_data(self, user_id: int, field: str, value: str):
        # Validate field name
        if field not in self.VALID_FIELDS:
            raise ValueError(f"Invalid field name: {field}")

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute('SELECT 1 FROM user_data WHERE user_id = ?', (user_id,))
            if not cursor.fetchone():
                # Create new user record with all fields as NULL
                fields = ['user_id'] + list(self.VALID_FIELDS)
                placeholders = ['?'] * (len(fields))
                query = f'INSERT INTO user_data ({", ".join(fields)}) VALUES ({", ".join(placeholders)})'
                values = [user_id] + [None] * len(self.VALID_FIELDS)
                cursor.execute(query, values)
            
            # Update the specified field using parameterized query
            cursor.execute('UPDATE user_data SET {} = ? WHERE user_id = ?'.format(field), (value, user_id))
            conn.commit()

    def get_user_data(self, user_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_data WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'full_name': row[1] or '',
                    'email': row[2] or '',
                    'phone': row[3] or '',
                    'location': row[4] or '',
                    'professional_summary': row[5] or '',
                    'education': {
                        'degree': row[6] or '',
                        'institution': row[7] or '',
                        'year': row[8] or '',
                        'location': row[9] or ''
                    },
                    'experience': {
                        'company': row[10] or '',
                        'position': row[11] or '',
                        'period': row[12] or '',
                        'location': row[13] or '',
                        'description': row[14] or ''
                    },
                    'skills': row[15] or '',
                    'languages': row[16] or '',
                    'additional_info': row[17] or ''
                }
            return None

    def clear_user_data(self, user_id: int):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_data WHERE user_id = ?', (user_id,))
            conn.commit()

    def mark_completed(self, user_id: int):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE user_data SET is_completed = 1 WHERE user_id = ?", (user_id,))
            conn.commit() 