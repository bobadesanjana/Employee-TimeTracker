from flask import render_template, session, flash, redirect, request
from app import app
from models import *
from database.db import *
from datetime import datetime, timedelta
from xhtml2pdf import pisa
import io
from bson import ObjectId


def adddept():
    dept_name = request.form['dept_name']
    dept_desc = request.form['dept_desc']

    department = {"dept_name": dept_name,
                "dept_desc": dept_desc,
                }
    print(department)
    check = db.departments.find_one({"dept_name": dept_name})
    if check is None:
        db.departments.insert_one(department)

def updatedept():
    dept_name = request.form['dept_name']
    dept_desc = request.form['dept_desc']
    dbResponse = db.departments.update_one({"dept_name": dept_name},
                                        {"$set": {"dept_name": dept_name, "dept_desc": dept_desc
                                                  }})
    
def addrole():
    role_name = request.form['role_name']
    role_permission = request.form['role_permission']

    role = {"role_name": role_name,
                "role_permission": role_permission,
                }
    print(role)
    check = db.roles.find_one({"role_name": role_name})
    if check is None:
        db.roles.insert_one(role)

def updaterole():
    role_name = request.form['role_name']
    role_permission = request.form['role_permission']
    dbResponse = db.roles.update_one({"role_name": role_name},
                                        {"$set": {"dept_name": role_name, "role_permission": role_permission
                                                  }})
    

def addemp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    phone_number = request.form['phone_number']
    gender_name = request.form['gender_name']
    job_type = request.form['job_type']
    role_name = request.form['role_name']
    dept_name = request.form['dept_name']
    street_address = request.form['street_address']
    street_address1 = request.form['street_address1']
    city_name = request.form['city_name']
    region_name = request.form['region_name']
    zip_code = request.form['zip_code']
    country_name = request.form['country_name']
    paycheck_type = request.form['paycheck_type']
    dob = request.form['dob']
    doj = request.form['doj']
    salary = request.form['salary']
    hourly_rate = request.form['hourly_rate']
    tax = request.form['tax']
    ssn_number = request.form['ssn_number']
    notes = request.form['notes']
    leave_balance = request.form['leave']

    employee = {"emp_id": emp_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "phone_number": phone_number,
                "gender": gender_name,
                "job_type": job_type,
                "role_name": role_name,
                "dept_name": dept_name,
                "street_address": street_address,
                "street_address1": street_address1,
                "city_name": city_name,
                "region_name": region_name,
                "zip_code": zip_code,
                "country_name": country_name,
                "paycheck_type": paycheck_type,
                "dob": dob,
                "doj": doj,
                "salary": salary,
                "hourly_rate": hourly_rate,
                "tax": tax,
                "leave_balance" : leave_balance,
                "ssn_number": ssn_number,
                "supervisor_id":"",
                "notes": notes,
                "is_verified":False}
    print(employee)
    check = db.employee.find_one({"emp_id": emp_id})
    if check is None:
        db.employee.insert_one(employee)


def updateemp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    phone_number = request.form['phone_number']
    gender_name = request.form['gender_name']
    job_type = request.form['job_type']
    role_name = request.form['role_name']
    dept_name = request.form['dept_name']
    street_address = request.form['street_address']
    street_address1 = request.form['street_address1']
    city_name = request.form['city_name']
    region_name = request.form['region_name']
    zip_code = request.form['zip_code']
    country_name = request.form['country_name']
    paycheck_type = request.form['paycheck_type']
    dob = request.form['dob']
    doj = request.form['doj']
    salary = request.form['salary']
    hourly_rate = request.form['hourly_rate']
    tax = request.form['tax']
    ssn_number = request.form['ssn_number']
    notes = request.form['notes']
    leave_balance = request.form['leave']

    print(role_name)
    dbResponse = db.employee.update_one({"emp_id": emp_id},
                                        {"$set": {"first_name": first_name, "last_name": last_name, "email": email, "password": password, "phone_number": phone_number, "gender_name": gender_name, "job_type":job_type, "role_name":role_name, "dept_name":dept_name,"street_address": street_address, "street_address1": street_address1,
                                                  "city_name": city_name, "region_name": region_name, "zip_code": zip_code, "country_name": country_name, "salary":salary,"paycheck_type": paycheck_type, "dob": dob,
                                                  "doj":doj,"hourly_rate":hourly_rate,"tax":tax,"leave_balance" : leave_balance,"ssn_number":ssn_number,"notes":notes}})
    
def leaveData():
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    leave_reason = request.form['leave_reason']
    sup_id = request.form['sup_id']

    leave = {"emp_id": session["emp_id"], "supervisor_id":sup_id,"start_date": start_date, "end_date": end_date,"reason": leave_reason,"status": "In Progress", "comment":""}

    check = db.leaverequests.find_one({"emp_id": session["emp_id"] , "status": "In Progress"})
    if check is None:
        db.leaverequests.insert_one(leave)

def updatesup():
    emp_id = request.form['emp_name']
    sup_id = request.form['sup_id']

    print(sup_id)
    dbResponse = db.employee.update_one({"emp_id": emp_id},
                                        {"$set": {"supervisor_id": sup_id}})
    
def updateleaveData():
    start_date_str = request.form['start_date']
    end_date_str = request.form['end_date']
    leave_reason = request.form['leave_reason']
    leave_comment = request.form['leave_comment']
    emp_id = request.form['emp_id']
    status = request.form['status']

    # Convert strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Calculate the difference in days
    delta = end_date - start_date
    days_difference = delta.days

    dbResponse = db.leaverequests.update_one({"emp_id": emp_id, "status":"In Progress"},
                                        {"$set": {"start_date":start_date_str, "end_date": end_date_str,"comment":leave_comment,"status":status }})

    # Fetch the current leave balance for the employee
    employee = db.employee.find_one({"emp_id": emp_id})
    if employee:
        current_leave_balance = employee.get('leave_balance')
        new_leave_balance = int(current_leave_balance) - days_difference

        if status == "Approved":
            # Update the leave balance in the database
            db.employee.update_one({"emp_id": emp_id}, {"$set": {"leave_balance": new_leave_balance}})


def calattendance():
    employee = db.employee.find_one({"emp_id": session['emp_id']})
    if employee['paycheck_type'] == "Bi-Weekly":
        paycheck = db.payroll.find_one({"emp_id": session['emp_id'], "paid": 'no', "paycheck_month": str(datetime.now().month)})
        print(paycheck)
        print("#############################")
        
        if datetime.now().day == 1 or datetime.now().day == 16:
            print('update old paycheck')
            roundedtime = 0
            timesheets = db.attendance.find({"emp_id": session['emp_id'], "paid": 'no', "check_out": {"$exists": True, "$ne": ""}})
            if not list(timesheets):
                print('nothing to update')
                if paycheck is None:
                    print('create')
                    employee = db.employee.find_one({"emp_id": session['emp_id']})
                    emp_id = session['emp_id']
                    payment_date= str(datetime.now().date())
                    basic_salary=employee['salary']
                    tax_deduction=employee['tax']
                    hourly_rate=employee['hourly_rate']
                    paid="no"
                    print(str(datetime.now().month))
                    paycheck_month=str(datetime.now().month)

                    new_paycheck={"emp_id":emp_id,"payment_date":payment_date,"basic_salary":basic_salary,
                                  "tax_deduction":tax_deduction,"net_pay":"","hourly_rate":hourly_rate,"hours_worked": "","paid":paid,"paycheck_month":paycheck_month}
                    db.payroll.insert_one(new_paycheck)
                else:
                    if paycheck['payment_date'] == str(datetime.now().date()):
                        print('created today')
                    else:
                        db.payroll.update_one({'_id': paycheck['_id']}, {
                                       '$set': {"paid":'yes'}})
                        
            else:
                    
                    timesheets = db.attendance.find({"emp_id": session['emp_id'], "paid": 'no', "check_out": {"$exists": True, "$ne": ""}})
                    for timesheet in timesheets:
                        if timesheet['rounded_time'] != '':
                            roundedtime += float(timesheet['rounded_time'])
                            print(timesheet)
                            db.attendance.update_one({'_id': timesheet['_id']}, {
                                                '$set': {'paid': 'yes'}})
                            print(timesheet)
                    print(roundedtime*10)
                    if paycheck['hours_worked'] =="" or paycheck['hours_worked'] ==0:
                        hours_worked = roundedtime
                    else:
                        hours_worked = float(paycheck['hours_worked'])+roundedtime
                    employee = db.employee.find_one({"emp_id": session['emp_id']})
                    
                    net_pay = round(hours_worked* float(employee['hourly_rate']),2)
                    tax_deduction= round(net_pay/10,2)
                    db.payroll.update_one({'_id': paycheck['_id']}, {
                                       '$set': {'hours_worked': str(hours_worked),"net_pay":net_pay,"tax_deduction":tax_deduction,"paid":'no'}})
                    
        else:
            print('update paycheck for every new timesheet')
            if paycheck is None:
                    print('create')
                    employee = db.employee.find_one({"emp_id": session['emp_id']})
                    emp_id = session['emp_id']
                    payment_date= str(datetime.now().date())
                    basic_salary=employee['salary']
                    tax_deduction=employee['tax']
                    hourly_rate=employee['hourly_rate']
                    paid="no"
                    print(str(datetime.now().month))
                    paycheck_month=str(datetime.now().month)

                    new_paycheck={"emp_id":emp_id,"payment_date":payment_date,"basic_salary":basic_salary,
                                  "tax_deduction":tax_deduction,"net_pay":"","hourly_rate":hourly_rate,"hours_worked": "","paid":paid,"paycheck_month":paycheck_month}
                    db.payroll.insert_one(new_paycheck)
            roundedtime = 0
            timesheets = db.attendance.find(
                {"emp_id": session['emp_id'], "paid": 'no', "check_out": {"$exists": True, "$ne": ""}})
            print(timesheets)
            paycheck = db.payroll.find_one({"emp_id": session['emp_id'], "paid": 'no', "paycheck_month": str(datetime.now().month)})
            print(paycheck)
            if not list(timesheets):
                print('nothing to update')
            else:
                timesheets = db.attendance.find({"emp_id": session['emp_id'], "paid": 'no', "check_out": {"$exists": True, "$ne": ""}})
                for timesheet in timesheets:
                    if timesheet['rounded_time'] != '':
                        roundedtime += float(timesheet['rounded_time'])
                        print(timesheet)
                        db.attendance.update_one({'_id': timesheet['_id']}, {
                                                '$set': {'paid': 'yes'}})
                print(roundedtime*10)
                print('##################################################')
                print(paycheck['_id'])
                print('##################################################')
                if paycheck['hours_worked'] =='0':
                    hours_worked = roundedtime
                    print(hours_worked)
                    print("##")
                else:
                    print(float(paycheck['hours_worked']))
                    print(roundedtime)
                    hours_worked = float(paycheck['hours_worked'])+roundedtime
                    print(hours_worked)
                net_pay = round(hours_worked* float(employee['hourly_rate']),2)
                tax_deduction= round(net_pay/10,2)
                db.payroll.update_one({'_id': paycheck['_id']}, {
                                       '$set': {'hours_worked': str(hours_worked),"net_pay":net_pay,"tax_deduction":tax_deduction,"paid":'no'}})
    else:
        print('monthly')
        paycheck = db.payroll.find_one({"emp_id": session['emp_id'], "paid": 'no', "paycheck_month": str(datetime.now().month)})
         
        if datetime.now().day == 1:
            print("1")
            print('update old paycheck')
            roundedtime = 0
            timesheets = db.attendance.find({"emp_id": session['emp_id'], "paid": 'no', "check_out": {"$exists": True, "$ne": ""}})
            if not list(timesheets):
                print('nothing to update')
                if paycheck is None:
                    print('create')
                    employee = db.employee.find_one({"emp_id": session['emp_id']})
                    emp_id = session['emp_id']
                    payment_date= str(datetime.now().date())
                    basic_salary=employee['salary']
                    tax_deduction=employee['tax']
                    hourly_rate=employee['hourly_rate']
                    paid="no"
                    print(str(datetime.now().month))
                    paycheck_month=str(datetime.now().month)

                    new_paycheck={"emp_id":emp_id,"payment_date":payment_date,"basic_salary":basic_salary,
                                  "tax_deduction":tax_deduction,"net_pay":"","hourly_rate":hourly_rate,"hours_worked": "","paid":paid,"paycheck_month":paycheck_month}
                    db.payroll.insert_one(new_paycheck)
                else:
                    if paycheck['payment_date'] == str(datetime.now().date()):
                        print('created today')
                    else:
                        print(paycheck['_id'])
                        db.payroll.update_one({'_id': paycheck['_id']}, {
                                       '$set': {"paid":'yes'}})
                        
            else:
                    timesheets = db.attendance.find({"emp_id": session['emp_id'], "paid": 'no', "check_out": {"$exists": True, "$ne": ""}})
                    for timesheet in timesheets:
                        if timesheet['rounded_time'] != '':
                            roundedtime += float(timesheet['rounded_time'])
                            print(timesheet)
                            db.attendance.update_one({'_id': timesheet['_id']}, {
                                                '$set': {'paid': 'yes'}})
                            print(timesheet)
                    print(roundedtime*10)
                    if paycheck['hours_worked'] =="":
                        hours_worked = roundedtime
                    else:
                        hours_worked = round(float(paycheck['hours_worked'])+roundedtime)
                    employee = db.employee.find_one({"emp_id": session['emp_id']})
                    
                    net_pay = round(hours_worked* float(employee['hourly_rate']),2)
                    tax_deduction= round(net_pay/10,2)
                    db.payroll.update_one({'_id': paycheck['_id']}, {
                                       '$set': {'hours_worked': str(hours_worked),"net_pay":net_pay,"tax_deduction":tax_deduction,"paid":'no'}})
                    
        else:
            if paycheck is None:
                    print('create')
                    employee = db.employee.find_one({"emp_id": session['emp_id']})
                    emp_id = session['emp_id']
                    payment_date= str(datetime.now().date())
                    basic_salary=employee['salary']
                    tax_deduction=employee['tax']
                    hourly_rate=employee['hourly_rate']
                    paid="no"
                    print(str(datetime.now().month))
                    paycheck_month=str(datetime.now().month)

                    new_paycheck={"emp_id":emp_id,"payment_date":payment_date,"basic_salary":basic_salary,
                                  "tax_deduction":tax_deduction,"net_pay":"","hourly_rate":hourly_rate,"hours_worked": "","paid":paid,"paycheck_month":paycheck_month}
                    db.payroll.insert_one(new_paycheck)
            print('update paycheck for every new timesheet')
            roundedtime = 0
            timesheets = db.attendance.find(
                {"emp_id": session['emp_id'], "paid": 'no', "check_out": {"$exists": True, "$ne": ""}})
            if not list(timesheets):
                print('nothing to update')
            else:
                timesheets = db.attendance.find({"emp_id": session['emp_id'], "paid": 'no', "check_out": {"$exists": True, "$ne": ""}})
                for timesheet in timesheets:
                    if timesheet['rounded_time'] != '':
                        roundedtime += float(timesheet['rounded_time'])
                        print(timesheet)
                        db.attendance.update_one({'_id': timesheet['_id']}, {
                                                '$set': {'paid': 'yes'}})
                print(roundedtime*10)
                if paycheck['hours_worked'] =="":
                    hours_worked = roundedtime
                    db.payroll.update_one({'_id': paycheck['_id']}, {
                                       '$set': {'hours_worked': str(hours_worked)}}) 
                else:
                    hours_worked = float(paycheck['hours_worked'])+roundedtime
                employee = db.employee.find_one({"emp_id": session['emp_id']})
                hours_worked = round((float(paycheck['hours_worked'])+roundedtime),2)
                net_pay = round(hours_worked* float(employee['hourly_rate']),2)
                print(net_pay)
                tax_deduction= round(net_pay/10,2)
                db.payroll.update_one({'_id': paycheck['_id']}, {
                                       '$set': {'hours_worked': str(hours_worked),"net_pay":net_pay,"tax_deduction":tax_deduction,"paid":'no'}}) 
                

def generate_pdf(html):
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Convert the HTML to PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    # Return the generated PDF
    if pisa_status.err:
        return 'An error occurred: {}'.format(pisa_status.err)
    else:
        return buffer.getvalue()    

def timeData(id):
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    print(start_date)
    dbResponse = db.attendance.update_one({"_id": ObjectId(id)},
                                        {"$set": {"check_in": start_date, "check_out": end_date}})