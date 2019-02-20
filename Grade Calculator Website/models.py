from app import db


class Class(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, nullable=False)
    professor = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)

    def __init__(self, id, name, professor, time):
        self.id=id
        self.name=name
        self.professor=professor
        self.time=time
    
    def __repr__(self):
        return "Course Num: {}, Course Name: {}, Professor: {}, Time: {}".format(self.id, self.name, self.professor, self.time)

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
 
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"))

    # def __repr__(self):
    #     return "Id: {}, Assignment Name: {}, Class For: {}".format(self.id, self.name, self.class_id)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.Integer)

    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))