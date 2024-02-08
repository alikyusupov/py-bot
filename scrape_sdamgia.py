import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('exams.db')

# Создание курсора
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exerciseText TEXT,
    exercise_number INTEGER,
    answer TEXT,
    work_type TEXT
)
""")

# Закрытие соединения с базой данных
conn.close()
