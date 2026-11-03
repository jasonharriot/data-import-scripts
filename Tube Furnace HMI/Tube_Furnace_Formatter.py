import csv
import sys
import re
import datetime
import os
import codecs

def convert(csv_in_path, csv_out_path):
	if os.path.isfile(csv_out_path):
		print('Error: output file already exists: ' + csv_out_path)
		exit(-1)

	field_map = {
		'MCGS_TIME': 'Date base',
		'MCGS_TIMEMS': 'Milliseconds',
		'左炉膛温度': 'Temperature left (°C)',
		'左炉膛设定值': 'Temperature setpoint left (°C)',
		'中炉膛温度': 'Temperature center (°C)',
		'中炉膛设定值': 'Temperature setpoint center (°C)',
		'右炉膛温度': 'Temperature right (°C)',
		'右炉膛设定值': 'Temperature setpoint right (°C)',
		'搅拌速度': 'Rotation rate (rpm)',
		'H2流量': 'Reaction gas flow rate (slm)',
		'H2设定值': 'Reaction gas flow rate setpoint (slm)',
		'N2流量': 'Neutral gas flow rate (slm)',
		'N2设定值': 'Neutral gas flow rate setpoint (slm)',
		'H2累积流量': 'Reaction gas volume (L)',
		'N2累积流量': 'Neutral gas volume (L)',
	}

	fields_out = [
		'Timestamp',
		'Timestamp millis',
		'Temperature left (°C)',
		'Temperature setpoint left (°C)',
		'Temperature center (°C)',
		'Temperature setpoint center (°C)',
		'Temperature right (°C)',
		'Temperature setpoint right (°C)',
		'Rotation rate (rpm)',
		'Reaction gas flow rate (slm)',
		'Reaction gas flow rate setpoint (slm)',
		'Neutral gas flow rate (slm)',
		'Neutral gas flow rate setpoint (slm)',
		'Reaction gas volume (L)',
		'Neutral gas volume (L)',
	]

	#csv_in_f = open(csv_in_path, 'r')
	csv_in_f = codecs.open(csv_in_path, 'r', 'gb18030')	#gb18030 appears to be the CSV format used by the MCGS HMI.
	csv_out_f = open(csv_out_path, 'w', newline='')

	#csv_r = csv.reader(csv_in_f, delimiter=',')
	csv_r = csv.DictReader(csv_in_f, delimiter=',')

	csv_w = csv.DictWriter(csv_out_f, delimiter=',', fieldnames = fields_out)

	csv_w.writeheader()

	for line in csv_r:
		#print(line)

		parsed = {}

		for (field_in, field_out) in field_map.items():
			parsed[field_out] = line[field_in]

		#Assemble the correct timestamp

		date_base = datetime.datetime.strptime(parsed['Date base'], '%Y/%m/%d %H:%M:%S')

		date_millis = datetime.timedelta(milliseconds=int(parsed['Milliseconds']))

		date_full = date_base + date_millis

		#Assemble the CSV output row
		row_out = {}

		for field_out in fields_out:
			if field_out in parsed:	#If an output field is just a direct copy of the input field
				row_out[field_out] = parsed[field_out]

		row_out['Timestamp'] = date_full.strftime('%Y-%m-%d %H:%M:%S')	#Use a format that plays nice with Excel.

		row_out['Timestamp millis'] = date_full.timestamp() * 1000 #Linux epoch millis

		#print(row_out)

		csv_w.writerow(row_out)
			
	return 0



if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Usage: Tube_Furnace_Formatter.py input_csv_file_path output_csv_file_path')
		exit(-1)
		
	exit(convert(sys.argv[1], sys.argv[2]))