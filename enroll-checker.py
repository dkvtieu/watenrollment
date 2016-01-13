from lxml import html, etree
import time
import urllib2
import smtplib
import winsound


subject = raw_input('Subject? ')
course_number = raw_input('Course Number? ')
section_input = raw_input('Section? ')
section_number = int(section_input) + 1
ask_email = raw_input('Would you like to recieve email notifications when a spot opens up? [y/n] ')


if ask_email is 'y':
	your_email = raw_input('Please provide an email for notification ')	
else:
	True
refresh_rate = raw_input('Refresh Rate? ')
refresh_rate = int(refresh_rate)


"""
# EMAIL HANDLING #

msg='hello'
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login("EMAIL", "PASS")
server.sendmail('from_email', 'your_email', msg)
server.quit()
"""

exit = True

while exit:
	url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1161&subject=%s&cournum=%s' % (subject.upper(), course_number.upper())
	request = urllib2.Request(url)
	page = urllib2.urlopen(request)

	html_parser = etree.HTMLParser()
	tree = etree.parse(page, html_parser)

	enrollment_capacity = tree.xpath('//table[@border="2"]//table/tr[%s]/td[7]/text()' % section_number)
	enrollment_total = tree.xpath('//table[@border="2"]//table/tr[%s]/td[8]/text()' % section_number)

	enrollment_capacity = int(seats_taken[0])
	enrollment_total = int(seats_total[0])

	if enrollment_total > enrollment_capacity: 
		print 'All %s seats are unavailable for Section %s of %s %s' % (seats_total, int(section_input), subject.upper(), course_number)
	else:
		print "SEATS ARE AVAILABLE"
		seats_available = seats_total - seats_taken
		# msg = "There are now %s seats available for Section %s of %s %s" % (seats_available, int(section_input), subject, course_number)
		while True:
			winsound.Beep(500,500)
		exit = False

	time.sleep(refresh_rate)



