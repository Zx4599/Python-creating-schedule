import json
import re
from collections import defaultdict


def StudyPlan():
    studyplan = []
    with open('CEStudyPlan.txt', 'r') as studyplanfile:
        studyplanlines = studyplanfile.readlines()
    years = int(studyplanlines[len(studyplanlines) - 1][0])
    for i in range(years):
        for j in range(3):
            temp = [i + 1, j + 1]
            for k in studyplanlines[1:]:
                k = k.split(',')
                k[2] = re.sub('\n$', '', k[2])
                if str(k[0]) == str(i + 1) and str(k[1]) == str(j + 1):
                    temp.append(k[2])
            if len(temp) >= 3:
                studyplan.append(temp)
    return studyplan


def Pstudyplan(studyplan):
    print("Year Semester Courses")
    for i in studyplan:
        print(str(i[0]) + '\t\t' + str(i[1]) + '\t  ', end='')
        for courses in i[2:]:
            print(courses + ', ', end='')
        print('')


def Student_record():
    while True:
        Student_recordpath = input("Please enter the path to the student records file: ")
        try:
            with open(Student_recordpath, 'r') as Student_recordfile:
                Student_recordlines = Student_recordfile.readlines()
                break
        except FileNotFoundError:
            print("Error, file not found!")
    Student_record = []
    for line in Student_recordlines[1:]:
        line = line.split(',')
        year = line[0]
        semester = line[1]
        courses = line[2:]
        coursesrecords = {}
        for course in courses:
            course = course.split(':')
            coursecode = course[0]
            courserecord = course[1]
            courserecord = re.sub('\n$', '', courserecord)
            coursesrecords[coursecode] = courserecord
        Student_record.append((year, semester, coursesrecords))
    return Student_record


def PrintRecord(Student_record):
    print("Year Semester Courses")
    for i in Student_record:
        print(str(i[0]) + '\t\t' + str(i[1]) + '\t  ', end='')
        for coursesrecords in i[2]:
            print(coursesrecords + ':' + i[2][coursesrecords] + ', ', end='')
        print('')


def PrintStudnet(Student_record, studyplan):
    print("Year Semester Courses")
    for studyplanline in studyplan:
        print(str(studyplanline[0]) + '\t\t' + str(studyplanline[1]) + '\t  ', end='')
        for courses in studyplanline[2:]:
            for studentrecordline in Student_record:
                if studentrecordline[0] == str(studyplanline[0]) and studentrecordline[1] == str(studyplanline[1]):
                    if courses in studentrecordline[2] and studentrecordline[2][courses] >= '60':
                        print('\033[32m' + courses + ',' + '\033[0m' + ' ', end='')
                        break
                    else:
                        print(courses + ', ', end='')
                        break
            else:
                print(courses + ', ', end='')
        print('')


def Prequisites():
    prequisites = {}
    with open('CEStudyPlan.txt', 'r') as studyplanfile:
        studyplanlines = studyplanfile.readlines()
    for line in studyplanlines[1:]:
        line = re.sub('\n$', '', line)
        line = line.split(',')
        if len(line) > 3:
            temp = line[3:]
            prequisites[line[2]] = temp
    return prequisites


def PrintPrequisites(prequisites):
    for course in prequisites:
        print(course + ': ', end='')
        for prequisite in prequisites[course]:
            print(prequisite + ', ', end='')
        print('')


def parse_elective_courses():
    elective_courses = []
    with open('Electives.txt', 'r') as f:
        for line in f:
            group, course_code, *prequisites = line.strip().split(',')
            if prequisites:
                prequisites = prequisites[0].split(':')
                prequisites = [prerequisite.split(':')[0] for prerequisite in prequisites]
                elective_courses.append((course_code, prequisites))
            else:
                elective_courses.append((course_code, []))
    return elective_courses


with open("CourseBrowser_1.json") as fs:
    First = json.load(fs)

with open("CourseBrowser_2.json") as sc:
    Second = json.load(sc)

with open("CourseBrowser_3.json") as sm:
    Summer = json.load(sm)


def calculate_total_credits(courses):
    total_credits = sum(int(course[2]) for course in courses)
    return total_credits


def get_eligible_courses(studyplan, Student_record, prerequisites):
    completed_courses = []
    for studyplanline in studyplan:
        for courses in studyplanline[2:]:
            for studentrecordline in Student_record:
                if studentrecordline[0] == str(studyplanline[0]) and studentrecordline[1] == str(studyplanline[1]):
                    if courses in studentrecordline[2] and int(studentrecordline[2][courses]) >= 60:
                        completed_courses.append(courses)

    eligible_courses = []
    for year, semester, *courses in studyplan:
        for course in courses:
            if course not in completed_courses and all(
                    prerequisite in completed_courses for prerequisite in prerequisites.get(course, [])):
                eligible_courses.append((year, semester, course))
                # print(f"Added eligible course: year={year}, semester={semester}, course={course}")

    return eligible_courses


def sort_eligible_courses(eligible_courses, study_plan, prerequisites):
    # Create a dictionary to map courses to their position in the study plan
    course_order = {}
    for i, plan in enumerate(study_plan):
        for course in plan[2:]:
            course_order[course] = i

    # Define a custom sort key function
    def sort_key(course):
        year, semester, course_code = course
        # Sort by the year and semester according to the study plan
        order = course_order[course_code]
        # Sort by the number of prerequisites
        num_prereqs = len(prerequisites.get(course_code, []))
        return (order, year, semester, -num_prereqs, course_code)

    # Sort the eligible courses using the custom sort key function
    sorted_courses = sorted(eligible_courses, key=sort_key)

    return sorted_courses


def PrintStudentP(schedules, studyplan):
    print("Year Semester Courses")
    print("---- -------- -------")
    for studyplanline in studyplan:
        print(str(studyplanline[0]) + '\t\t' + str(studyplanline[1]) + '\t  ', end='')
        for courses in studyplanline[2:]:
            for studentrecordline in schedules:
                if studentrecordline[0] == str(studyplanline[0]) and studentrecordline[1] == str(studyplanline[1]):
                    if courses in studentrecordline[2] and studentrecordline[2][courses] >= '60':
                        print('\033[32m' + courses + ',' + '\033[0m' + ' ', end='')
                        break
                    else:
                        print(courses + ', ', end='')
                        break
            else:
                print(courses + ', ', end='')
        print('')


def generate_schedules(sorted_courses, max_first_credits, max_second_credits, max_summer_credits, num_of_schedules):
    # Initialize schedules list
    elective_courses = parse_elective_courses()
    schedules = []
    for s in range(num_of_schedules):
        # Initialize semester counters
        first_semester_courses = {}
        second_semester_courses = {}
        summer_courses = {}
        # Initialize credit counters
        first_semester_credits = 0
        second_semester_credits = 0
        summer_credits = 0
        # Iterate over the sorted courses list
        for course in sorted_courses:
            # Extract year, semester, and course code from the course tuple
            year, semester, course_code = course
            # Calculate the number of credits based on the course code
            try:
                num_of_credits = int(course_code[5])
            except ValueError:
                print(f"Invalid number of credits for course {course_code}. Skipping this course.")
                continue

            # Check if the course is a UE course
            if "UE" in course_code:
                # Select a random elective course
                if elective_courses:
                    elective_course = random.choice(elective_courses)
                    elective_courses.remove(elective_course)
                    elective_course_code, elective_num_of_credits = elective_course
                    course_code = elective_course_code
                    num_of_credits = elective_num_of_credits
                else:
                    # No more elective courses available
                    print(f"No more elective courses available. Skipping course {course_code}.")
                    continue
            # Check if the course can fit in the current semester
            if semester == 1 and first_semester_credits + num_of_credits <= max_first_credits:
                first_semester_courses[course_code] = num_of_credits
                first_semester_credits += num_of_credits

            elif semester == 2 and second_semester_credits + num_of_credits <= max_second_credits:
                second_semester_courses[course_code] = num_of_credits
                second_semester_credits += num_of_credits
            elif summer_credits + num_of_credits <= max_summer_credits:
                summer_courses[course_code] = num_of_credits
                summer_credits += num_of_credits

            # Do not include the course if it cannot fit in any semester
            else:
                continue
        # Append the current schedule to the schedules list
        schedules.append((first_semester_courses, second_semester_courses, summer_courses))
        sorted_courses = [c for c in sorted_courses if c not in list(first_semester_courses.items()) + list(second_semester_courses.items()) + list(summer_courses.items())]

    # Print the schedules
    for i, schedule in enumerate(schedules):
        print(f"Schedule {i + 1}:")
        first_semester, second_semester, summer_semester = schedule
        if first_semester:
            print("First semester:")
            first_semester_credits = sum(first_semester_courses.values())
            for course, credits in first_semester_courses.items():
                print(f"  - {course} ({credits} credits)")
            print(f"  Total credits: {first_semester_credits}")
        if second_semester:
            print("Second semester:")
            second_semester_credits = sum(second_semester_courses.values())
            for course, credits in second_semester_courses.items():
                print(f"  - {course} ({credits} credits)")
            print(f"  Total credits: {second_semester_credits}")
        if summer_semester:
            print("Summer semester:")
            summer_credits = sum(summer_courses.values())
            for course, credits in summer_courses.items():
                print(f"  - {course} ({credits} credits)")
            print(f"  Total credits: {summer_credits}")

        print("\n")
    # Ask the user whether to save the suggested courses to a text file
    while True:
        save_to_file = input("Do you want to save the suggested courses to a text file? (y/n): ").lower()
        if save_to_file == "y":
            # Write schedules to text file
            with open("SuggestedCourses.txt", "w") as f:
                for i, schedule in enumerate(schedules):
                    f.write(f"Schedule {i + 1}:\n")
                    first_semester, second_semester, summer_semester = schedule
                    if first_semester:
                        f.write("First semester:\n")
                        first_semester_credits = sum(first_semester_courses.values())
                        for course, credits in first_semester_courses.items():
                            f.write(f"  - {course} ({credits} credits)\n")
                        f.write(f"  Total credits: {first_semester_credits}\n")
                    if second_semester:
                        f.write("Second semester:\n")
                        second_semester_credits = sum(second_semester_courses.values())
                        for course, credits in second_semester_courses.items():
                            f.write(f"  - {course} ({credits} credits)\n")
                        f.write(f"  Total credits: {second_semester_credits}\n")
                    if summer_semester:
                        f.write("Summer semester:\n")
                        summer_credits = sum(summer_courses.values())
                        for course, credits in summer_courses.items():
                            f.write(f"  - {course} ({credits} credits)\n")
                        f.write(f"  Total credits: {summer_credits}\n")
                    f.write("\n")
            print("Suggested courses have been saved to 'SuggestedCourses.txt'")
            break
        elif save_to_file == "n":
            while True:
                exit_program = input("Do you want to exit the program? (y/n): ").lower()
                if exit_program == "y":
                    exit()
                elif exit_program == "n":
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    return schedules


studyplan = StudyPlan()
print("Printing study plan....")
Pstudyplan(studyplan)
Student_record = Student_record()
print("Printing student plan....")
PrintStudnet(Student_record, studyplan)
prequisites = Prequisites()
print("Printing prequisites....")
PrintPrequisites(prequisites)
eligible_courses = get_eligible_courses(studyplan, Student_record, prequisites)
sorted_courses = sort_eligible_courses(eligible_courses, studyplan, prequisites)
for year, semester, course in sorted_courses:
    print(f"Year: {year}, Semester: {semester}, Course Code: {course}")

while True:
    try:
        minimum_free_days = int(input("Please enter the number of free days you want per week: "))
        if minimum_free_days > 5 or minimum_free_days < 0:
            print("Error, number of free days is not valid!")
            continue
        max_first_credits = int(
            input("Please enter the maximum number of credits you want to take for the first semester: "))
        if max_first_credits > 18 or max_first_credits < 1:
            print("Error, number of credits for the first semester is not valid!")
            continue
        max_second_credits = int(
            input("Please enter the maximum number of credits you want to take for the second semester: "))
        if max_second_credits > 18 or max_second_credits < 1:
            print("Error, number of credits for the second semester is not valid!")
            continue
        max_summer_credits = int(
            input("Please enter the maximum number of credits you want to take for the summer semester: "))
        if max_summer_credits > 9 or max_summer_credits < 1:
            print("Error, number of credits for the summer semester is not valid!")
            continue
        break
    except ValueError:
        print("Error, please enter a number!")

while True:
    try:
        num_of_semesters = int(input("Please enter the number of semesters "
                                     "you want to do the schedule planning for: "))
        break
    except ValueError:
        print("Error, please enter a number!")

# Generate schedules
schedules = generate_schedules(sorted_courses, max_first_credits, max_second_credits, max_summer_credits, num_of_semesters)

PrintStudentP(schedules, studyplan)
