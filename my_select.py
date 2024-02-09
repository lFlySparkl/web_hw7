from sqlalchemy import create_engine, text

# Підключення до бази даних
engine = create_engine('postgresql://myuser:1111@localhost:5432/mydatabase')

def select_1():
    # Створення текстового об'єкту SQL-запиту
    # 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    sql_query = text("""
        SELECT s.id, s.student_name, AVG(e.grade) as avg_grade
        FROM students s
        JOIN estimates e ON s.id = e.student_id
        GROUP BY s.id, s.student_name
        ORDER BY avg_grade DESC
        LIMIT 5;
    """)
    return sql_query

def select_2():
    # 2. Знайти студента із найвищим середнім балом з певного предмета.
    sql_query = text("""
        SELECT s.id, s.student_name, AVG(e.grade) as avg_grade
        FROM students s
        JOIN estimates e ON s.id = e.student_id
        WHERE e.subject_id = (
            SELECT subject_id
            FROM estimates
            GROUP BY subject_id
            ORDER BY AVG(grade) DESC
            LIMIT 1
    )
    GROUP BY s.id, s.student_name
    ORDER BY avg_grade DESC
    LIMIT 1;
    """)
    return sql_query

def select_3():
    # 3. Знайти середній бал у групах з певного предмета.
    sql_query = text("""
        SELECT g.id as group_id, g.group_name, AVG(e.grade) as avg_grade
        FROM groups g
        JOIN students s ON g.id = s.group_id
        JOIN estimates e ON s.id = e.student_id
        GROUP BY g.id, g.group_name
        ORDER BY avg_grade DESC;
    """)
    return sql_query

def select_4():
    # 4. Знайти середній бал на потоці (по всій таблиці оцінок).
    sql_query = text("""
        SELECT AVG(grade) as avg_grade
        FROM estimates;
    """)
    return sql_query

def select_5():
    # 5. Знайти які курси читає певний викладач.
    sql_query = text("""
        SELECT t.id as teacher_id, t.teacher_name, s.subject_name
        FROM teachers t
        JOIN subjects s ON t.id = s.teacher_id;
    """)
    return sql_query

def select_6():
    # 6. Знайти список студентів у певній групі.
    group_id = input("Введіть потрібне значення 'group_id' - 1,2,3: ")  # Замініть на потрібне значення 1,2,3
    sql_query = text("""
        SELECT s.id as student_id, s.student_name, g.group_name
        FROM students s
        JOIN groups g ON s.group_id = g.id
        WHERE g.id = :group_id;
    """).bindparams(group_id=group_id)
    return sql_query

def select_7():
    # 7. Знайти оцінки студентів у окремій групі з певного предмета.
    group_id = input("Введіть потрібне значення 'group_id' - 1,2,3: ")  # Замініть на потрібне значення 1,2,3
    subject_id = input("Введіть потрібне значення 'subject_id' - 1,2,3,4,5: ") # Замініть на потрібне значення 1,2,3,4,5
    sql_query = text("""
        SELECT s.student_name, e.grade
        FROM students s
        JOIN estimates e ON s.id = e.student_id
        WHERE s.group_id = :group_id AND e.subject_id = :subject_id;
    """).bindparams(group_id=group_id, subject_id=subject_id)
    return sql_query

def select_8():
    # 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
    sql_query = text("""
        SELECT t.id as teacher_id, t.teacher_name, AVG(e.grade) as avg_grade
        FROM teachers t
        JOIN subjects s ON t.id = s.teacher_id
        JOIN estimates e ON s.id = e.subject_id
        GROUP BY t.id, t.teacher_name;
    """)
    return sql_query

def select_9():
    # 9. Знайти список курсів, які відвідує студент.
    sql_query = text("""
        SELECT s.student_name, sb.subject_name
        FROM students s
        JOIN estimates e ON s.id = e.student_id
        JOIN subjects sb ON e.subject_id = sb.id;
    """)
    return sql_query

def select_10():
    # 10. Список курсів, які певному студенту читає певний викладач.
    student_id = input("Введіть потрібне значення 'student_id' - 1-30: ")  # Замініть на потрібне значення 1-30
    teacher_id = input("Введіть потрібне значення 'teacher_id' - 1,2,3: ") # Замініть на потрібне значення 1,2,3
    sql_query = text("""
        SELECT sub.subject_name
        FROM subjects sub
        JOIN teachers t ON sub.teacher_id = t.id
        JOIN students s ON s.group_id = group_id
        WHERE s.id = :student_id AND t.id = :teacher_id;
    """).bindparams(student_id=student_id, teacher_id=teacher_id)
    return sql_query

def select_11():
    # 11. Середній бал, який певний викладач ставить певному студентові.
    student_id = input("Введіть потрібне значення 'student_id' - 1-30: ")  # Замініть на потрібне значення 1-30
    teacher_id = input("Введіть потрібне значення 'teacher_id' - 1,2,3: ") # Замініть на потрібне значення 1,2,3
    sql_query = text("""
        SELECT AVG(e.grade) as average_grade
        FROM estimates e
        JOIN subjects sub ON e.subject_id = sub.id
        JOIN teachers t ON sub.teacher_id = t.id
        JOIN students s ON e.student_id = s.id
        WHERE s.id = :student_id AND t.id = :teacher_id;
    """).bindparams(student_id=student_id, teacher_id=teacher_id)
    return sql_query

def select_12():
    # 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
    group_id = input("Введіть потрібне значення 'group_id' - 1,2,3: ")  # Замініть на потрібне значення 1,2,3
    subject_id = input("Введіть потрібне значення 'subject_id' - 1,2,3,4,5: ") # Замініть на потрібне значення 1,2,3,4,5
    sql_query = text("""
        SELECT e.grade, e.time_rating
        FROM estimates e
        JOIN subjects sub ON e.subject_id = sub.id
        JOIN students s ON e.student_id = s.id
        JOIN groups g ON s.group_id = g.id
        WHERE g.id = :group_id AND sub.id = :subject_id
        ORDER BY e.time_rating;
    """).bindparams(group_id=group_id, subject_id=subject_id)
    return sql_query

def main(number: int):
    if 1 <= number <= 12:
        select_function = globals()[f"select_{number}"]
        query = select_function()

        with engine.connect() as connection:
            result = connection.execute(query)

            for row in result:
                print(row)
    else:
        print("Number should be between 1 and 12.")

if __name__ == "__main__":
    main(1) # Для виклику функцій змініть тільки "1" на потрібний вам від 1 до 12.