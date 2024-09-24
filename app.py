import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from model import db, Department, Course, Instructor, Student, Exam, Enrollment, HOD
from datetime import datetime

app = Flask(__name__)
app.secret_key = '2003'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

INSTRUCTOR_PASSWORD = 'instructor123'
ADMIN_PASSWORD = 'admin123'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/admin', methods=['GET', 'POST'])
def admin_auth():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid password. Please try again.'
            return render_template('admin_panel.html', error=error)
    return render_template('admin_panel.html', error=None)

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/manage/students', methods=['GET', 'POST'])
def admin_manage_students():
    students = Student.query.all()
    if request.method == 'POST':
        name = request.form['name']
        new_student = Student(name=name)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('admin_manage_students'))
    return render_template('manage_students.html', students=students)

@app.route('/admin/manage/hods', methods=['GET', 'POST'])
def admin_manage_hods():
    hods = HOD.query.all()  
    departments = Department.query.all() 
    instructors = Instructor.query.all()  
    if request.method == 'POST':
        department_id = request.form['department_id']
        instructor_id = request.form['instructor_id']
        new_hod = HOD(department_id=department_id, instructor_id=instructor_id)
        db.session.add(new_hod)
        db.session.commit()
        return redirect(url_for('admin_manage_hods'))
    return render_template('manage_hods.html', hods=hods, departments=departments, instructors=instructors)

@app.route('/admin/manage_courses', methods=['GET', 'POST'])
def admin_manage_courses():
    courses = Course.query.all()
    departments = Department.query.all() 
    instructors = Instructor.query.all() 

    if request.method == 'POST':
        name = request.form['name']
        department_id = request.form['department_id']
        instructor_id = request.form['instructor_id']

        new_course = Course(name=name, department_id=department_id, instructor_id=instructor_id)

        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for('admin_manage_courses'))
    return render_template('manage_courses.html', courses=courses, departments=departments, instructors=instructors)

@app.route('/admin/manage/departments', methods=['GET', 'POST'])
def admin_manage_departments():
    departments = Department.query.all()
    instructors = Instructor.query.all()  
    if request.method == 'POST':
        name = request.form['name']
        head_id = request.form.get('head_id', None)
        new_department = Department(name=name, head_id=head_id)
        db.session.add(new_department)
        db.session.commit()
        return redirect(url_for('admin_manage_departments'))
    return render_template('manage_departments.html', departments=departments, instructors=instructors)


@app.route('/admin/manage/instructors', methods=['GET', 'POST'])
def admin_manage_instructors():
    instructors = Instructor.query.all()
    if request.method == 'POST':
        name = request.form['name']
        new_instructor = Instructor(name=name)
        db.session.add(new_instructor)
        db.session.commit()
        return redirect(url_for('admin_manage_instructors'))
    return render_template('manage_instructors.html', instructors=instructors)

@app.route('/instructors', methods=['GET', 'POST'])
def instructor_auth():
    if request.method == 'POST':
        password = request.form['password']
        if password == INSTRUCTOR_PASSWORD:
            return redirect(url_for('instructor_dashboard'))
        else:
            error = 'Invalid password. Please try again.'
            return render_template('instructors.html', error=error)
    return render_template('instructors.html', error=None)

@app.route('/instructors/dashboard')
def instructor_dashboard():
    return render_template('instructor_dashboard.html')

@app.route('/instructors/manage/students', methods=['GET', 'POST'])
def instructor_manage_students():
    students = Student.query.all()
    if request.method == 'POST':
        name = request.form['name']
        new_student = Student(name=name)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('instructor_manage_students'))
    return render_template('manage_students.html', students=students)

@app.route('/instructors/manage/courses', methods=['GET', 'POST'])
def instructor_manage_courses():
    courses = Course.query.all()
    departments = Department.query.all() 
    instructors = Instructor.query.all() 

    if request.method == 'POST':
        name = request.form['name']
        department_id = request.form['department_id']
        instructor_id = request.form['instructor_id']

        new_course = Course(name=name, department_id=department_id, instructor_id=instructor_id)
        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for('instructor_manage_courses'))

    return render_template('manage_courses.html', courses=courses, departments=departments, instructors=instructors)

@app.route('/instructors/manage/enrollments', methods=['GET', 'POST'])
def instructor_manage_enrollments():
    enrollments = Enrollment.query.all()
    students = Student.query.all() 
    courses = Course.query.all()  

    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']

        new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.session.add(new_enrollment)
        db.session.commit()

        return redirect(url_for('instructor_manage_enrollments'))

    return render_template('manage_enrollments.html', enrollments=enrollments, students=students, courses=courses)

@app.route('/instructors/manage/exams', methods=['GET', 'POST'])
def manage_exams():
    exams = Exam.query.all()
    courses = Course.query.all()  

    if request.method == 'POST':
        course_id = request.form['course_id']
        date = request.form['date']

        new_exam = Exam(course_id=course_id, date=date)
        db.session.add(new_exam)
        db.session.commit()

        return redirect(url_for('manage_exams'))

    return render_template('manage_exams.html', exams=exams, courses=courses)


@app.route('/exam/add', methods=['POST'])
def add_exam():
    course_id = request.form['course_id']
    date_str = request.form['date']  
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()  
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD.", 400 
    new_exam = Exam(course_id=course_id, date=date)
    db.session.add(new_exam)
    db.session.commit()

    return redirect(url_for('manage_exams'))

@app.route('/departments')
def departments():
    departments = Department.query.all()
    return render_template('departments.html', departments=departments)

@app.route('/department/add', methods=['POST'])
def add_department():
    name = request.form['name']
    head_id = request.form.get('head_id', None) 
    new_department = Department(name=name, head_id=head_id)
    db.session.add(new_department)
    db.session.commit()
    return redirect(url_for('departments'))

@app.route('/department/delete/<int:id>', methods=['POST'])
def delete_department(id):
    Department.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('departments'))

@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/course/add', methods=['POST'])
def add_course():
    name = request.form['name']
    department_id = request.form['department_id']
    instructor_id = request.form['instructor_id']
    new_course = Course(name=name, department_id=department_id, instructor_id=instructor_id)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('admin_manage_courses'))

@app.route('/course/delete/<int:id>', methods=['POST'])
def delete_course(id):
    Course.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('admin_manage_courses'))

@app.route('/exams')
def exams():
    courses = Course.query.all()
    for course in courses:
        course.exams = Exam.query.filter_by(course_id=course.id).all()
    return render_template('exams.html', courses=courses)


@app.route('/exam/delete/<int:id>', methods=['POST'])
def delete_exam(id):
    Exam.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('manage_exams'))

@app.route('/students', methods=['GET', 'POST'])
def student_enrollment():
    if request.method == 'POST':
        student_id = request.form['student_id']
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        return render_template('student.html', enrollments=enrollments, student_id=student_id)
    return render_template('student.html', enrollments=None)

@app.route('/delete_student/<int:id>', methods=['POST', 'GET'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash('Student has been deleted successfully!', 'success')
    else:
        flash('Student not found!', 'danger')
    return redirect(url_for('admin_manage_students'))

@app.route('/admin/manage/hods/remove/<int:id>', methods=['POST'])
def remove_hod(id):
    hod = HOD.query.get_or_404(id)
    db.session.delete(hod)
    db.session.commit()
    return redirect(url_for('admin_manage_hods'))

@app.route('/admin/manage/students/add', methods=['POST'])
def add_student():
    name = request.form['name']
    new_student = Student(name=name)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('admin_manage_students'))

@app.route('/instructors/manage/students/add', methods=['POST'])
def instructor_add_student():
    name = request.form['name']
    new_student = Student(name=name)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('instructor_manage_students'))

@app.route('/admin/manage/hods/add', methods=['POST'])
def add_hod():
    department_id = request.form['department_id']
    instructor_id = request.form['instructor_id']
    new_hod = HOD(department_id=department_id, instructor_id=instructor_id)
    db.session.add(new_hod)
    db.session.commit()
    return redirect(url_for('admin_manage_hods'))

@app.route('/admin/manage/enrollments', methods=['GET', 'POST'])
def admin_manage_enrollments():
    enrollments = Enrollment.query.all()
    students = Student.query.all() 
    courses = Course.query.all() 
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        marks = request.form.get('marks') 
        if marks:
            try:
                marks = int(marks) 
            except ValueError:
                marks = None 
            
            new_enrollment = Enrollment(student_id=student_id, course_id=course_id, marks=marks)  
            db.session.add(new_enrollment)
            db.session.commit()
            return redirect(url_for('admin_manage_enrollments'))
    
    return render_template('manage_enrollments.html', enrollments=enrollments, students=students, courses=courses)

@app.route('/enrollment/add', methods=['POST'])
def add_enrollment():
    student_id = request.form.get('student_id')
    course_id = request.form.get('course_id')
    marks = request.form.get('marks')
    print(f"Student ID: {student_id}, Course ID: {course_id}, Marks: {marks}")
    if not student_id or not course_id or not marks:
        return "All fields are required.", 400  
    try:
        marks = int(marks)  
    except ValueError:
        return "Marks must be a number.", 400 
    new_enrollment = Enrollment(student_id=student_id, course_id=course_id, marks=marks)
    db.session.add(new_enrollment)
    db.session.commit()

    return redirect(url_for('admin_manage_enrollments')) 

@app.route('/admin/manage/instructors/add', methods=['POST'])
def add_instructor():
    name = request.form['name']
    new_instructor = Instructor(name=name)
    db.session.add(new_instructor)
    db.session.commit()
    return redirect(url_for('admin_manage_instructors'))

@app.route('/delete_instructor/<int:id>', methods=['POST', 'GET'])
def delete_instructor(id):
    instructor = Instructor.query.get(id)
    if instructor:
        db.session.delete(instructor)
        db.session.commit()
        flash('Instructor has been deleted successfully!', 'success')
    else:
        flash('Instructor not found!', 'danger')
    return redirect(url_for('admin_manage_instructors'))

@app.route('/instructors/manage/hods/add', methods=['POST'])
def instructor_add_hod():
    department_id = request.form['department_id']
    instructor_id = request.form['instructor_id']
    new_hod = HOD(department_id=department_id, instructor_id=instructor_id)
    db.session.add(new_hod)
    db.session.commit()
    return redirect(url_for('admin_manage_hods')) 

@app.route('/delete_enrollment/<int:id>', methods=['POST', 'GET'])
def delete_enrollment(id):
    enrollment = Enrollment.query.get(id)
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        flash('Enrollment has been deleted successfully!', 'success')
    else:
        flash('Enrollment not found!', 'danger')
    return redirect(url_for('admin_manage_enrollments'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
