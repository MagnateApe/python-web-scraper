'''
Created on May 19, 2020

@author: Jack

- Uses Beautiful Soup and Requests libraries for html reception
- Uses sys for UTF-8 encoding
- Uses urlib and re for regex searching/parsing

WHAT IT DOES:
- Receives user input keywords as searches
- Uses those keywords to conduct a google search
- Parses google searches, returning all relevant websites
- Uses html parsers and UTF-8 encoding to make html vieweable
- Parses those websites for email addresses 
- sends customized emails to those recipients
- parses email addresses sifting out obvious bad emails.
'''
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlsplit
import requests
import sys
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

#-----------------------UTF-8 encoding handling------------------------------
sys.stdout.encoding
u"Stöcker".encode(sys.stdout.encoding, errors='replace')
u"Стоескер".encode(sys.stdout.encoding, errors='replace')

            
#-----------------------Google Searches Initialization--------------------------------------
#add as many google searches as you want (separate by '+' not space ' ').
keyword_count  = input("How many keywords/phrases do you have?\n")

searches = []

for i in range (0, int(keyword_count)):
    search = input("Enter keyword/phrase " + str(i + 1) + ". In the case of a phrase, seperate with a '+'. Ex: super+cool+stuff\n")
    searches.append(search)

print("Keywords and phrases added.\n")

iterations = input("How many search iterations? Enter a number 1-100.\n")

start = input("Which result do you want to start at? Type 1 for default. Otherwise enter any reasonable integer.\n")

all_emails = set()  

#-----------------------Parsing Google Results-----------------------------------------

def assemble_library(search):
    
    #set up an agent so google doesn't freak out.
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    #the google search url
    URL = 'https://google.com/search?q={}&num={}&start={}'.format(search, iterations, start)

    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)

    #check to make sure the site actually gave us something.
    if resp.status_code == 200:  
        raw = BeautifulSoup(resp.content, "lxml")

    #parse the google search page. Collect all the websites URL's.
    results = []
    for x in raw.find_all('div', class_='r'):
        anchor = x.find_all('a')
        if anchor:
            link = anchor[0]['href']
            item = link
            results.append(item)
    #for x in range(len(results)): 
        #print(results[x])
    
    inspect_websites(results)
    
def inspect_websites(sites):
    for i in range (0, len(sites)):
        URL = sites[i]
        print(URL)
        fetch_html(URL)

def fetch_html(URL):
    #get the website URL from the list
    resp = None
    restrict = False;
    
    try:
        #print('yyy')
        resp = requests.get(URL, timeout=5.0)
        #print('ccc')
        
    except requests.exceptions.Timeout:
        restrict = True;
        print('e')
        # Maybe set up for a retry, or continue in a retry loop
    except requests.exceptions.TooManyRedirects:
        restrict = True;
        print('e')
        # Tell the user their URL was bad and try a different one
    except requests.exceptions.RequestException:
        restrict = True;
        print('e')
        

    if (restrict == False):
        #print('here')
        resp = requests.get(URL)
        grab_emails(resp)
          
    
        
def grab_emails(html):
    #make sure we get something
    if html != None and html.status_code == 200:
        #print('here')
        #parse for emails (regex)
        emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", 
                                    html.text))
         
    
        all_emails.update(emails)
        
        #print('herr')

def send_emails(email):
    
    if (email_check(email)):
        return 0;
    

    # email object that has multiple part:
    msg = MIMEMultipart()
    msg['Subject'] = 'Brāv Conflict Management'
    msg['To'] = email


    with open('/Users/Jack/Desktop/img1.png', 'rb') as f:
        # set attachment mime and file name, the image type is png
        mime = MIMEBase('image', 'png', filename='img1.png')
        # add required header data:
        mime.add_header('Content-Disposition', 'attachment', filename='img1.png')
        mime.add_header('X-Attachment-Id', '0')
        mime.add_header('Content-ID', '<0>')
        # read attachment file content into the MIMEBase object
        mime.set_payload(f.read())
        # add MIMEBase object to MIMEMultipart object
        encoders.encode_base64(mime)
        msg.attach(mime)

    msg.attach(MIMEText('<html><body><h2><center></center></h2>' +
    '<p><center><img src="cid:0"></center></p>' +
    """<p><h3><center> Brāv is an online platform to manage conflicts. (www.brav.org). In addition, 
    anyone can train in conflict management and they in turn manage the conflicts of others, directly on the site. </center><h3><p>""" +
  
    """<p><h3><center> If a term is violated, we hash out issues as well directly on the site. There, we use diverse 
    functionalities, including emasks for users to cover their faces in case they are too shy to show 
    to those they are in conflict. </center><h3><p>"""  + 
    
    """<p><center> 
    <br>Please check out our E-training! Here is our instructional video: (CLE/ CME).
                    <br><a href="https://www.youtube.com/watch?v=emIz-fkxm4c">https://www.youtube.com/watch?v=emIz-fkxm4c</a>
                    
    <br>Last, please view, like, subscribe, comment and share our video with your audience:</center><p>""" +
    
    """<p><h3><center>Brochures: 
                   <br><a href="https://files2.mixmaxusercontent.com/RH7KMP8Dv8mWhFDM5/f/5bMTAKjrbH4cikvR8/?messageId=7u2F9mF9ktOq9lAeG&rn=gI2FIxyJkI&re=ISbvNmLslWYtdGQu9Wa0FWakVWbu9Wa0Fmcl5WZnRHel5mI">https://files2.mixmaxusercontent.com/RH7KMP8Dv8mWhFDM5/f/5bMTAKjrbH4cikvR8/?messageId=7u2F9mF9ktOq9lAeG&rn=gI2FIxyJkI&re=ISbvNmLslWYtdGQu9Wa0FWakVWbu9Wa0Fmcl5WZnRHel5mI</a>
                    <br><a href="https://files4.mixmaxusercontent.com/RH7KMP8Dv8mWhFDM5/f/VgSIfvcECAi0drEvk/?messageId=7u2F9mF9ktOq9lAeG&rn=gI2FIxyJkI&re=ISbvNmLslWYtdGQu9Wa0FWakVWbu9Wa0Fmcl5WZnRHel5mI">https://files4.mixmaxusercontent.com/RH7KMP8Dv8mWhFDM5/f/VgSIfvcECAi0drEvk/?messageId=7u2F9mF9ktOq9lAeG&rn=gI2FIxyJkI&re=ISbvNmLslWYtdGQu9Wa0FWakVWbu9Wa0Fmcl5WZnRHel5mI</a>
                    <br><p><h3><center>""" + 
    """<p><h3><center>Thank you!<p><h3><center>""" + 
    '</body></html>', 'html', 'utf-8'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
      
    server.starttls()
             
    server.login('brav.blast@gmail.com', 'Mediation98')
       
    server.sendmail('brav.blast@gmail.com', '{}'.format(email), msg.as_string())

#     server.login('********', '******')
#       
#     server.sendmail('********, '{}'.format(email), msg.as_string())

def email_check(email):
    # checks to see if an email is proper, and records instances of each for efficiency
    # purposes.
    # Currently parsing out anything with the following:
    # 'example'
    # more than 5 numbers in the address
    # 'no-reply'
    # 'info'
    
    e = "example";
    r = "no-reply";
    i = "info";
    
    if((e in email) or (r in email) or (i in email)):
        return True;
    
    total_numbers = re.findall('[0-9]', email)
    
    if (len(total_numbers) > 5):
        return True;
    
    return False;


#--------Main---------

#Call assemble_library which will ultimately server to
#fetch all the relevant email adresses
for i in range (0, len(searches)):
    assemble_library(searches[i])

#print our emails to see what we got
print(all_emails)

#send emails to those in the list from a gmail server
for value in all_emails:
    send_emails(value)
#send_emails('123456@gmail.com')