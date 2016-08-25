import unittest

from mock import patch

import worklog
import datetime

#assertEqual(x,y) -  assertNotEqual(x,y)
#assertGreater(x,y) - assertLess(x,y) - assertGreaterEqual(x,y) - assertLessEqual(x,y)
#assertIn(x, list)
#assertIsInstance(x, int)
#assertRaises(Exception)

class WorkLogTests(unittest.TestCase):
	def setUp(self):
		self.date1 = datetime.datetime.now()
		self.Entry1 = worklog.Entry.create(date=self.date1, employee="Tim", title="Do Laundry", notes="NA")

	@patch('__main__.worklog.create_new_task')
	def test_create_new_task_called(self, mock):
		worklog.work_log()
		self.assertTrue(mock.called)
		
if __name__ == '__main__':
	unittest.main()