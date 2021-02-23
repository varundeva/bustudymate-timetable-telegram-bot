import csv
import json


def getTimeTable(callBackData):
    with open('timetable.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        timetable = []
        heading = []
        for i, row in enumerate(csv_reader):
            if i == 0:
                heading = row
            elif (callBackData[0].lower() == row[0].lower()) and (callBackData[1].lower() == row[4].lower()) and (callBackData[2].lower() == row[1].lower()):
                timetable.append(dict(zip(heading, row)))
    return timetable


def getAllCourseOfSemester(callBackData):
    with open('timetable.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        courses = []
        for course in csv_reader:
            if (course[1] not in courses) and (callBackData[0].lower() == course[0].lower()) and (callBackData[1].lower() == course[4].lower()):
                courses.append(course[1])

    return courses


def getAllUniversities():
    with open('timetable.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        university = []
        for uni in csv_reader:
            if uni[0] not in university:
                university.append(uni[0])

    return university[1:]


def getAllSemesterOfUniversity(universityName):
    with open('timetable.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        semesters = []
        for sem in csv_reader:
            if (sem[4] not in semesters) and (sem[0].lower() == universityName.lower()):
                semesters.append(sem[4])
    return semesters
