import csv
import datetime
import re
from peewee import *

db = SqliteDatabase('entries.db')

class Entry(Model):
	employee = CharField(max_length=255, null=True)
	title = CharField(max_length=255, null=True)
	date = DateTimeField(null=True)
	time = IntegerField(default=0, null=True)
	notes = TextField(null=True)

	def __str__(self):
		return "{}: {} - {}".format(self.date, self.employee, self.title)

	class Meta:
		database = db

if __name__ == '__main__':
	db.connect()
	db.create_tables([Entry], safe=True)

def work_log():
	while True:
		user_input = input("Would you like to create a new entry(c), or look up old ones(L) c/L ? ")
		if user_input == 'c':
			create_new_task()
			break
		elif user_input == 'L':
			search_task()
			break
		else:
			print("That is not a valid response")

def create_new_task():
	employee = input("Enter employee name: ")
	task_name = input("Enter a task name: ")
	minutes_spent = input("Enter minutes spent on task: ")
	notes = input("Enter any additional notes about the task: ")

	while True:
		save = input("Would you like to save your entry, or start over? Y/n")
		if save == 'Y':
			Entry.create(employee=employee, title=task_name, 
								time=minutes_spent, notes=notes, date=datetime.datetime.now())
			while True:
				create_more = input("Would you like to add another entry? Y/n")
				if create_more == 'Y':
					create_new_task()
				else:
					break
			break
		else:
			create_new_task()

def search_task():
	while True:
		search_filter = input("Search for tasks by date(d), time spent on task(t), keyword search(k), or by employee(e): ")
		if search_filter not in ['d','t','e','k']:
			print("Not a valid selection")
		else:
			break

	if search_filter == 'd':
		search_database(filter='date')

	elif search_filter == 't':
		while True:
			minutes = input("enter minutes: ")
			try:
				int(minutes) 
			except:
				print("Please enter a valid number.")
			else:
				break
		search_database(filter='minutes', minutes=minutes)

	elif search_filter == 'e':
		employee = input("Enter employee name: ")
		search_database(filter='employee', employee=employee)

	elif search_filter == 'k':
		keyword = input("Enter a word you'd like to search by: ")
		search_database(filter='keyword', keyword=keyword)

def search_database(filter, minutes=0, keyword="", employee=""):
	if filter == 'date':
		entries = Entry.select().order_by('date')
		count = 1
		for entry in entries:
			print(str(count) + ") " + str(entry.date))
			count += 1

	elif filter == 'minutes':
		entries = Entry.select().where(Entry.time == minutes)
		count = 1
		for entry in entries:
			print(str(count) + ') ' + entry)
			count += 1

	elif filter == 'keyword':
		entries = Entry.select().where(Entry.title.contains(keyword) | Entry.notes.contains(keyword))
		count = 1
		for entry in entries:
			print(str(count) + ") " + entry)
			count += 1

	elif filter == 'employee':
		entries = Entry.select().where(Entry.employee == employee)
		count = 1
		for entry in entries:
			print(str(count) + ") " + entry)

# work_log()