from flask import make_response, render_template, session, flash, redirect, request, url_for
from app import app
from models import *
from database.db import *
from datetime import datetime, timedelta
from xhtml2pdf import pisa
from bson import ObjectId


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if session["user"] == 'admin':
            return render_template('admin/admin.html')
        else:
            employee = db.employee.find_one({"emp_id": session['emp_id']})
            print(session["in_disabled"])
            
            if session["in_disabled"]:
                latest_record = db.attendance.find_one(
                    {"emp_id": session['emp_id']}, sort=[("check_in", -1)])
                print(latest_record['_id'])
                check_outtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                check_outtime = datetime.strptime(
                    check_outtime, '%Y-%m-%d %H:%M:%S')
                print(check_outtime)
                check_intime = latest_record['check_in']
                print(check_intime)
                print(datetime.strptime(check_intime, '%Y-%m-%d %H:%M:%S'))
                check_intime = datetime.strptime(
                    check_intime, '%Y-%m-%d %H:%M:%S')
                round_time = check_outtime - check_intime
                print(round_time)
                notes = request.form['notes']
                dbResponse = db.attendance.update_one({'_id': latest_record['_id']},
                                                     {"$set": {"check_out": str(check_outtime), "raw_time": str(round_time), "rounded_time": str(round(round_time.total_seconds() / 3600, 2)), "notes": notes}})
            else:
                emp_timesheet = {"emp_id": session["emp_id"],
                                 "date": str(datetime.now().date()),
                                 "check_in": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                                 "check_out": "",
                                 "raw_time": "",
                                 "rounded_time": "",
                                 "paid": "no"}
                db.attendance.insert_one(emp_timesheet)
            return redirect(url_for('home'))
    else:
        if 'user' not in session:
            return redirect(url_for('login'))
        elif session["user"] == 'admin':
            # emp_count = db.employee.count_documents({})
            # designations_count = db.designations.count_documents({})
            # departments_count = db.departments.count_documents({})
            # clockedin_emp_count = db.timesheet.count_documents(
            #     {"check_out": ""})
            return render_template('admin/admin.html')
        elif session["user"] == 'supervisor':
            employee = db.employee.find_one({"emp_id": session['emp_id']})
            return render_template('supervisor/supervisor.html', employee=employee)
        else:
            employee = db.employee.find_one({"emp_id": session['emp_id']})
            check_out = db.attendance.find_one(
                {"check_out": "", "emp_id": session['emp_id']})
            if check_out is None:
                session["in_disabled"] = False
                session["out_disabled"] = True
            else:
                if not check_out['check_out']:
                    session["in_disabled"] = True
                    session["out_disabled"] = False
                else:
                    session["in_disabled"] = False
                    session["out_disabled"] = True
            return render_template('employee/employee.html', employee=employee)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        action = request.form['action']
        if action == 'login':
            if request.form["username"].strip():
                username = request.form["username"]
                password = request.form["password"]
                role = request.form.get("account")
                print(role)
                check = db.admin.find_one({"username": username})
                print(check)

                if role == "admin":
                    check = db.admin.find_one({"username": username})
                    print(check)
                    if check is None:
                        flash("Please check the role selected", 'error')
                        return redirect(request.url)
                    else:
                        session["user_id"] = str(check.get('_id'))
                        session["emp_id"] = username
                    if check.get('password') == password:
                        session["user"] = 'admin'
                        session["is_authenticated"] = True
                        return redirect(url_for('home'))
                    else:
                        flash("password mismatch")
                        return redirect(request.url)
                elif role == "employee":
                    check = db.employee.find_one({"emp_id": username})
                    print(check)
                    if check is None:
                        flash("Please check the role selected")
                        return redirect(request.url)
                    else:
                        session["user_id"] = str(check.get('_id'))
                        session['sup_id'] = check['supervisor_id']
                    if check.get('password') == password:
                        if check.get('is_verified') == False:
                            session["user"] = 'employee'
                            session["is_authenticated"] = True
                            session["emp_id"] = username
                            return redirect(url_for('home'))
                        else:
                            return redirect(url_for('resetpassword'))
                    else:
                        flash("password mismatch")
                        return redirect(request.url)
                elif role == "supervisor":
                    print(username)
                    check = db.employee.find_one({"emp_id": username})
                    print(check)
                    if check is None:
                        flash("Please check the role selected")
                        return redirect(request.url)
                    else:
                        session["user_id"] = str(check.get('_id'))
                    if check.get('password') == password:
                        if check.get('is_verified') == False:
                            session["user"] = 'supervisor'
                            session["is_authenticated"] = True
                            session["emp_id"] = username
                            return redirect(url_for('home'))
                        else:
                            return redirect(url_for('resetpassword'))
                    else:
                        flash("password mismatch")
                        return redirect(request.url)
                elif check is None:
                    flash("Please check the role selected")
                    return redirect(request.url)
                else:
                    session["user_id"] = str(check.get('_id'))
                    session["username"] = username
                    if check.get('password') == password:
                        auth = {"is_authenticated": True}
                        return render_template('index.html')
                    else:
                        flash("password mismatch")
                        return redirect(request.url)
            else:
                flash("fields are empty")
                return redirect(request.url)
        else:
            print("reset password########")
            return render_template('webpages/resetpassword.html')

    else:
        auth = {"is_authenticated": False}
        return render_template('includes/login.html')

    
@app.route('/logout', methods=["GET"])  # URL for logout
def logout():  # logout function
    session.pop('username', None)  # remove user session
    session.pop('user')
    session.clear()
    return redirect(url_for("login"))  # redirect to home page with message

@app.route('/editdepartment', methods=['GET', 'POST'])
def editdepartment():
    if request.method == 'POST':
        if request.form['request_type'] == 'request1':
            department = db.departments.find_one({"dept_name": request.form['dept_name']})
            return render_template('admin/editdepartment.html', department=department)
        elif request.form['request_type'] == 'request2':

            action = request.form['action']
            print(action)
            if action == 'update':
                # Handle update request
                updatedept()
                return redirect(url_for('home'))
            elif action == 'delete':
                print("###################")
                print(request.form['dept_name'])
                print("###################")
                db.departments.delete_one({"dept_name": request.form['dept_name']})
                return redirect(url_for('home'))
            # Handle delete request
            elif action == 'cancel':
                ################
                return redirect(url_for('home'))
            elif action == 'add':
                adddept()
                return redirect(url_for('home'))
    return render_template('admin/editdepartment.html', department={})

@app.route('/editroles', methods=['GET', 'POST'])
def editroles():
    if request.method == 'POST':
        if request.form['request_type'] == 'request1':
            role = db.roles.find_one({"role_name": request.form['role_name']})
            return render_template('admin/editroles.html', role=role)
        elif request.form['request_type'] == 'request2':

            action = request.form['action']
            print(action)
            if action == 'update':
                # Handle update request
                updaterole()
                return redirect(url_for('home'))
            elif action == 'delete':
                print("###################")
                print(request.form['role_name'])
                print("###################")
                db.roles.delete_one({"role_name": request.form['role_name']})
                return redirect(url_for('home'))
            # Handle delete request
            elif action == 'cancel':
                ################
                return redirect(url_for('home'))
            elif action == 'add':
                addrole()
                return redirect(url_for('home'))
    return render_template('admin/editroles.html', role={})


@app.route('/editemployee', methods=['GET', 'POST'])
def editemployee():
    if request.method == 'POST':
        if request.form['request_type'] == 'request1':
            employee = db.employee.find_one({"emp_id": request.form['emp_id']})
            departments = db.departments.find({})
            roles = db.roles.find({})
            return render_template('admin/editemployee.html', employee=employee,departments=departments, roles=roles)
        elif request.form['request_type'] == 'request2':

            action = request.form['action']
            print(action)
            if action == 'update':
                # Handle update request
                updateemp()
                return redirect(url_for('home'))
            elif action == 'delete':
                print("###################")
                print(request.form['emp_id'])
                print("###################")
                db.employee.delete_one({"emp_id": request.form['emp_id']})
                return redirect(url_for('home'))
            # Handle delete request
            elif action == 'cancel':
                ################
                return redirect(url_for('home'))
            elif action == 'add':
                addemp()
                return redirect(url_for('home'))
    else:
        departments = db.departments.find({})
        roles = db.roles.find({})
        return render_template('admin/editemployee.html', employee={},departments=departments, roles=roles)
    

@app.route("/checkinout", methods=['GET', 'POST'])
def checkinout():
    if request.method == "POST":
        employee = db.employee.find_one({"emp_id": session['emp_id']})
        print(session["in_disabled"])
        if session["in_disabled"]:
            latest_record = db.attendance.find_one(
                {"emp_id": session['emp_id']}, sort=[("check_in", -1)])
            print(latest_record['_id'])
            check_outtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            check_outtime = datetime.strptime(
                check_outtime, '%Y-%m-%d %H:%M:%S')
            print(check_outtime)
            check_intime = latest_record['check_in']
            print(check_intime)
            print(datetime.strptime(check_intime, '%Y-%m-%d %H:%M:%S'))
            check_intime = datetime.strptime(
                check_intime, '%Y-%m-%d %H:%M:%S')
            round_time = check_outtime - check_intime
            print(round_time)
            notes = request.form['notes']
            dbResponse = db.attendance.update_one({'_id': latest_record['_id']},
                                                 {"$set": {"check_out": str(check_outtime), "raw_time": str(round_time), "rounded_time": str(round(round_time.total_seconds() / 3600, 2)), "notes": notes}})
        else:
            emp_timesheet = {"emp_id": session["emp_id"],
                             "date": str(datetime.now().date()),
                             "check_in": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                             "check_out": "",
                             "raw_time": "",
                             "rounded_time": "",
                             "paid": "no"}
            db.attendance.insert_one(emp_timesheet)
            return redirect(url_for('home'))
    else:
        employee = db.employee.find_one({"emp_id": session['emp_id']})
        check_out = db.attendance.find_one(
            {"check_out": "", "emp_id": session['emp_id']})
        if check_out is None:
            session["in_disabled"] = False
            session["out_disabled"] = True
        else:
            if not check_out['check_out']:
                session["in_disabled"] = True
                session["out_disabled"] = False
            else:
                session["in_disabled"] = False
                session["out_disabled"] = True
        return render_template('employee/clock.html', employee=employee)

@app.route('/leaverequest', methods=['GET', 'POST'])
def leaverequest():
    if request.method == "POST":
        leaveData()
        return redirect(url_for('home'))
    else:
        
        return render_template('employee/leave.html')
    
@app.route('/empleaverequest', methods=['GET', 'POST'])
def empleaverequest():
    if request.method == "POST":
        return redirect(url_for('home'))
    else:
        leaves = db.leaverequests.find({"emp_id": session["emp_id"]})
        return render_template('employee/leaverequest.html', leaves=leaves)
    
@app.route('/addsupervisor', methods=['GET', 'POST'])
def addsupervisor():
    if request.method == "POST":
        updatesup()
        return redirect(url_for('home'))
    else:
        employees = db.employee.find({"role_name":"employee"})
        return render_template('supervisor/updatesupervisor.html', employees=employees)
    

@app.route('/supleaverequest', methods=['GET', 'POST'])
def supleaverequest():
    if request.method == "POST":
        return redirect(url_for('home'))
    else:
        leaves = db.leaverequests.find({"supervisor_id": session["emp_id"]})
        return render_template('supervisor/leaverequest.html', leaves=leaves)
    
@app.route('/leaveupdate+<emp_id>', methods=['GET', 'POST'])
def leaveupdate(emp_id):
    if request.method == "POST":
        return redirect(url_for('home'))
    else:
        print(emp_id)
        leave = list(db.leaverequests.find({"emp_id": emp_id, "status": "In Progress"}))
        return render_template('supervisor/leave.html', leave=leave[0])
    

@app.route('/updateleave', methods=['GET', 'POST'])
def updateleave():
    if request.method == "POST":
        updateleaveData()
        return redirect(url_for('home'))
    
@app.route('/paycheck', methods=['GET', 'POST'])
def paycheck():
    paycheck = db.payroll.find({"emp_id": session['emp_id']})
    employee = db.employee.find_one({"emp_id": session['emp_id']})
    calattendance()
    return render_template('employee/paycheck.html', paychecks=paycheck, employee=employee, salary=int(employee['salary'])/12, netpay=int(employee['salary'])/12-int(employee['tax']))

@app.route("/generatepdf/<paymentdate>", methods=["GET", "POST"])
def generatepdf(paymentdate):
    paymentdate = paymentdate
    print(paymentdate)
    employee = db.employee.find_one({"emp_id": session['emp_id']})
    paycheck = db.payroll.find_one(
        {"emp_id": session['emp_id'], "payment_date": paymentdate})
    print(paycheck)
    html = render_template("employee/paycheckpdf.html", paycheck=paycheck, todaydate=datetime.now().date(),
                           employee=employee, salary=int(employee['salary'])/12, netpay=int(employee['salary'])/12-int(employee['tax']))

    pdf = generate_pdf(html)

    # Create a response object and set the content type to application/pdf
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=row_data.pdf'

    return response

@app.route('/edittimes', methods=['GET', 'POST'])
def edittimes():
    if request.method == "POST":
        if request.form['request_type'] == 'request1':
            emp_id = request.form['emp_name']
            attendances = db.attendance.find({"emp_id": emp_id})
            employees = db.employee.find({"supervisor_id": session['emp_id']})
            return render_template('supervisor/clock.html',attendances=attendances,employees=employees)
    else:
        employees = db.employee.find({"supervisor_id": session['emp_id']})
        return render_template('supervisor/clock.html',attendances=[],employees=employees)
    
@app.route('/editclock+<id>', methods=['GET', 'POST'])
def editclock(id):
    if request.method == "POST":
        print("post")
    else:
        attendance = db.attendance.find_one({"_id": ObjectId(id)})
        return render_template('supervisor/editclock.html',attendance = attendance)
    
@app.route('/edittimecheck+<id>', methods=['GET', 'POST'])
def edittimecheck(id):
    if request.method == "POST":
        timeData(id)
        return redirect(url_for('home'))
    else:
        attendance = db.attendance.find_one({"_id": ObjectId(id)})
        return render_template('supervisor/editclock.html',attendance = attendance)