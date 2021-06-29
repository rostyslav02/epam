from flask import render_template, Blueprint, url_for, request, redirect, g, flash
from main import db
from models import Employee, Department


views = Blueprint('views', __name__)


@views.route('/search/<string:search>')
def Search(search):
    empl_id = []
    empl = Employee.query
    deps = Department.query.filter_by(name=search)
    for item in empl:
        if item.name == search or item.surname == search:
            empl_id.append(item.id)
    empl_id.unique()
    empls = []
    for item in empl.id:
        temp = Employee.query.filter_by(id=item).first()
        empls.append(temp)
    return render_template('search.html', employees=empls, departs=deps)

@views.route('/')
def start():
    return redirect(url_for('views.logging'))


@views.route('/loging', methods=["POST", "GET"])
def logging():
    if request.method == "POST":
        email = request.form['e-mail']
        pasw = request.form['password']
        empl = Employee.query.filter_by(email=email).first()
        if empl.password == pasw:
            return redirect(url_for('views.empllist'))
        else:
            flash("The wrong login or password", type="fail")
    return render_template("authorisation.html")


@views.route('/department')
def departlist():
    departs = Department.query
    lst = []
    for item in departs:
        temp = {}
        temp['name'] = item.name
        temp['id'] = item.id
        empl = Employee.query.filter_by(department_id=item.id)
        sum = 0
        n = 0
        for item in empl:
            sum += item.salary
            n += 1
        if n == 0:
            n = 1
        temp['salary'] = sum / n
        lst.append(temp)
    print(lst)
    return render_template("department_list.html", lst=lst)

@views.route('/departmntInfo/<int:id>')
def departInfo(id):
    depart = Department.query.filter_by(id=id).first()
    salary = 0
    k = 0
    empls = Employee.query.filter_by(department_id=id)
    for item in empls:
        salary += item.salary
        k += 1
    empls = Employee.query.filter_by(department_id=id)
    lst = []
    for item in empls:
        lst.append(item)
    for item in lst:
        dep = Department.query.filter_by(id=item.department_id).first()
        item.department_id = dep.name
    return render_template('department_info.html', name=depart.name, avSalary=salary/k, list=lst)


@views.route('/employeeInfo/<int:id>')
def emplInfo(id):
    empl = Employee.query.filter_by(id=id).first()
    dep = Department.query.filter_by(id=empl.department_id).first()
    empl.department_id = dep.name
    return render_template('employee_info.html', lst=empl)


@views.route('/employeesList', methods=["GET", "POST"])
def empllist():
    empls = Employee.query
    lst = []
    for item in empls:
        lst.append(item)
    for item in lst:
        dep = Department.query.filter_by(id=item.department_id).first()
        item.department_id = dep.name
    return render_template("employee_list.html", list=lst)


@views.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        name = str(request.form['name'])
        sname = str(request.form['sname'])
        depart = str(request.form['depart'])
        salary = int(request.form['salary'])
        email = str(request.form['e-mail'])
        password = str(request.form['password'])
        dep = Department.query
        chek = False
        for item in dep:
            if str(item.name) == depart:
                dep = Department.query.filter_by(name=depart).first()
                chek = True
                break
        if not chek:
            flash("Department does not exist")
            return render_template("registration.html")
        if request.form['password'] != request.form['cpassword']:
            flash("Password and confirm password fields are not equal")
            return render_template("registration.html")
        try:
            db.session.add(Employee(name, sname, dep.id, salary, email, password))
            db.session.commit()
        except:
            flash("Fail")
        else:
            return redirect(url_for('views.empllist'))
    return render_template("registration.html")


