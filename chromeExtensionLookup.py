import os
import urllib2
import re

username = raw_input("Enter the username: ") #use this is you want to run it locally on your computer
# computer_name = raw_input("Enter UNC path: ")

ext = os.listdir("C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data\\Default\Extensions" % (username))
url = 'https://chrome.google.com/webstore/detail/'

print ("Enumerating Chrome Extensions for %s" % (username))
print "\n"
for name in ext:
	try:
		name = str(name)
		if name == "pkedcjkdefgpdelpbcmbmeomcjbeemfm": #Don't see this one in the extension store, so have to hard code it
			print ("%s is ['Chrommecast']" % (name))
		else:
			response = urllib2.urlopen(url+name)
			html = response.read()
			title = re.findall(r'(?<=og:title" content=")([\S\s]*?)(?=">)', str(html))
			print ("%s is %s " % (name, title))
	except:
		print ("%s Cannot seem to find this one..." % (name))
		pass
		
