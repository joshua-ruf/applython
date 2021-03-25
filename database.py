
import sqlite3
from datetime import datetime
import csv

class database:
	def __init__(self):
		"""
		Initialize the database and create table if necessary.		
		"""
		db = sqlite3.connect('applython.sqlite3')
		cursor = db.cursor()

		cursor.execute("""
			CREATE TABLE IF NOT EXISTS applications(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			company TEXT,
			position TEXT,
			date DATE,
			callback BOOL)
		""")
		db.commit()

		self.db = db
		self.cursor = cursor

	def insert(self, company, position, date, callback = 0):
		"""
		Add row to the applications table.

		:param company: string, name of the company
		:param position: string, name of the position
		:param date: string, '%Y-%m-%d' format, date of application
		:param callback: int, 0 or 1, whether a callback has been received
		"""
		query = """
			INSERT INTO applications(company, position, date, callback)
			VALUES (?, ?, ?, ?)
		"""
		values = (company, position, date, callback)

		self.cursor.execute(query, values)
		self.db.commit()

	def applied(self, company, position):
		"""
		Return whether this job has been applied for

		:param company: string, name of the company
		:param position: string, name of the position
		:param date: string, '%Y-%m-%d' format, date of application

		Returns (False, None) if the company-position has not been applied to, and 
		the (True, <date>) (of the most recent application) otherwise.
		"""
		query = """
			SELECT max(date) as date
			FROM applications
			where company = ? and position = ?
		"""
		values = (company, position)

		self.cursor.execute(query, values)
		row = self.cursor.fetchone()[0]
		if row is None:
			return False, None
		else:
			return True, row


	def update_callback(self, company, position, date, callback=1):
		"""
		Update an entry to reflect a new callback. In the unlikely event
		that there exist multiple applications to the same place for the
		same position on the same day, this function will only update the
		most rescent row (by id).

		:param company: string, name of the company
		:param position: string, name of the position
		:param date: string, '%Y-%m-%d' format, date of application
		:param callback: int, 0 or 1, whether a callback has been received
		"""
		query = """
			UPDATE applications
			set callback = ?
			from applications t0
			inner join (
				SELECT MAX(id) AS id
				FROM applications
				where company = ?
				and position = ?
				and date = ?
			) t1
			on t0.id = t1.id
		"""
		values = (callback, company, position, date)
		self.cursor.execute(query, values)
		self.db.commit()

	def list_applications(self, n=10, company=None, position=None, to_csv=False):
		"""
		Print the most recent applications to console.

		:param n: int, number of applications to print
		:param company: string, company name to limit search, defaults to None
			which does not filter by company
		:param position: string, position name to limit search, defaults to None
			which does not filter by position
		:param to_csv: bool, whether to save save results to filename.csv, defaults
			to False which prints results to console
		"""
		query = f"""
			SELECT *
			FROM applications
			WHERE company {'IS NOT' if company is None else '='} ?
				and position {'IS NOT' if position is None else '='} ?
			ORDER BY date DESC
			limit ?
		"""

		values=(
			'NULL' if company is None else company,
			'NULL' if position is None else position,
			n
		)
		self.cursor.execute(query, values)

		rows = [r for r in self.cursor.fetchall()]
		print('Applications found:', len(rows))
		if len(rows) > 0:
			if to_csv:
				now = datetime.today().strftime('%Y%m%d%H%M%S')
				csv_file = now + 'applythonExport.csv'
				with open(csv_file, mode='w') as file:
					writer = csv.writer(file, delimiter=',', quotechar='"')
					writer.writerow(['id', 'company', 'position', 'date', 'callback'])
					for r in rows:
						writer.writerow(r)

				print('saved to', csv_file)
			else:
				for r in rows:
					print(r)

	def callback_rate(self):
		"""
		Print the callback rate to console.
		"""
		query = """
			SELECT AVG(callback)
			FROM applications
		"""
		self.cursor.execute(query)
		rate = self.cursor.fetchone()[0]
		print('Callback Rate:', rate)

if __name__ == '__main__':

	### testing
	DB = database()
	print('database connected')
	# DB.insert('company test', 'position test', '2021-03-18')
	# print('row inserted')
	# DB.list_applications(100, company='Byg Data', position='yes')
	# print('showed applications')

	DB.list_applications(100, to_csv=True)
	print('showed applications')



	# DB.callback_rate()
	# print('showed callback rate')
	# DB.update_callback('company test', 'position test', '2021-03-18')
	# print('updated callback')
	# DB.list_applications(100)
	# print('showed applications (again)')

	# print('have I applied?')
	# print(DB.applied('Byg Data', 'Data Shaman'))

	DB.db.close()