import time

def convertToTitleCase(sentence):
    words = sentence.split()
    for number, word in enumerate(words):
        if word not in ["to", "and", "of"]:
            words[number] = word.capitalize()
    return " ".join(words)

def checkFile(fileName):
    try:
        with open(f"{fileName}.txt", "r") as file:
            if len(file.readline()) > 1:
                return True
    except:
        return False

def fileWrite(value, fileName):
    if checkFile(fileName):
        with open(f"{fileName}.txt", "r+") as file:
            for lastLine in file:
                pass
            if "\n" not in lastLine:
                file.write("\n")
            file.write(value)
    else:
        with open(f"{fileName}.txt", "a") as file:
            file.write(value)

def getLineNumber(value, fileName):
    if checkFile(fileName):
        with open(f"{fileName}.txt", "r") as file:
            for number, line in enumerate(file):
                if value in line:
                    return number
    return "*"

def changeLine(lineNumber, value, fileName):
    with open(f"{fileName}.txt", "r+") as file:
        data = file.readlines()
        data.pop(lineNumber)
        if fileName == "course":
            data.insert(lineNumber, f'{value["CourseCode"]};{value["CourseName"]};{value["InstructorName"]};{str(value["StudentNumber"])}\n')
        elif fileName == "student":
            data.insert(lineNumber, f'{value["StudentId"]};{value["StudentName"]};{value["Courses"]}\n')
        file.seek(0)
        file.writelines(data)

def sameCourseChecker(value):
    with open("course.txt", "r") as file:
        num = 0
        for lines in file:
            if value in lines:
                num += 1
        return num

def getValue(line, fileName):
    with open(f"{fileName}.txt", "r") as file:
        for index, lines in enumerate(file):
            if index == line:
                list = lines.split(";")
                if fileName == "course":
                    return {"CourseCode":list[0], "CourseName":list[1], "InstructorName":list[2], "StudentNumber":int(list[3])}
                return {"StudentId":list[0], "StudentName":list[1], "Courses":list[2]}

def addCourse():
    courseCode = input("Please enter the course code: ").upper()
    instructorName = convertToTitleCase(input("Please enter the instructor name: "))
    lineNum = getLineNumber(courseCode, "course")
    if lineNum != "*":
        courseName = getValue(lineNum, "course")["CourseName"]
        if getLineNumber(f"{courseName};{instructorName}", "course") == "*":
            fileWrite(f"{courseCode};{courseName};{instructorName};0", "course")
            print(f"Course has been registered: {courseCode}, {courseName}, {instructorName}")
        else:
            print("This course has been already registered!")
    else:
        courseName = convertToTitleCase(input("Please enter the course name: "))
        fileWrite(f"{courseCode};{courseName};{instructorName};0", "course")
        print(f"Course has been registered: {courseCode}, {courseName}, {instructorName}")

def registerStudent():
    id = int(input("Please enter the student id: "))
    code = input("Please enter the course code.").upper()
    lineNumberC = getLineNumber(code, "course")
    if lineNumberC == "*":
        print("Course not Found!")
    else:
        course = getValue(lineNumberC, "course")
        instructorNumber = sameCourseChecker(f'{course["CourseCode"]};{course["CourseName"]}')
        if instructorNumber > 1:
            instructorName = input(f"There are {str(instructorNumber)} instructors! Please enter the instructor name:")
            lineNumberC = getLineNumber(f'{course["CourseName"]};{instructorName};', "course")
            if lineNumberC != "*":
                course = getValue(lineNumberC, "course")
            else:
                print("There is no instructor by this name")
                return
        course["StudentNumber"] = int(course["StudentNumber"]) + 1
        linenumberS = getLineNumber(f"{str(id)};", "student")
        if linenumberS != "*":
            student = getValue(linenumberS, "student")
            studentCourses = str(student["Courses"]).rstrip()
            student["Courses"] = studentCourses + "," + code
            if code not in studentCourses:
                changeLine(linenumberS, student, "student")
                changeLine(lineNumberC, course, "course")
                print("Student has been registered.")
            else:
                print("This student has been already registered this course!")
        else:
            name = convertToTitleCase(input("Please enter the student name: "))
            changeLine(lineNumberC, course, "course")
            fileWrite(f'{str(id)};{name};{code}', "student")
            print("Student has been registered.")

def top3Courses():
    if checkFile("course"):
        with open("course.txt", "r") as file:
            studentDictionary = {}
            for index, lines in enumerate(file):
                course = lines.split(";")
                studentDictionary[index] = int(course[3].rstrip())
            dictionary = dict(sorted(studentDictionary.items(), key=lambda item: item[1], reverse=True))
            num = 1
            print("TOP 3 Most Crowded Courses:")
            print("")
            for i in dictionary:
                if num <= 3:
                     x = getValue(i, "course")
                     print(f'{str(num)}) Course Code: {x["CourseCode"]}, Course Name: {x["CourseName"]}, Instructor Name: {x["InstructorName"]}, Student Number in the Class: {int(x["StudentNumber"])}')
                     num += 1
    else:
        print("There is no course which has been registered at all!")

def top3Students():
    if checkFile("student"):
        with open("student.txt", "r") as file:
            studentDictionary = {}
            for index, lines in enumerate(file):
                student = lines.split(";")
                course = student[2].replace("\n", "").split(",")
                studentDictionary[index] = int(len(course))
            dictionary = dict(sorted(studentDictionary.items(), key=lambda item: item[1], reverse=True))
            num = 1
            print("Top 3 students with the most course registrations: ")
            print("")
            for i in dictionary:
                if num <= 3:
                    x = getValue(i, "student")
                    x["Courses"] = x["Courses"].replace("\n", "")
                    print(f'{str(num)}) ID: {x["StudentId"]}, Name: {x["StudentName"]}, Courses: {x["Courses"]}')
                    num += 1
    else:
        print("There is no student who has been registered at all!")

def listCourses(type):
    if checkFile("course"):
        with open("course.txt", "r") as file:
            if type == "code" or type == "name":
                name = input(f"Please enter the course {type}: ")
                if type == "code":
                    name = name.upper()
                else:
                    name = convertToTitleCase(name)
            list = []
            num = 1
            for lines in file:
                course = lines.split(";")
                if type == "name":
                    if name in course[1]:
                        list.append(f"{str(num)}) Course Code: {course[0]}, Course Name: {course[1]}, Instructor Name: {course[2]}, Student number in the class: {str(course[3].rstrip())}")
                        num += 1
                elif type == "code":
                    if name in course:
                        list.append(f"{str(num)}) Course Code: {course[0]}, Course Name: {course[1]}, Instructor Name: {course[2]}, Student number in the class: {str(course[3].rstrip())}")
                        num += 1
                elif type == "least":
                    if int(course[3]) != 0:
                        list.append(f"{str(num)}) Course Code: {course[0]}, Course Name: {course[1]}, Instructor Name: {course[2]}, Student number in the class: {str(course[3].rstrip())}")
                        num += 1
                else:
                    list.append(f"{str(num)}) Course Code: {course[0]}, Course Name: {course[1]}, Instructor Name: {course[2]}, Student number in the class: {str(course[3].rstrip())}")
                    num += 1
            if list != []:
                print("\n".join(list))
            else:
                print("Course not found!")
    else:
        print("There is no course which has been registered at all!")

def listStudents():
    if checkFile("student"):
        with open("student.txt", "r") as file:
            num = 1
            for lines in file:
                student = lines.split(";")
                print(str(num)+")", "ID:", student[0], "Name:", student[1], "Courses:", student[2].replace("\n", ""))
                num += 1
    else:
        print("There is no student who has been registered at all!")

def registerAdminMenu():
    functionList = [addCourse, registerStudent, listStudents, top3Courses, top3Students]
    type = ["*", "least", "code", "name"]
    while True:
        print("1-List all the courses")
        print("2-List all the course that have at least one student registered")
        print("3-Search a course by course code")
        print("4-Search a course by name")
        print("5-Add a new course")
        print("6-Register a student to a course")
        print("7-List all the students their registered courses.")
        print("8-List top 3 most crowded courses")
        print("9-List top 3 students with the most course registrations")
        print("0-Exit")
        choice = int(input("Please select an operation you want to do (0-9): "))
        print("\n")
        if choice == 0:
            print("Exited")
            break
        elif choice <= 4 and choice >= 1:
            print("The operation has been selected:", choice)
            print("\n")
            listCourses(type[choice-1])
            time.sleep(2)
            print("\n" * 2)
        elif choice <= 9:
            print("The operation has been selected:", choice)
            print("\n")
            functionList[choice-5]()
            time.sleep(2)
            print("\n" * 2)
        else:
            print("Please enter the number between 0 and 9!")

registerAdminMenu()