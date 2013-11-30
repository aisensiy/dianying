class A(object):
    @property
    def name(self):
        """docstring for name"""
        return 'aisensiy'

    @name.setter
    def name(self, value):
        """docstring for na"""
        print 'test'

a = A()

print a.name
a.name = 'aaa'
print a.name
