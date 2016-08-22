import utest
__author__ = "ian drosos"
# python 2

print "\nin " + __name__ + " by " + __author__


def is_equal(x, y):
    return x == y

    
@utest.ok
def _okwho1():
  "Adding another test case to who1.py, is \"__main__\" == __name__"
  assert is_equal("__main__", __name__), "is name == main equality failure in who1 test"
