# # create_temp_db.py
# from app import create_app
# from app.extensions import db
# from app.models import User, Role, Course, Enrollment, LectureSession, Assignment, Submission, Notification

# app = create_app()

# with app.app_context():
#     db.create_all()
#     # Bạn có thể thêm dữ liệu mẫu ở đây nếu cần


import pandas as pd
from app import create_app, db
from app.models import User

def generate_student_excel():
    app = create_app()
    app.app_context().push()

    # Query all students
    students = User.query.filter(User.roles.any(name='student')).all()

    # Prepare data for Excel
    data = {
        'username': [student.username for student in students],
        'fullname': [student.username for student in students],  # Placeholder for full names
        'dob': ['2000-01-01'] * len(students),  # Placeholder for date of birth
        'email': [student.email for student in students]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    df.to_excel('all_students.xlsx', index=False, engine='openpyxl')

    print("Excel file 'all_students.xlsx' created successfully.")

if __name__ == '__main__':
    generate_student_excel()