from app import app, db
from db_setup import init_db, db_session,engine

from flask import redirect, url_for, request, make_response, Response
from flask import send_from_directory, jsonify, render_template

from models import Class, Assignment, Grade

from sqlalchemy.sql import select

import os
import json

init_db()

#Class.__table__.drop(engine)
#Assignment.__table__.drop(engine)
#Grade.__table__.drop(engine)
db.create_all()
db_session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    all_classes = db_session.query(Class).all()
    options = []
    db_session.commit()
    for row in all_classes:
        options.append((row.id, row.name))
    
    if request.method == "GET":
        return render_template("index.html", options = options)
    
    if request.form.get("class"):
        course = request.form.get('class')
        return redirect(url_for('search', courseNum = course))


@app.route('/search', methods=['GET'])
def search():
    courseNum = request.args['courseNum']
    all_classes = db_session.query(Class).all()
    options = []
    for row in all_classes:
        options.append((row.id, row.name))

    if request.method == "GET":
        query = db_session.query(Class).filter_by(id=courseNum).first()
        courseInfo = [query.id, query.name, query.professor, query.time]

        assignmentQuery = db_session.query(Assignment).filter_by(class_id = courseNum).all()
        all_assignments = []
        totalPercent = 0
        count = 0

        for row in assignmentQuery:
            assignment = row.name

            grade = db_session.query(Grade).filter_by(assignment_id=row.id).order_by(Grade.id.desc()).first()

            totalPercent += grade.grade
            all_assignments.append([assignment, grade.grade, row.id])
            count += 1
        if count == 0:
            classGrade = 0
        else:
            classGrade = totalPercent / count

        db_session.commit()
        return render_template('results.html', options = options, course = courseInfo, grade = "{:.2f}".format(classGrade), results = all_assignments)
     
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "GET":
        course_num = request.args['courseNum']
        return render_template("addAssignment.html", course_num=course_num)
    
    name = request.form.get('assignment')
    course_num = request.form.get('courseNum')
    newAssignment =Assignment(name=name,class_id=course_num)
    db_session.add(newAssignment)
    db_session.commit()
    db_session.add(Grade(grade=0, assignment_id = newAssignment.id))
    db_session.commit()
    return redirect(url_for('search', courseNum=course_num))

@app.route('/delete', methods=['POST'])
def delete():
    courseNum = request.form.get('course')
    assignmentName = request.form.get('assignmentName')
    deleteAssignment = db_session.query(Assignment).filter_by(name=assignmentName, class_id = courseNum).first()
    db_session.delete(deleteAssignment)
    db_session.commit()
    return redirect(url_for('search', courseNum=courseNum))

@app.route('/saveGrade', methods=['POST'])
def saveGrade():
    assignId = request.form.get('assignmentId')
    newGrade = request.form.get('newGrade')
    db_session.add(Grade(grade=newGrade, assignment_id = assignId))
    db_session.commit()
    return redirect(url_for('search', courseNum=request.form.get('course')))

@app.route('/api/<courseNum>')
def getJSON(courseNum):
    all_assignments = db_session.query(Assignment).filter_by(class_id=courseNum).all()
    returnList = []
    assignmentsList=[]
    for assign in all_assignments:
        assignmentObject = {}
        assignmentObject['name'] = assign.name
        assignmentObject['assignment_id'] = assign.id
        grades = []
        gradeQuery = db_session.query(Grade).filter_by(assignment_id=assign.id).order_by(Grade.id.desc()).all()
        for grade in gradeQuery:
            gradeObject = {}
            gradeObject['grade_id'] = grade.id
            gradeObject['percent'] = grade.grade
            grades.append(gradeObject)
        assignmentObject['grades'] = grades
        returnList.append(assignmentObject)
    apiDictionary = {}
    classQuery = db_session.query(Class).filter_by(id=courseNum).first()
    apiDictionary['course_num'] = courseNum
    apiDictionary['course_name'] = classQuery.name
    apiDictionary['professor'] = classQuery.professor
    apiDictionary['time'] = classQuery.time
    apiDictionary['assignments'] = returnList

    return json.dumps(apiDictionary)
 
if __name__ == '__main__':
    app.run()