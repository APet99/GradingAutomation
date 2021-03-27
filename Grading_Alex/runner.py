from utils.github_integration import repo_helper
from utils.java_compilation import compile
import git
import os
import os.path
import subprocess

#Github prefix
course = 'EGR222'
semester = 'SP20'
assignment = 'hw4'

inst_test='AssassinManagerInstructorTest' # Name of the instructor test file
save_dir = './repos/{Course}/{Assignment}/'.format(Course=course, Assignment= assignment)
assignment_link = 'http://github.com/cbu-{Course}-{Semester}/{Assignment}-'.format(Course = course, Semester=semester, Assignment=assignment)
test_files = 'C:/Users/Alex/Desktop/Grading_Alex/repos/{Course}/{Assignment}/{Inst_Test}.java'.format(Course=course, Assignment=assignment, Inst_Test=inst_test)


file = open('{}-{}-Roster'.format(course, semester),"r")
students = file.readlines()
student_names = []
student_usernames = []
student_links = []
student_folders = []

def prepare_student():
    for student in students:
        student = student.split()
        student_names.append(student[0] + '_' + student[1])
        student_usernames.append(student[-1])
        student_links.append(assignment_link + student[-1])
        student_folders.append(save_dir + student[0] + '_' + student[1])
        
def pull_all_student_repos():
        i = 0;
        while i < len(student_links):
            print('\nPulling repo for: ' + student_names[i])
            repo_helper.clone_repo(student_links[i], student_folders[i])
            i+=1
            print('\n\n')

def is_passing(results):
    return results.splitlines()[:-1][:2] == 'OK'

def test_all_students(cwd):
    for repo in student_folders:
        os.chdir(repo)

        try:
            source_files = [os.path.join('src', fn) for fn in os.listdir('src') if fn[-5:] == '.java']
            #tst_files = [fn for fn in 'tst' if fn[-5:] == '.java']
        except FileNotFoundError:
            pass


        for file in source_files:
            student_output = "student_report.txt"
            with open(student_output, 'w') as stdout_file:
                    try:
                        #Compile java classes and tests
                        subprocess.run(['javac', '-cp', '.;C:/Users/Alex/Desktop/Grading_Alex/utils/java_compilation/java_dependencies/junit-4.13.jar;C:/Users/Alex/Desktop/Grading_Alex/utils/java_compilation/java_dependencies/hamcrest-core-1.3.jar',
                            *source_files, test_files,'-d', '.'])
                        #Execute tests against compiled classes
                        result = subprocess.run(['java', '-cp', '.;C:/Users/Alex/Desktop/Grading_Alex/utils/java_compilation/java_dependencies/junit-4.13.jar;C:/Users/Alex/Desktop/Grading_Alex/utils/java_compilation/java_dependencies/hamcrest-core-1.3.jar',
                            'org.junit.runner.JUnitCore', inst_test], stdout=stdout_file, timeout=5)
                    except subprocess.TimeoutExpired:
                        pass
                    except FileNotFoundError:
                        pass
        os.chdir(cwd)
        


prepare_student()
pull_all_student_repos()

cwd = os.getcwd()

#test_all_students(cwd)
