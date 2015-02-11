# this works for getting the following operations to happen without ascii errors, etc:
# nltk themselves now recommend you use beautifulSoup's get_text()
# 
from bs4 import BeautifulSoup



soup = BeautifulSoup('your_html_file.html')
text = soup.get_text()
j = open('output.txt','w')
text = text.encode('ascii', 'ignore').decode('ascii')
j.write(text)
j.close()

# text is now saved like regular text in that file, ready for nltk and nlp stuff



'''
OK, new idea about how data flows
tuned-resonator is the subnet stuff.
local Curriculum is one barnacle on the subnet
rf-immanence is another barnacle on the subnet
...should they be subsets of the tuned-resonator repo?





'''