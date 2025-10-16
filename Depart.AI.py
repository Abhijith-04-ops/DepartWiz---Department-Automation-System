from flask import *
from DBConnection import Db
import datetime , os

app = Flask(__name__)
app.secret_key='123'


@app.route('/')
def login():
    return render_template('Login.html')

@app.route('/login_post' , methods=['POST'])
def login_post():
    usr = request.form['username']
    psd = request.form['password']
    db = Db()
    data = db.selectOne("select * from login WHERE username='" + usr + "' and passwrd='" + psd + "';")
    if data is not None:
        session['lid'] = data['id']
        if data['usertype'] == 'admin':
            return "<script>alert('Welcome Admin!');window.location='/admin_home'</script>"
        elif data['usertype'] == 'staff':
            return "<script>alert('Welcome Staff!');window.location='/staff_home'</script>"
        elif data['usertype'] == 'student':
            return "<script>alert('Welcome Student!');window.location='/stud_home'</script>"
        elif data['usertype'] == 'block':
            return "<script>alert('Access Denied! , Please Contact the Admin');window.location='/'</script>"
        else:
            return "<script>alert('User Not Found!');window.location='/'</script>"
    else:
        return "<script>alert('User Not Found!');window.location='/'</script>"

@app.route('/staff_register')
def staff_register():
    db=Db()
    data = db.select("select course_name,id from course;")
    return render_template('staff_register.html',data=data)

@app.route('/staff_register_post', methods=['POST'])
def staff_register_post():
    nme = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    gndr = request.form['gender']
    corse = request.form['course']
    dob = request.form['dob']
    psd = request.form['psd']
    db = Db()
    c = db.selectOne("select * from login where username='" + email + "';")
    if c is not None:
        return "<script>alert('Email Already Exists!!');window.location='/staff_register'</script>"
    else:
        x = db.insert(
            "insert into `login`(`id`,`username`,`passwrd`,`usertype`) VALUES ('','" + email + "','" + psd + "','block');")
        y = str(x)
        db.insert(
            "insert into `staff`(`id`,`staff_name`,`staff_email`,`staff_phone`,`staff_dob`,`staff_gender`,`login_id`,`course_id`) values ('','"+ nme +"', '" + email + "','"+ phone +"','" + dob + "','" + gndr  + "','" + y + "','"+ corse +"');")
        return "<script>alert('Staff Registration Successfull! Please Wait for Admin to Approve');window.location='/'</script>"

@app.route('/student_register')
def student_register():
    db = Db()
    data = db.select("select course_name,id from course;")
    return render_template('student_register.html', data=data)

@app.route('/student_register_post', methods=['POST'])
def student_register_post():
    nme = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    gndr = request.form['gender']
    corse = request.form['course']
    dob = request.form['dob']
    psd = request.form['psd']
    db = Db()
    c = db.selectOne("select * from login where username='" + email + "';")
    if c is not None:
        return "<script>alert('Email Already Exists!!');window.location='/student_register'</script>"
    else:
        x = db.insert(
        "insert into `login`(`id`,`username`,`passwrd`,`usertype`) VALUES ('','" + email + "','" + psd + "','block');")
        y = str(x)
        db.insert(
        "insert into `student`(`id`,`student_name`,`student_email`,`student_phone`,`student_dob`,`student_gender`,`login_id`,`course_id`) values ('','" + nme + "', '" + email + "','" + phone + "','" + dob + "','" + gndr + "','" + y + "','" + corse + "');")
        return "<script>alert('Student Registration Successfull! Please Wait for Admin to Approve');window.location='/'</script>"

@app.route('/logout')
def logout():
    session.clear()
    return "<script>alert('Logout Successfull!!');window.location='/'</script>"

#==================================================================ADMIN MODULE =====================================================================================================
@app.route('/admin_home')
def admin_home():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        return render_template('Admin/index.html')

@app.route('/add_department')
def add_department():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        session['heading'] = 'Add Department'
        return render_template('Admin/AddDepartment.html')

@app.route('/add_department_post' , methods=['POST'])
def add_department_post():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        dept = request.form['department']
        if dept:
            db = Db()
            data = db.select("select * from department WHERE department_name='"+dept+"';")
            print(data)
            if data:
                return "<script>alert('Department Already Exists. Try Again!!');window.location='/add_department#views'</script>"
            else:
                db.insert("insert into `department`(`id` , `department_name`) VALUES ('','"+ dept +"');")
                return "<script>alert('Department Added Successfully!!');window.location='/admin_home'</script>"
        else:
            return "<script>alert('Department Name Cannot be Empty. Try Again!!');window.location='/add_department#views'</script>"

@app.route('/view_department')
def view_department():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        session['heading'] = 'View Department'
        db = Db()
        data = db.select(
            "select * from department;")
        return render_template('Admin/ViewDepatment.htm', data=data)

@app.route('/update_department/<id>')
def update_department(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db = Db()
        session['heading']='Update Department'
        data = db.selectOne(
            "select * from department where id = '"+ id +"';")
        return render_template('Admin/UpdateDepartment.htm', data=data)

@app.route('/update_department_post/<id>', methods=['POST'])
def update_department_post(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        dept = request.form['department']
        db = Db()
        dat = db.selectOne("select * from department WHERE id='"+id+"';")
        if dept:
            if dept == str(dat.get('department_name')):
                return "<script>alert('No Changed Detected!! ');window.location='/view_department#views'</script>"
            else:
                db.update("update `department` set `department_name`='" + dept + "' where `id`='" + id + "';")
                return "<script>alert('Department Updated Successfully!!');window.location='/view_department#views'</script>"
        else:
            return "<script>alert('Department Name Cannot be Empty. Try Again!!');window.location='/view_department#views'</script>"

@app.route('/delete_department/<id>')
def delete_department(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        cor=db.select("select * from course WHERE dept_id='"+id+"'")
        if cor:
            return "<script>alert('Department Cannot Be Deleted as Courses are present!! Try Deleting the Courses First');window.location='/view_department#views'</script>"
        else:
            db.delete("delete from `department` where id=+'"+id+"';")
            return "<script>alert('Department Deleted Successfully!!');window.location='/view_department#views'</script>"


@app.route('/add_course/<id>')
def add_course(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        session['heading'] = 'Add Courses'
        return render_template('Admin/AddCourse.html',id=id)

@app.route('/add_course_post/<id>' , methods=['POST'])
def add_course_post(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        course = request.form['course']
        if course:
            db = Db()
            data = db.select("select * from course WHERE course_name='"+course+"';")
            if data:
                return "<script>alert('Course Already Exists. Try Again!!');window.location='/view_department#views'</script>"
            else:
                db.insert("insert into `course`(`id`,`course_name`,`dept_id`) VALUES('','"+course+"','"+id+"');")
                return "<script>alert('Course Added Successfully!!');window.location='/admin_home'</script>"
        else:
            return "<script>alert('Course Cannot be Empty. Try Again!!');window.location='/view_department#views'</script>"

@app.route('/view_course')
def view_course():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db = Db()
        session['heading']='View Courses'
        data = db.select(
            "select course.id , course.course_name , course.dept_id , department.department_name from `course` JOIN `department` ON course.dept_id=department.id;")
        print(data)
        return render_template('Admin/ViewCourse.htm', data=data)

@app.route('/update_course/<id>')
def update_course(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db = Db()
        session['heading']='Update Course'
        data = db.selectOne(
            "select * from course where id = '"+ id +"';")
        return render_template('Admin/UpdateCourse.htm', data=data)

@app.route('/update_course_post/<id>', methods=['POST'])
def update_course_post(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        course = request.form['course']
        db = Db()
        dat = db.selectOne("select * from course WHERE id='"+id+"';")
        if course:
            if course == str(dat.get('course_name')):
                return "<script>alert('No Changed Detected!! ');window.location='/view_course#views'</script>"
            else:
                db.update("update `course` set `course_name`='" + course + "' where `id`='" + id + "';")
                return "<script>alert('Course Updated Successfully!!');window.location='/view_course'</script>"
        else:
            return "<script>alert('Course Name Cannot be Empty. Try Again!!');window.location='/view_course#views'</script>"

@app.route('/delete_course/<id>')
def delete_course(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        sub=db.select("select * from `subject` WHERE course_id='"+id+"'")
        if sub:
            return "<script>alert('Course Cannot Be Deleted as Subjects are present!! Try Deleting the Subjects First');window.location='/view_course#views'</script>"
        else:
            db.delete("delete from `course` where id=+'"+id+"';")
            return "<script>alert('Course Deleted Successfully!!');window.location='/view_course#views'</script>"

@app.route('/add_subject/<cid>/<did>')
def add_subject(cid , did):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        session['heading']='Add Subject'
        return render_template('Admin/AddSubject.html',cid=cid , did= did)

@app.route('/add_subject_post/<cid>/<did>' , methods=['POST'])
def add_subject_post(cid,did):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        print(cid,'cccccccccccccccc')
        print(did,'ddddddddddddddddddddddddd')
        sub = request.form['subject']
        if sub:
            db = Db()
            data = db.select("select * from subject WHERE subject_name='"+sub+"' and course_id='"+cid+"';")
            if data:
                return "<script>alert('Subject Already Exists. Try Again!!');window.location='/view_course#views'</script>"
            else:
                db.insert("insert into `subject`(`id`,`subject_name`,`course_id`,`dept_id`) VALUES('','"+sub+"','"+cid+"','"+did+"');")
                return "<script>alert('Subject Added Successfully!!');window.location='/admin_home'</script>"
        else:
            return "<script>alert('Subject Cannot be Empty. Try Again!!');window.location='/view_course#views'</script>"

@app.route('/view_subject')
def view_subject():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        session['heading'] = 'View Subjects'
        db = Db()
        data = db.select(
            "select subject.id , subject.subject_name, department.department_name,course.course_name  from `subject` JOIN `department` ON subject.dept_id=department.id JOIN course on course.id=subject.course_id;")
        return render_template('Admin/ViewSubject.htm', data=data)

@app.route('/update_subject/<id>')
def update_subject(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        session['heading']='Update Subject'
        db = Db()
        data = db.selectOne("select subject_name,id from subject where id = '"+ id +"';")
        return render_template('Admin/UpdateSubject.htm', data=data)

@app.route('/update_subject_post/<id>', methods=['POST'])
def update_subject_post(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        sub = request.form['subject']
        db = Db()
        dat = db.selectOne("select * from subject WHERE id='"+id+"';")
        if sub:
            if sub == str(dat.get('subject_name')):
                return "<script>alert('No Changed Detected!! ');window.location='/view_subject#views'</script>"
            else:
                db.update("update `subject` set `subject_name`='" + sub + "' where `id`='" + id + "';")
                return "<script>alert('Subject Updated Successfully!!');window.location='/view_subject#views'</script>"
        else:
            return "<script>alert('Subject Cannot be Empty. Try Again!!');window.location='/view_subject#views'</script>"

@app.route('/delete_subject/<id>')
def delete_subject(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        db.delete("delete from `subject` where id=+'"+id+"';")
        return "<script>alert('Subject Deleted Successfully!!');window.location='/view_subject#views'</script>"

@app.route('/view_staff')
def view_staff():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db = Db()
        session['heading']='View Staffs'
        data = db.select(
            "select *  from `staff` JOIN login ON staff.login_id=login.id;")
        return render_template('Admin/ViewStaff.htm', data=data)

@app.route('/block_staff/<id>')
def block_staff(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        db.update("update login set usertype='block' where id ='"+id+"' ;")
        return "<script>alert('Staff Blocked Successfully!!');window.location='/view_staff#views'</script>"

@app.route('/unblock_staff/<id>')
def unblock_staff(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        db.update("update login set usertype='staff' where id ='"+id+"' ;")
        return "<script>alert('Staff Unblocked Successfully!!');window.location='/view_staff#views'</script>"

@app.route('/view_student')
def view_student():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db = Db()
        session['heading']='View Students'
        data = db.select(
            "select *  from `student` JOIN login ON student.login_id=login.id;")
        return render_template('Admin/ViewStudent.htm', data=data)

@app.route('/block_stud/<id>')
def block_stud(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        db.update("update login set usertype='block' where id ='"+id+"' ;")
        return "<script>alert('Student Blocked Successfully!!');window.location='/view_student#views'</script>"

@app.route('/unblock_stud/<id>')
def unblock_stud(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        db.update("update login set usertype='student' where id ='"+id+"' ;")
        return "<script>alert('Student Unblocked Successfully!!');window.location='/view_student#views'</script>"

@app.route('/view_feedback')
def view_feedback():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db = Db()
        session['heading'] = 'View Feedbacks'
        data = db.select(
            "select feedback.id , feedback.feed_date , feedback.feedback , login.username from feedback JOIN login ON feedback.login_id=login.id;")
        return render_template('Admin/ViewFeedback.htm', data=data)

@app.route('/view_complaint')
def view_complaint():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db = Db()
        session['heading']='View Complaints'
        data = db.select(
            "select complaint.id , complaint.comp_date ,complaint.complaint ,complaint.reply , complaint.reply_date, login.username from complaint JOIN login ON complaint.login_id=login.id;")
        return render_template('Admin/ViewComplaint.htm', data=data)

@app.route('/send_reply/<id>')
def send_reply(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        session['heading']='Send Reply'
        return render_template('Admin/SendReply.htm',id=id)

@app.route('/send_reply_post/<id>', methods=['POST'])
def send_reply_post(id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        reply = request.form['reply']
        d=datetime.datetime.now().strftime("%d-%m-%Y")
        if reply:
            db=Db()
            db.update("update complaint set reply_date='"+d+"', reply='"+reply+"' where `id`='"+id+"' ;")
            return "<script>alert('Reply Send Successfully!!');window.location='/view_complaint#views'</script>"
        else:
            return "<script>alert('Reply Cannot be Empty. Try Again!!');window.location='/view_complaint#views'</script>"

@app.route('/allocate_subject/<lid>')
def allocate_subject(lid):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        session['heading']='Subject Allocation'
        db=Db()
        c = db.selectOne("select id,course_id from staff WHERE login_id='"+lid+"'")
        sid = str(c.get('id'))
        cid = str(c.get('course_id'))
        data = db.select("select subject.id , subject.subject_name, course.course_name from subject JOIN course ON subject.course_id=course.id WHERE subject.course_id='"+cid+"';")
        return render_template('Admin/ShowSubject.htm',data = data , id=sid)

@app.route('/assign_subject_post/<sid>/<sub_id>/')
def assign_subject_post(sid,sub_id):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        dat = db.select("select * from subject_allocation WHERE subject_id='"+sub_id+"' and staff_id='"+sid+"';")
        if dat:
            return "<script>alert('Subject Already Allocated to the Staff!!');window.location='/view_staff#views'</script>"
        else:
            db.insert("insert into subject_allocation(id,subject_id,staff_id) VALUES ('','"+sub_id+"','"+sid+"');")
            return "<script>alert('Subject Assigned Successfully!!');window.location='/view_staff#views'</script>"

@app.route('/view_allocated_user')
def view_allocated_user():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db = Db()
        session['heading']='View Allocated Staffs'
        data = db.select("select subject_allocation.id , staff.staff_name,subject.subject_name from subject_allocation JOIN staff ON subject_allocation.staff_id=staff.id JOIN subject ON subject_allocation.subject_id=subject.id;")
        return render_template('Admin/ViewAllocatedStaff.htm', data=data)


@app.route('/delete_staff/<lid>')
def delete_staff(lid):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        s = db.selectOne("select * from staff WHERE login_id='"+lid+"';")
        sid = str(s.get('id'))
        db.delete("delete from `subject_allocation` WHERE staff_id='"+sid+"';")
        db.delete("delete from `staff` WHERE id='"+sid+"';")
        db.update("update login set `usertype` = 'deleted' WHERE id='"+lid+"'")
        return "<script>alert('Staff Deleted Successfully!!');window.location='/view_staff'</script>"

@app.route('/delete_allocation/<aid>')
def delete_allocation(aid):
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        db=Db()
        mat = db.select("select * from material WHERE alloc_id='"+aid+"';")
        if mat:
            db.delete("delete from material WHERE alloc_id='" + aid + "';")
            db.delete("delete from subject_allocation WHERE id='" + aid + "';")
            return "<script>confirm('UnAllocating Will Erase The Materials Uploaded By the Staff!!');window.location='/view_allocated_user#views'</script>"
        else:
            db.delete("delete from subject_allocation WHERE id='"+aid+"';")
            return "<script>alert('Allocation Deleted Successfully!!');window.location='/view_allocated_user#views'</script>"

@app.route('/change_password_admin')
def change_password_admin():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        session['heading']='Change Password '
        return render_template('Admin/ChangePasswordAdmin.htm')

@app.route('/change_password_admin_post',methods=['POST'])
def change_password_admin_post():
    if 'lid' not in session:
        return "<script>alert('Please Login!!');window.location='/'</script>"
    else:
        current_password = request.form['cpasswd']
        new_password = request.form['npasswd']
        re_enter_password = request.form['cfpasswd']
        db = Db()
        pwd = db.selectOne("select `passwrd` from login where `id`='" + str(
            session['lid']) + "' and passwrd='" + current_password + "';")
        if pwd is not None:
            if new_password == re_enter_password:
                db = Db()
                db.update("update `login` set `passwrd`='" + new_password + "' WHERE id='"+str(session['lid'])+"';")
                return "<script>alert('Password Changed Successfully!!');window.location='/admin_home'</script>"
            else:
                return "<script>alert('Please Check New Password and Re-enter Password!!');window.location='/change_password'</script>"
        else:
            return "<script>alert('Please check current password!!');window.location='/change_password'</script>"




#================================================ STAFF MODULE ======================================================================================

@app.route('/staff_home')
def staff_home():
    return render_template('Teacher/StaffHome.htm')

@app.route('/staff_profile')
def staff_profile():
    lid=str(session['lid'])
    db=Db()
    data = db.selectOne("select * from staff where login_id='"+lid+"';")
    return render_template('Teacher/ViewStaffProfile.htm', data=data)

@app.route('/update_staff_profile')
def update_staff_profile():
    lid = str(session['lid'])
    db = Db()
    data = db.selectOne("select * from staff WHERE login_id='" + lid + "';")
    return render_template('Teacher/UpdateStaffProfile.htm', data=data)

@app.route('/update_staff_profile_post' , methods=['POST'])
def update_staff_profile_post():
    lid = str(session['lid'])
    nme = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    dob = request.form['dob']
    db = Db()
    db.update("update staff set staff_name='"+nme+"',staff_email='"+email+"',staff_phone='"+phone+"',staff_dob='"+dob+"' WHERE login_id='"+lid+"';")
    return "<script>alert('Profile Updated Successfully!!');window.location='/staff_profile'</script>"

@app.route('/view_my_subject')
def view_my_subject():
    db = Db()
    lid = str(session['lid'])
    sdata = db.selectOne("select * from staff WHERE login_id='"+lid+"';")
    sid = str(sdata.get('id'))
    data = db.select("select subject_allocation.id, subject.subject_name from subject_allocation JOIN subject ON subject_allocation.subject_id = subject.id WHERE subject_allocation.staff_id='"+sid+"';")
    return render_template('Teacher/ViewMySubject.htm',data=data)

@app.route('/add_material/<id>')
def add_material(id):
    return render_template('Teacher/AddMaterial.htm',id=id)

@app.route('/add_material_post/<id>', methods=['POST'])
def add_material_post(id):
    material=request.files['material']
    d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    date = datetime.datetime.now().strftime("%d%m%Y")
    material.save(r"C:\Users\Abhi\PycharmProjects\Depart.AI\static\material\\" + d + '.pdf')
    path = "static/material/" + d + '.pdf'
    db=Db()
    db.insert("insert into material(`id`,`material`,`upload_date`,`alloc_id`)VALUES ('','"+path+"','"+date+"','"+id+"');")
    return "<script>alert('Material Uploaded Successfully!!');window.location='/view_my_subject'</script>"

@app.route('/view_material/<id>')
def view_material(id):
    db = Db()
    data = db.select("select material.id, material.material, material.upload_date from material WHERE alloc_id='"+id+"';")
    return render_template('Teacher/ViewMaterial.htm', data = data)

@app.route('/open_file/<id>')
def open_file(id):
    db=Db()
    path = db.selectOne("select material from material WHERE id='"+id+"';")
    relative_path = path.get('material')
    directory =os.path.dirname(relative_path)
    filename = os.path.basename(relative_path)
    return send_from_directory(directory, filename, mimetype='application/pdf')

@app.route('/delete_file/<id>')
def delete_file(id):
    db=Db()
    db.delete("delete from material where id='"+id+"';")
    return "<script>alert('Material Deleted Successfully!!');window.location='/view_my_subject'</script>"

@app.route('/view_my_student')
def view_my_student():
    db =Db()
    lid = str(session['lid'])
    data = db.selectOne("select * from staff WHERE login_id='"+lid+"';")
    cid = str(data.get('course_id'))
    data1 = db.select("select * from student WHERE course_id='"+cid+"';")
    return render_template('Teacher/ViewStaffStud.htm',data = data1)

@app.route('/send_complaint')
def send_complaint():
    return render_template('Teacher/Send_complaint.htm')

@app.route('/send_complaint_post', methods=['post'])
def send_complaint_post():
    lid = session['lid']
    comp = request.form['complaint']
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    db = Db()
    db.insert("insert into complaint(`id`,`comp_date`,`complaint`,`reply_date`,`reply`,`login_id`) VALUES ('','"+date+"','"+comp+"','pending','pending','"+str(lid)+"');")
    return "<script>alert('Complaint Send Successfully!!');window.location='/staff_home'</script>"

@app.route('/view_complaint_reply')
def view_complaint_reply():
    lid = str(session['lid'])
    db = Db()
    data = db.select("select * from complaint WHERE login_id='"+lid+"';")
    return render_template('Teacher/ViewReply.htm' , data=data)

@app.route('/send_feedback')
def send_feedback():
    return render_template('Teacher/Send_feedback.htm')

@app.route('/send_feedback_post', methods=['post'])
def send_feedback_post():
    lid = session['lid']
    feed = request.form['feedback']
    date = datetime.datetime.now().strftime("%d%m%Y")
    db = Db()
    db.insert("insert into feedback(`id`,`feed_date`,`feedback`,`login_id`) VALUES ('','"+date+"','"+feed+"','"+str(lid)+"');")
    return "<script>alert('Feedback Send Successfully!!');window.location='/staff_home'</script>"

#=======================================================STUDENT MODULE =========================================================================
@app.route('/stud_home')
def stud_home():
    return render_template('Student/StudentHome.htm')

@app.route('/stud_profile')
def stud_profile():
    lid=str(session['lid'])
    db=Db()
    data = db.selectOne("select * from student where login_id='"+lid+"';")
    return render_template('Student/ViewStudProfile.htm', data=data)

@app.route('/update_stud_profile')
def update_stud_profile():
    lid = str(session['lid'])
    db = Db()
    data = db.selectOne("select * from student WHERE login_id='" + lid + "';")
    return render_template('Student/UpdateStudProfile.htm', data=data)

@app.route('/update_stud_profile_post' , methods=['POST'])
def update_stud_profile_post():
    lid = str(session['lid'])
    nme = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    dob = request.form['dob']
    db = Db()
    db.update("update student set student_name='"+nme+"',student_email='"+email+"',student_phone='"+phone+"',student_dob='"+dob+"' WHERE login_id='"+lid+"';")
    return "<script>alert('Profile Updated Successfully!!');window.location='/stud_profile'</script>"

@app.route('/view_stud_subject')
def view_stud_subject():
    db = Db()
    lid = str(session['lid'])
    sdata = db.selectOne("select * from student WHERE login_id='"+lid+"';")
    cid = str(sdata.get('course_id'))
    data = db.select("select subject.id , subject.subject_name from subject JOIN course ON subject.course_id = course.id WHERE subject.course_id='"+cid+"';")
    return render_template('Student/ViewStudSubject.htm',data=data)

@app.route('/view_stud_material/<id>')
def view_stud_material(id):
    db = Db()
    adata = db.selectOne("select id from subject_allocation WHERE subject_id='"+id+"'")
    if adata:
        aid = str(adata.get('id'))
        data = db.select("select material.id, material.material, material.upload_date from material WHERE alloc_id='"+aid+"';")
        return render_template('Student/ViewStudMaterial.htm', data = data)
    else:
        return "<script>alert('Materials Not Uploaded For the Subject');window.location='/view_stud_subject'</script>"

@app.route('/view_stud_classmates')
def view_stud_classmates():
   db =Db()
   lid = str(session['lid'])
   cdat = db.selectOne("select course_id from student WHERE login_id='"+lid+"';")
   cid = str(cdat.get('course_id'))
   data = db.select("select * from student WHERE course_id='"+cid+"';")
   return render_template('Student/ViewStudClassmates.htm',data=data)

@app.route('/send_stud_complaint')
def send_stud_complaint():
    return render_template('Student/Send_stud_complaint.htm')

@app.route('/send_stud_complaint_post', methods=['post'])
def send_stud_complaint_post():
    lid = session['lid']
    comp = request.form['complaint']
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    db = Db()
    db.insert("insert into complaint(`id`,`comp_date`,`complaint`,`reply_date`,`reply`,`login_id`) VALUES ('','"+date+"','"+comp+"','pending','pending','"+str(lid)+"');")
    return "<script>alert('Complaint Send Successfully!!');window.location='/stud_home'</script>"

@app.route('/view_stud_complaint_reply')
def view_stud_complaint_reply():
    lid = str(session['lid'])
    db = Db()
    data = db.select("select * from complaint WHERE login_id='"+lid+"';")
    return render_template('Student/ViewStudReply.htm' , data=data)

@app.route('/send_stud_feedback')
def send_stud_feedback():
    return render_template('Student/Send_stud_feedback.htm')

@app.route('/send_stud_feedback_post', methods=['post'])
def send_stud_feedback_post():
    lid = session['lid']
    feed = request.form['feedback']
    date = datetime.datetime.now().strftime("%Y%m%d")
    db = Db()
    db.insert("insert into feedback(`id`,`feed_date`,`feedback`,`login_id`) VALUES ('','"+date+"','"+feed+"','"+str(lid)+"');")
    return "<script>alert('Feedback Send Successfully!!');window.location='/stud_home'</script>"











if __name__ == '__main__':
    app.run()
