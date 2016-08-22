import utest
import who1
import who2
import who3

from random import randint


def is_equal(x, y):
    return x == y


@utest.ok
def _okmain():
  "Adding another test case to main.py, is \"__main__\" == __name__"
  assert is_equal("__main__", __name__), "is name == main equality failure in main test"

if __name__ == "__main__":
    print "\nokmain"
