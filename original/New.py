class Employee:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
    #    self.email = first + '.' + '@email.com'

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return '{}.{}@email.com'.format(self.first, self.last)


emp1 = Employee('hasnath', 'Emon', 20000)

emp1.first = "Noor"

print(emp1.email, emp1.fullname())
