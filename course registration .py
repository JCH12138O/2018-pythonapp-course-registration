import os.path
import os

def processProgramFile(pathName):
    # construct file path
    filePath1 = os.path.join(pathName, 'program1.txt')
    filePath2 = os.path.join(pathName, 'program2.txt')
    # read program1 and  remove title line
    infile1 = open(filePath1, 'r')
    file1 = infile1.read().split('\n')
    title = ['Program ONE', 'Program TWO']
    # create a set of program1 description for program1
    s1 = set()
    for r in file1:
        if r in title:
            file1.remove(r)
        else:
            s1.add(r)
    infile1.close()
    # convert set into lists and combine as dictionary
    s1 = list(s1)
    list1f1 = []
    list2f1 = []
    for r in s1:
        list1f1.append(r[:r.find(' ')])
        list2f1.append(r[r.find(" ") + 1:])
    description1 = zip(list1f1, list2f1)
    dic1 = dict((list1f1, list2f1) for list1f1, list2f1 in description1)
    # read program2 and remove title
    infile2 = open(filePath2, 'r')
    file2 = infile2.read().split('\n')
    s2 = set()
    for r in file2:
        if r in title:
            file2.remove(r)
        else:
            s2.add(r)
    infile2.close()
    # convert set into lists and combine as dictionary
    s2 = list(s2)
    list1f2 = []
    list2f2 = []
    for r in s2:
        list1f2.append(r[:r.find(' ')])
        list2f2.append(r[r.find(" ") + 1:])
    description2 = zip(list1f2, list2f2)
    dic2 = dict((list1f2, list2f2) for list1f2, list2f2 in description2)
    # construct a tuple of program1 and program2
    result = (('Program ONE', dic1), ('Program TWO', dic2))
    return result


def processPrereqsFile(pathName):
    # read course prerequisites line by line
    fileName = os.path.join(pathName, 'prereqs.txt')
    inFile = open(fileName, 'r')
    file = str(inFile.readline())
    list1 = []
    list2 = []
    # create lists of every lines
    while file:
        if file.find('\n') != -1:
            file = file[:file.find('\n')]
        list1.append(file[:file.find(':')])
        list2.append(file[file.find(':')+2:].split())
        file = inFile.readline()
    # combine lists into dictionary for prerequisites
    prereq = zip(list1, list2)
    dic = dict((list1, list2) for list1, list2 in prereq)
    return dic


def processClassFiles(pathName):
    # get all doc names in the folder and delete other three files names
    lst = os.listdir(pathName)
    del(lst[-3:])
    # get course number out of file names
    courseList = []
    for i in lst:
        courseList.append(i[1:5])
    courseList = set(courseList)
    # create dic from files names
    dic = {}
    for i in courseList:
        s = set()
        for course in lst:
            if course[1:5] == i:
                file = open(os.path.join(pathName, course), 'r')
                text = file.readline()
                while text:
                    s.add(text[:text.find(' ')])
                    text = file.readline()
        dic[i] = s
    return dic


def initFromFiles(pathName):
    t = (processProgramFile(pathName), processClassFiles(pathName), processPrereqsFile(pathName))
    return t


def estimateClass(pathName,courseNumber):
    t = initFromFiles(pathName)
    setTotal = set()
    listCourse = ['2005', '2075', '2300', '2470', '2600', '1100', '1001', '1250', '1380', '1420']
    # test if input course number is in the course list
    if courseNumber in listCourse:
        # name set for all students
        for sets in t[1].values():
            setTotal = setTotal.union(sets)
        # get name set of input course number
        setTaken = t[1].get(courseNumber)
        # if input course have a prerequisite
        if courseNumber in t[2]:
            # get set of names that able to take course
            setPre = set()
            time = 0
            while time < len(t[2].get(courseNumber)):
                if time == 0 :
                    setPre = t[1].get(t[2].get(courseNumber)[0])
                else:
                    setPre = setPre.intersection(t[1].get(t[2].get(courseNumber)[time]))
                time += 1
            # from people who can take and not took before
            setFinal = setPre.difference(setTaken)
        else:
            # from all people and who not took before
            setFinal = setTotal.difference(setTaken)
    else:
        #   wrong input number results empty set
        setFinal = setTotal
    return setFinal


def classSet(pathName):
    # create a set of all distinct courses
    filePath1 = os.path.join(pathName, 'program1.txt')
    filePath2 = os.path.join(pathName, 'program2.txt')
    infile1 = open(filePath1, 'r')
    file1 = infile1.read().split('\n')
    title = ['Program ONE', 'Program TWO']
    s1 = set()
    for r in file1:
            s1.add(r)
    infile1.close()

    infile2 = open(filePath2, 'r')
    file2 = infile2.read().split('\n')
    for r in file2:
            s1.add(r)
    infile2.close()
    return s1


def main():
    direcName = input("Please enter the name of subfolder with files:")
    courseNumber = input('Enter course number or press enter to stop:')
    while courseNumber != '':
        pathName = os.path.join(os.getcwd(), direcName)
        if os.path.exists(pathName) is False:
            os.mkdir(pathName)
        number = len(estimateClass(pathName, courseNumber))
        t = initFromFiles(pathName)
        list1 = list(classSet(pathName))
        count = 0
        for i in list1:
            if i[:4] == courseNumber:
                description = i
                count += 1
        if count == 0:
            description = str(courseNumber) + ' None'
        print('There are ' + str(number) + ' students who could take course ' + description)
        courseNumber = input('Enter course number or press enter to stop:')


main()