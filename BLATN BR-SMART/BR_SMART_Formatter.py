import csv
import sys
import re
import datetime
import os

def read_file_lines(path):
	with open(path) as f:
		for line in f:
			yield line

def convert(txtpath, csvpath):
	fields = {	#Fields and matching regex to parse from TXT file
		'Date': 				r'Date:([0-9]*) ',
		'Time': 				r'Time:([0-9]*) ',
		'PM1.0 (ug-m^-3)': 		r'PM1\.0:([0-9]*) ',
		'PM2.5 (ug-m^-3)':		r'PM2\.5:([0-9]*) ',
		'PM10 (ug-m^-3)':		r'PM10:([0-9]*) ',
		'HCHO (mg-m^-3)':		r'HCHO:([0-9]*\.[0-9]*) ',
		'TVOC (mg-m^-3)':		r'TVOC:([0-9]*\.[0-9]*) ',
		'Dust > 0.3 (L^-1)':	r'>0\.3DustNum:([0-9]*)',
		'Dust > 0.5 (L^-1)':	r'>0\.5DustNum:([0-9]*)',
		'Dust > 1.0 (L^-1)':	r'>1\.0DustNum:([0-9]*)',
		'Dust > 2.5 (L^-1)':	r'>2\.5DustNum:([0-9]*)',
		'Dust > 5.0 (L^-1)':	r'>5.0DustNum:([0-9]*)',
		'Dust > 10 (L^-1)':		r'>10DustNum:([0-9]*)'
	}

	csv_fields = [	#Fields in the output CSV
		'Timestamp',
		'PM1.0 (ug-m^-3)',
		'PM2.5 (ug-m^-3)',
		'PM10 (ug-m^-3)',
		'HCHO (mg-m^-3)',
		'TVOC (mg-m^-3)',
		'Dust > 0.3 (L^-1)',
		'Dust > 0.5 (L^-1)',
		'Dust > 1.0 (L^-1)',
		'Dust > 2.5 (L^-1)',
		'Dust > 5.0 (L^-1)',
		'Dust > 10 (L^-1)'
	]

	if os.path.isfile(csvpath):
		print('Error: output file ' + csvpath + ' already exists')
		exit(-1)

	with open(csvpath, 'w', newline='') as csvf:
		csvw = csv.DictWriter(csvf, delimiter=',', fieldnames = csv_fields)

		csvw.writeheader()

		for line in read_file_lines(txtpath):
			parsed_fields = {}

			for (name, reg) in fields.items():
				parsed_fields[name] = re.findall(reg, line)[0]

			#print(parsed_fields)

			#Assemble the correct timestamp
			year = int(parsed_fields['Date'][0:4])
			month = int(parsed_fields['Date'][4:6])
			day = int(parsed_fields['Date'][6:8])

			hour = int(parsed_fields['Time'][0:2])
			minute = int(parsed_fields['Time'][2:4])

			dt = datetime.datetime(year, month, day, hour, minute)

			#Assemble the CSV row

			row = {}

			for csv_field in csv_fields:
				if csv_field in parsed_fields:
					row[csv_field] = float(parsed_fields[csv_field])
				else:
					pass 	#The requested field doesn't exist in the source TXT file, so it will need to be manually added below

			row['Timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S')

			print(row)

			csvw.writerow(row)
			
	return 0



if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Usage: BR_SMART_Formatter.py input_txt_file_path output_csv_file_path')
		exit(-1)
		
	exit(convert(sys.argv[1], sys.argv[2]))