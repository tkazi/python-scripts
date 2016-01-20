# connects ot mysql to pull a report for a list of schools provided, and then sends an email to each school with the report

import mysql.connector
import csv

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


layer = 1
n = 1

mainConn = mysql.connector.connect(user='',
                               password='',
                               host='')

cursor = mainConn.cursor()

n = 10

while (n  <= 12):
    cursor.execute("""
                    Select
                        s.SchoolForce__School_Name__c
                        , s.nps_student_id__C
                        , s.SchoolForce__Student_First_Name__c
                        , s.SchoolForce__Student_Last_Name__c
                        , case when p.student_number is null then '     not' else p.student_number end ps_student_number
                        , case when p.first_name is null then '        in' else p.first_name end ps_first_name
                        , case when p.last_name is null then 'powerschool' else p.last_name end ps_last_name
                    from sf_ps_reconcile.sf_active_all_students s

                    left join (
                            select * from powerschool.students
                            where 1=1
                            and school_id = %s
                            and enroll_status = 0
                            ) p on p.student_number = s.nps_student_id__C

                    where 1=1
                    and ps_School_id__c = %s
                    and p.student_number is null

                    UNION 

                    -- left join for all ps records
                    Select  
                            s.SchoolForce__School_Name__c
                            , case when s.nps_student_id__C is null then '     not' else s.nps_student_id__C end s_student_number
                            , case when s.SchoolForce__Student_First_Name__c is null then '        in' else s.SchoolForce__Student_First_Name__c end s_first_name
                            , case when s.SchoolForce__Student_Last_Name__c is null then 'salesforce' else s.SchoolForce__Student_Last_Name__c end s_last_name
                            , p.student_number
                            , p.first_name
                            , p.last_name

                    from powerschool.students p

                    left join (
                            select * from sf_ps_reconcile.sf_active_all_students 
                            where 1=1
                            and ps_School_id__c = %s
                            ) s on p.student_number = s.nps_student_id__C
                            
                    where 1=1
                    and p.school_id = %s
                    and enroll_status = 0
                    and nps_student_id__c is null""" %(n, n, n, n) )

    ##rows = cursor.fetchall()
    result = []

    columns = tuple( [d[0].decode('utf8') for d in cursor.description] )

    for row in cursor:
        result.append(dict(zip(columns, row)))

    k = len(result)
    print "running school_id " + str(n)

    if k > 1:
        file_name =  str(result[0]['SchoolForce__School_Name__c'])
        school_name = str(result[0]['SchoolForce__School_Name__c'])
        fileLocation = 'exports/' + file_name + '.csv'
        f = open('exports/' + file_name + '.csv','w') 
        l = [str(item) for item in result[0]]
        f.write(','.join(l))
        f.write("\n")
        l = [[str(i) for i in item.values()] for item in result]
        for item in l:
          f.write(','.join(item))
          f.write("\n")
        f.close()
       
        
        #######email script
        emailfrom = ""
        recipients = ['']
        fileToSend = fileLocation
        username = ""
        password = ""

        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = school_name + "_errors_test_email"
        msg.preamble = "test email from automated data reconcile script"

        text = "Hello Siblings, test email with an attached csv file for " + school_name

        attachment_name = school_name + '.csv'
        part1 = MIMEText(text, 'plain')

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note:  handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=attachment_name)
        msg.attach(attachment)
        msg.attach(part1)


        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, recipients, msg.as_string())
        server.quit()
        
        n = n + 1
    else:
        n = n + 1

    
    




