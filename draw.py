from numpy import array
from numpy.random import normal
from matplotlib import pyplot


def genData():
    heights = []
    weights = []
    grades = []
    N = 100

    for i in range(N):
        while True:
            height = normal(172, 6)
            if 0 < height: break
        while True:
            weight = (height - 80) * 0.7 + normal(0, 1)
            if 0 < weight: break
        while True:
            score = normal(70, 15)
            if 0 <= score and score <= 100:
                grade = 'E' if score < 60 else ('D' if score < 70 else ('C' if score < 80 else ('B' if score < 90 else 'A')))
                break
        heights.append(height)
        weights.append(weight)
        grades.append(grade)
    return array(heights), array(weights), array(grades)

heights, weights, grades = genData()




def drawBar(grades):
    xticks = ['A', 'B', 'C', 'D', 'E']
    gradeGroup = {}
    for grade in grades:
        gradeGroup[grade] = gradeGroup.get(grade, 0) + 1
    pyplot.bar(range(5), [gradeGroup.get(xtick, 0) for xtick in xticks], align='center')

    pyplot.xticks(range(5), xticks)

    pyplot.xlabel('Grade')
    pyplot.ylabel('Frequency')
    pyplot.title('Grades Of Male Students')
    pyplot.show()

#drawBar(grades)

def drawPie(grades):
    labels = ['A', 'B', 'C', 'D', 'E']
    gradeGroup = {}
    for grade in grades:
        gradeGroup[grade] = gradeGroup.get(grade, 0) + 1
    pyplot.pie([gradeGroup.get(label, 0) for label in labels], labels=labels, autopct='%1.1f%%')
    pyplot.title('Grades Of Male Students')
    pyplot.show()

#drawPie(grades)


def drawHist(heights):
    print 'Height:', heights
    pyplot.hist(heights, 20)
    pyplot.xlabel('Heights')
    pyplot.ylabel('Frequency')
    pyplot.title('Heights Of Male Students')
    pyplot.show()

#drawHist(heights)

def drawScatter(heights, weights):
    pyplot.scatter(heights, weights)
    pyplot.scatter(heights, heights)
    pyplot.xlabel('Heights')
    pyplot.ylabel('Weights')
    pyplot.title('Heights & Weights Of Male Students')
    pyplot.show()

drawScatter(heights, weights)
