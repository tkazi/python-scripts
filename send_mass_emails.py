## feed in lsit of emails, and the script will send an email to the users one after another


#!/usr/bin/env python

import smtplib
import mimetypes
from premailer import transform
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import csv
import time
import os, sys
import datetime




with open('/Users/tkazi/Dropbox/python/educator_emails/scripts/send_email/email_test.csv', 'rU') as f:
	s = csv.reader(f)
	recipients = list(s)


emailfrom = formataddr((str(Header('Code4Schools', 'utf-8')), "info@codeforschools.com")) 
user = ""
password = ""
server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(user,password)

errors = []
success = []

emails_sent = []

n = 1

for receiver in recipients:
	if n < 41:
		print receiver
		print n, receiver[0]
		try:
			# recipients = ['taha698@gmail.commm']
			emailto = str(receiver[0])
			msg = MIMEMultipart()


			html =  transform("""
			<html>
			<head>
			<style>
				body,
				html {
				  margin: 0;
				  padding: 0;
				  height: 100%;
				} 

				.bodyWrapper {
				  background: #eee ;
				  padding:40px 0 25px;
				}

				.imageContainer{
					margin:0 auto;
					text-align:center;
					background: #51676C; 
					width:610px;
					border-radius:5px 5px 0 0;
				}

				.contentWrapper {
				  text-align: center;
				}

				.contentWrapper .logoImage {
				  margin: 10px auto 0;
				  max-width: 55%;
				}

				.innerWrapper {
				  width: 610px;
				  background: white;
				  border-radius: 5px;
				  margin: 0px auto 20px;
				  padding-bottom: 40px;
				  box-shadow: 0 0 2px rgba(0, 0, 0, 0.25);
				}

				.content {
				}

				.innerWrapper .topContent{
				  background:white;
				  padding: 30px 40px 20px;
				}

				.innerWrapper .content .bottomContent{
				  background:white;
				  text-align:center;
				  padding: 30px 30px 20px;
				}

				.innerWrapper .topContent p {
				  margin:0;
				  text-align: justify;
				}

				.innerWrapper .projects {
				  margin:0 auto;
				  border-radius:4px;
				  background:white;
				  text-align:center;
				}

				.innerWrapper .projects p {
				  font-weight:bold;
				  text-align:center;
				  margin-top:0;
				}

				.innerWrapper .projectDetail {
				  width:225px;
				  height:150px;
				  display: inline-block;
				  margin: 10px;
				  text-align:center;
				  padding: 10px 0;
				  border:1px solid #E4E4E4;
				  border-radius:4px;
				  vertical-align:top;
				}

				.projectDetail img {
				  width:191.25px;
				  height: 122px;
				}


				.innerWrapper h4 {
				  padding: 15px 10px;
				  margin: 0;
				  border-bottom: 1px solid #eee;
				  color: #4D5466;
				  font-family: Helvetica,Arial,sans-serif;
				  font-size: 14px;
				}

				.innerWrapper p,
				
				ul {
				  color: #4D5466;
				  font-family: Helvetica,Arial,sans-serif;
				  font-size: 14px;
				  line-height: 22px;
				  padding: 0 25px;
				  list-style: none;
				}

				.innerWrapper ul {
				  font-weight: bold;
				}

				.innerWrapper li {
				  font-weight: normal;
				  margin-top: 2.5px;
				  margin-left: 0px;
				}

				.signature {
				  padding-top:15px;
				}

				.signature p {
				  margin: 0;
				}

				.projects .projectDetail .projectDetailsp {
				  margin: 6.5px 0 0;
				  font-size:1em;
				  padding:0;
				  text-align:center;
				  font-weight:normal;
				}

			</style>
			</head>

			<body>
				<div class="bodyWrapper">
					<div class="contentWrapper">
					  <div class="imageContainer">
					  	<img class="logoImage" src="https://s3.amazonaws.com/code4schools/tittle.png">
					  </div>
					  <div class="innerWrapper">
					    <h4>We work around your budget!</h4>
					    <div class="content"> 
					      <div class="topContent">
					        <p>We are web developers and data analysts with a passion for solving problems in education. We work around your budget, providing affordable rates with an emphasis on high quality work, and a firm dedication to improving learning outcomes for students everywhere.</p>
					      </div>
					       
					      <div class="projects">         
					        <div class="projectDetail">
					          <img  src="https://s3.amazonaws.com/code4schools/validation.png"/>
					          <p class='projectDetailsp'>SIS Data Validation</p>
					        </div> 
					        <div class="projectDetail">
					          <img src="https://s3.amazonaws.com/code4schools/geocode.jpg"/>
					          <p class='projectDetailsp'>Geocoding / School Zoning</p>
					        </div>
					        <div class="projectDetail">
					          <img src="https://s3.amazonaws.com/code4schools/email.png"/>
					          <p class='projectDetailsp'>Email Automation</p>
					        </div>
					        <div class="projectDetail">
					          <img src="https://s3.amazonaws.com/code4schools/enrollmentform.png"/>
					          <p class='projectDetailsp'>Online Application Forms</p>
					        </div>
					        <div class="projectDetail">
					          <img src="https://s3.amazonaws.com/code4schools/dashboard.png"/> 
					          <p class='projectDetailsp'>SIS Dashboards</p>
					        </div>
					        <div class="projectDetail">
					          <img src="https://s3.amazonaws.com/code4schools/multiply.png"/>
					          <p class='projectDetailsp'>Subject Content Games</p>
					        </div>
					      </div> 
					      
					      <div class="bottomContent">
					        <p class="lastP">Please reach out to us for your free technical consultation or with any questions.</p>
					        <p>We look forward to working with you!</p>
					        <div class="signature">
					          <p>Code4Schools</p>
					          <p>San Francisco, CA</p> 
					        </div>
					      </div>
					    </div> 
					  </div>
					  <br>  
					  <a href="https://twitter.com/code4schools" target="_blank">
					    <img class="twitter" src="https://s3.amazonaws.com/code4schools/Follow+me.png" width="48" />
					  </a> 
					</div>
					</div>
			</body> 
			</html>

		""")
			

			html = MIMEText(html, 'html')

			msg["From"] = emailfrom
			msg["To"] = emailto
			# msg["To"] = ", ".join(recipients)
			msg["Subject"] = "Technology and Data Services for Schools"
			msg.attach(html)


			send = server.sendmail(emailfrom, emailto, msg.as_string())
			success.append(send)

			emails_sent.append(receiver[0])

		except Exception as e:
			errors.append(e)
			pass

		print "--"*25, "sent:", len(success), "--", "errors:", len(errors)

		n = n + 1

now = str(datetime.datetime.now()).replace(" ","")
output = csv.writer(open('/Users/tkazi/Dropbox/python/educator_emails/scripts/send_email/sent_emails/sent_'+now+'.csv', 'wb'))
for row in emails_sent:
	output.writerow([row])

os.renames("/Users/tkazi/Dropbox/python/educator_emails/scripts/send_email/email_test.csv","/Users/tkazi/Dropbox/python/educator_emails/scripts/send_email/email_test_archive.csv")
remaining = []
for row in recipients:
	if row[0] not in emails_sent:
		remaining.append(row)

output = csv.writer(open('/Users/tkazi/Dropbox/python/educator_emails/scripts/send_email/email_test.csv', 'wb'))
for row in remaining:
	output.writerow(row)









