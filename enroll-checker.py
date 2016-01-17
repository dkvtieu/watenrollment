from lxml import html, etree
import time
import urllib2


###USER INPUT###
term = raw_input('Term? (e.g. 1161 is Winter 2016) ')
subject = raw_input('Subject? (e.g. MATH) ')
catalog = raw_input('Course Number? (e.g. 240) ')
section_type = raw_input('Are you looking for a LEC or TUT? (e.g. LEC) ')
section_number = raw_input('Section? (e.g. 001) ')
section_number = int(section_number)
refresh_rate = raw_input('Refresh Rate? ')
refresh_rate = int(refresh_rate)

#column index for table of information
comp_sec = 2
enrl_cap = 6
enrl_tot = 7


#queries the url and feeds it to the lxml parser for further use
def get_page():
	url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=%s&subject=%s&cournum=%s' % (term, subject.upper(), catalog)
	request = urllib2.Request(url)
	page = urllib2.urlopen(request)
	html_parser = etree.HTMLParser()
	tree = etree.parse(page, html_parser)
	return tree

#gets all the text elements for the row in question
def get_row_info(row_index):
	display_row = get_page().xpath('//table[@border="2"]//table/tr[%d]//td/text()' % row_index)
	return display_row

#creates a list of lists where each element is a valid row (with its text elements) in the data table
def row_list():
	list = []
	number_of_rows = get_page().xpath('//table[@border="2"]//table/tr')
	for i in range(2, len(number_of_rows)): #begins at 2 so that it disregards the first two useless rows
		list.append(get_row_info(i))
	return list

#loop for finding correct row to parse 
def find_row():
	row_list_info = row_list()
	for row in row_list_info:
		section = row[1]
		if section[:3] == section_type.upper() and int(section[4:7]) == int(section_number):
			break
	return row

def main():
	while True:
		correct_row = find_row()
		enrollment_capacity = int(correct_row[enrl_cap])
		enrollment_total = int(correct_row[enrl_tot])
		if enrollment_total >= enrollment_capacity: 
			print 'All %d seats are unavailable for %s %03d of %s %s' % (enrollment_capacity, section_type.upper(), section_number, subject.upper(), catalog)
			time.sleep(refresh_rate)
		else:
			seats_available = enrollment_capacity - enrollment_total
			print "There are now %d seat(s) available for %s %03d of %s %s" % (seats_available, section_type.upper(), section_number, subject.upper(), catalog)
			time.sleep(15) #makes sure the message stays visible to the user for a brief period of time 
			break

if __name__ == "__main__":
	# execute only if run as a script
	main()