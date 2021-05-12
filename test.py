import unittest
import requests

class FlaskTest(unittest.TestCase):

    def test_login(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h1>Welcome to Group 2 Many Guys\' UNCC Events App</h1>' in response.text, True)

    def test_events(self):
        response = requests.get("http://127.0.0.1:5000/events")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        print(response.text)
        self.assertEqual('<title>UNCC Events App - View your Events</title>' in response.text, True)

    # def test_note(self):
    #     response = requests.get("http://127.0.0.1:5000/notes/1")
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 200)
    #     self.assertEqual('First Note' in response.text, True)

    # def test_new(self):
    #     response = requests.get("http://127.0.0.1:5000/notes/new")
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 200)
    #     self.assertEqual('<form action="new" method="post">' in response.text, True)

    # def test_delete(self):
    #     response = requests.get('http://127.0.0.1:5000/notes/delete')
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 500)

    # print("test")
    # def test_sorting(self):
    #     response = requests.get("http://127.0.0.1:5000/events")
    #     print("Sorting Test")
    #     # session['user']="Jonathan"
    #     get_events()
    #     print("Testing Sorting Buttons...")

# Test File for group_2_many_guys

'''
def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print ('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))
'''

if __name__ == "__main__":
    unittest.main()