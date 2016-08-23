import utest
import who1
import who2
import who3


def is_equal(x, y):
    return x == y


@utest.ok
def _okmain():
  "Adding another test case to main.py, is \"__main__\" == __name__"
  assert is_equal("__main__", __name__), "is name == main equality failure in main test"

@utest.ok
def _okwho2():
    #Testing who2.getAuthorReverse
    assert who2.getAuthorReverse()=="iruhD tekinA"



if __name__ == "__main__":
    print "\nokmain"

#Final Statistics of Pass and Failure case
utest.oks()