from main import db


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    salary = db.Column(db.Integer)
    password = db.Column(db.String(100))

    def __init__(self, nam, sunam, depart, sal, em, pas):
        self.name = nam
        self.surname = sunam
        self.email = em
        self.department_id = depart
        self.salary = sal
        self.password = pas

    def __repr__(self):
        return '<Employee %r>' % self.id


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    employee = db.relationship('Employee', backref='department', lazy=True)


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Employee %r>' % self.id