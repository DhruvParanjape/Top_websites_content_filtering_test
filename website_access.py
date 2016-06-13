from requests import get
from lxml.html import fromstring
from datetime import datetime
from requests.exceptions import ConnectionError

website_list = "websites.txt"
filename = "results.txt"
cert_path = "SQTerminator.der"
results = open(filename,'w')

#Start calculating program running time
start_time = datetime.now().replace(microsecond=0)

#setup counters
website_counter = 0
blocked_counter = 0
not_blocked_counter = 0

#Header block
results.write("WEBSITE NAME\t\tSTATUS\t\tBLOCKED SITE\t\tCATEGORY\n")


for website in open(website_list,'r'):
    website = website.rstrip("\n").rstrip("\r")
    if website == '':
	continue

    name = "http://"+website
    try :    
	webpage = get(name) # verify verify works else use cert=
    	#webpage = get(name, verify = cert_path)
    	#webpage = get(name, cert = cert_path)
    	site_map = fromstring(webpage.content)
    	website_counter = website_counter+1
    
    	try:
        	#Sites blocked
        	result = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/h1/label//text()')[0]
        	site = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()[1]')[0].replace(": ","",1)
        	category = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()')[1].replace(": ","",1)
        	blocked_counter=blocked_counter + 1
    
    	except IndexError as e:
        	#Oops sites not blocked
        	result = "not blocked"
        	site = ""
        	category = ""
        	not_blocked_counter = not_blocked_counter + 1

    except ConnectionError :
	#Oops sites not blocked
        result = "not blocked"
        site = ""
        category = ""
        not_blocked_counter = not_blocked_counter + 1

    #Dumping into the file to have a report at the end
    results.write(website+"\t"+result+"\t"+site+"\t"+category+"\n")

results.close()

end_time = datetime.now().replace(microsecond=0)

duration = end_time - start_time
print "\n\t\t--Statistics--\n"
print "Total running time :\t\t", duration
print "Total websites accessed :\t", website_counter
print "Total websites blocked :\t", blocked_counter
print "Total websites not blocked :\t", not_blocked_counter