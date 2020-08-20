# The aim of the below script is to find and download the summary of product characteristics (chpl - 'charakterystyka produktu leczniczego') 
# for any drug available in the Polish market. The documents are downloaded from a government-sponsored site pub.rejestrymedyczne.csioz.gov.pl

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import bs4, requests, os
from datetime import datetime
starttime = datetime.now()

try:
	os.unlink('chpl.pdf')
except:
	pass

drug_name = input('Please provide the trade name of the drug ')
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)

browser.get('https://pub.rejestrymedyczne.csioz.gov.pl/')

browser.find_element_by_id('NazwaTXTSearch').send_keys(drug_name)
browser.find_element_by_id('btnSearch').click()

while True:
	try:
		browser.find_element_by_id('GridView1_ToDetailsLink_0').click()
		break
	except:
		pass
		
all_tabs = browser.window_handles
while len(all_tabs) < 2:
	all_tabs = browser.window_handles

while True:
	try:
		browser.switch_to.window(all_tabs[1])
		elem = browser.find_element_by_partial_link_text('charakterystyki')
		if browser.current_url != 'about:blank':
			break
	except:
		pass
			
link = elem.get_attribute('href')
myfile = requests.get(link, allow_redirects = True)
file = open('chpl.pdf','wb')
for chunk in myfile.iter_content(100000):
	file.write(chunk)
file.close()
os.startfile('chpl.pdf')
print('The script took ' + str(datetime.now() - starttime) + ' to execute')




