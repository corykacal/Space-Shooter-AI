class student(object):

    def __init__(self,name,age):
        self.name = name
        self.age = age

    def getName(self):
        return self.name

    def getAge(self):
        return self.age





dylan = student(cory,21)

anand = student(anand,24)

print anand.getAge()
print dylan.getName()
