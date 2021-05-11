import flask06
# Test File for group_2_many_guys

def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print ('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))

#Test Cases

def main():
    check_Sorting_Buttons = True

    if check_Sorting_Buttons:
        print("Testing Sorting Buttons...")

        

