import csv
import datetime
import re
from peewee import *

db = SqliteDatabase('entries.db')

class Entry(Model):
	employee = CharField(max_length=255)
	date = DateTimeField(auto_now_add=True)
	time = IntegerField(default=0)
	notes = TextField()

	class Meta:
		database = db

if __name__ == '__main__':
	db.connect()
	db.create_tables([Entry], safe=True)

def print_csv(filter, minutes=0, keyword="", regex=""):
	with open('tasks.csv', newline='') as csvfile:
		task_reader = csv.reader(csvfile, delimiter=",")
		rows = list(task_reader)
		if filter == 'date':
			count = 1
			entries = []
			for row in rows:
				print(str(count) + ') ' + row[0] + ' - ' + row[1])
				entries.append([row[0], row[1], row[2], row[3]])
				count += 1
			entry = input("Choose an entry by number or press 'q' to quit: ")
			entry = int(entry) - 1
			print('Task Name: ' + entries[entry][1])
			print('Date Created: ' + entries[entry][0])
			print('Time Taken: ' + entries[entry][2])
			print('')
			print(entries[entry][3])

		elif filter == 'minutes':
			count = 1
			entries = []
			for row in rows:
				if row[2] == str(minutes):
					print(str(count) + ') ' + row[2] + 'min - ' + row[1])
					entries.append([row[0], row[1], row[2], row[3]])
					count += 1
			entry = input("Choose an entry by number or press 'q' to quit: ")
			entry = int(entry) - 1
			print('Task Name: ' + entries[entry][1])
			print('Date Created: ' + entries[entry][0])
			print('Time Taken: ' + entries[entry][2])
			print('')
			print(entries[entry][3])

		elif filter == 'keyword':
			count = 1
			entries = []
			for row in rows:
				note_list = row[3].split(" ")
				name_list = row[1].split(" ")
				if keyword in note_list or keyword in name_list:
					print(str(count) + ') ' + row[0] + ' ' + row[1] + ' ' + row[3])
					entries.append([row[0], row[1], row[2], row[3]])
					count += 1
			entry = input("Choose an entry by number or press 'q' to quit: ")
			entry = int(entry) - 1
			print('Task Name: ' + entries[entry][1])
			print('Date Created: ' + entries[entry][0])
			print('Time Taken: ' + entries[entry][2])
			print('')
			print(entries[entry][3])

		elif filter == 'pattern':
			count = 1
			entries = []
			for row in rows:
				name_results = re.match(r'' + regex + '', row[1])
				note_results = re.search(r'' + regex +'', row[3])
				if name_results != None or note_results != None:
					print(str(count) + ') ' + row[0] + ' ' + row[1] + ' ' + row[3])
					entries.append([row[0], row[1], row[2], row[3]])
					count += 1
			entry = input("Choose an entry by number or press 'q' to quit: ")
			entry = int(entry) - 1
			print('Task Name: ' + entries[entry][1])
			print('Date Created: ' + entries[entry][0])
			print('Time Taken: ' + entries[entry][2])
			print('')
			print(entries[entry][3])

def write_csv_header():
	with open('tasks.csv', 'a') as csvfile:
		fieldnames = ['date', 'name', 'minutes', 'notes']
		taskwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

		taskwriter.writeheader()

def write_csv(name, minutes, notes):
	with open('tasks.csv', 'a') as csvfile:
		fieldnames = ['date', 'name', 'minutes', 'notes']
		taskwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

		taskwriter.writerow({
			'date': datetime.datetime.now(),
			'name': name,
			'minutes': minutes,
			'notes': notes
		})

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
	task_name = input("Enter a task name: ")
	minutes_spent = input("Enter minutes spent on task: ")
	notes = input("Enter any additional notes about the task: ")
	while True:
		save = input("Would you like to save your entry, or start over? Y/n")
		if save == 'Y':
			write_csv(task_name, minutes_spent, notes)
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
		search_filter = input("Search for tasks by date(d), time spent on task(t), pattern(p), or keyword search(k): ")
		if search_filter not in ['d','t','p','k']:
			print("Not a valid selection")
		else:
			break

	if search_filter == 'd':
		print_csv('date')
	elif search_filter == 't':
		while True:
			minutes = input("enter minutes: ")
			try:
				int(minutes) 
			except:
				print("Please enter a valid number.")
			else:
				break
		print_csv('minutes', int(minutes), '', '')

	elif search_filter == 'p':
		reg_ex = input("Enter regular expression to search by: ")
		print_csv('pattern', 0, '', reg_ex)
	elif search_filter == 'k':
		keyword = input("Enter a word you'd like to search by: ")
		print_csv('keyword', 0, keyword, '')

work_log()