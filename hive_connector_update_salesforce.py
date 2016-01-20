
## connects to hive to pull a summary dashboard and then connects to salesforce to update the mapped records/accounts


import csv
import SQLForce
import pyhs2
import sys
import smtplib
import mimetypes
import datetime
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



now = datetime.datetime.now() 

file_name = "district_data_from_hive_" + str(now.month) + "-" + str(now.day) + "-" + str(now.year)
print file_name

fields = []
results = []

with pyhs2.connect(host='',
               port=10000,
               authMechanism="",
               user='',
               password='') as conn:

	with conn.cursor() as cur:
	    #Show databases
	    #print cur.getDatabases()

		print "running hive jobs...."
	#Execute query
		cur.execute(""" 
			select 
	 concat(if(isnull(account_id),'',account_id),',',if(isnull(as_of_date__c),'',as_of_date__c),',',if(isnull(district_id_text__c),'',district_id_text__c),',',if(isnull(name),'',name),',',
			if(isnull(billingstate),'',billingstate),',',if(isnull(district_subdomain__c),'',district_subdomain__c),',',
			if(isnull(subdomain_requestor__c),'',subdomain_requestor__c),',',if(isnull(ip_forwarding__c),'',ip_forwarding__c),',',
			if(isnull(total_active_schools__c),'',total_active_schools__c),',',if(isnull(verified_teachers__c),'',verified_teachers__c),',',
			if(isnull(verified_registered_students__c),'',verified_registered_students__c),',',if(isnull(total_registered_teachers__c),'',total_registered_teachers__c),',',
			if(isnull(total_registered_students__c),'',total_registered_students__c),',',if(isnull(x7d_teacher_actives__c),'',x7d_teacher_actives__c),',',
			if(isnull(x7d_student_actives__c),'',x7d_student_actives__c),',',if(isnull(x28d_activ__c),'',x28d_activ__c),',',
			if(isnull(x28d_student_actives__c),'',x28d_student_actives__c),',',if(isnull(total_registered_parents__c),'',total_registered_parents__c),',',
			if(isnull(subdomain_creation_date__c),'',subdomain_creation_date__c),',',if(isnull(cumulative_snapshot_teachers__c),'',cumulative_snapshot_teachers__c),',',
			if(isnull(cumulative_snapshots_assigned__c),'',cumulative_snapshots_assigned__c),',',if(isnull(cumulative_snapshot_students__c),'',cumulative_snapshot_students__c),',',
			if(isnull(cumulative_snapshots_taken__c),'',cumulative_snapshots_taken__c),',',if(isnull(edmodo_tipped_school__c),'',edmodo_tipped_school__c),',',
			if(isnull(total_edmodo_tipped_schools__c),'',total_edmodo_tipped_schools__c),',',if(isnull(sales_tipped_school__c),'',sales_tipped_school__c),',',
			if(isnull(total_sales_tipped_schools__c),'',total_sales_tipped_schools__c),',',if(isnull(purchased_sfs__c),'',purchased_sfs__c),',',
			if(isnull(earliest_expiration__c),'',earliest_expiration__c) )
    
    
 from ( 
    
    
    select ad.*
	, case when to_date(subdomain_Creation_date) is null then '' else to_date(subdomain_Creation_date) end as Subdomain_Creation_Date__c
	, case when cumulative_snapshot_teachers is null then 0 else cumulative_snapshot_teachers end as Cumulative_Snapshot_Teachers__c
	, case when cumulative_snapshots_assigned is null then 0 else cumulative_snapshots_assigned end as Cumulative_Snapshots_Assigned__c
	, case when cumulative_snapshot_students is null then 0 else cumulative_snapshot_students end as Cumulative_Snapshot_Students__c
	, case when cumulative_snapshots_taken is null then 0 else cumulative_snapshots_taken end as Cumulative_Snapshots_Taken__c
	, case when has_edmodo_tipped_school is null then 0 else has_edmodo_tipped_school end as Edmodo_Tipped_School__c
	, case when count_edmodo_tipped_schools is null then 0 else count_edmodo_tipped_schools end as Total_Edmodo_Tipped_Schools__c
	, case when has_sales_tipped_school is null then 0 else has_sales_tipped_school end as Sales_Tipped_School__c
	, case when count_sales_tipped_schools is null then 0 else count_sales_tipped_schools end as Total_Sales_Tipped_Schools__c
	, case when purchasing_district is null then 0 else purchasing_district end as Purchased_SFS__c
	, case when earliest_expiration is null then '' else earliest_expiration end as Earliest_Expiration__c
	, sai.account_id
    from
	   (select 
	      report_date as As_of_Date__c
	    , district_id as District_ID_text__c
	    , district_name as Name
	    , State as BillingState
	    , case when subdomain is null then '-' else subdomain end as District_Subdomain__c
	    , case when requester is null then '-' else requester end as Subdomain_Requestor__c
	    , ip_forward IP_Forwarding__c
	    , sum(case when user_type='TEACHER' and active_schools is not null then active_schools else '' end) as Total_Active_Schools__c
	    , sum(case when user_type='TEACHER' and code_verified is not null then code_verified else '' end) as Verified_Teachers__c
	    , sum(case when user_type='STUDENT' and code_verified is not null then code_verified else '' end) as Verified_Registered_Students__c
	    , sum(case when user_type='TEACHER' and cumulative_reg is not null then cumulative_reg else '' end) as Total_Registered_Teachers__c
	    , sum(case when user_type='STUDENT' and cumulative_reg is not null then cumulative_reg else '' end) as Total_Registered_Students__c
	    , sum(case when user_type='TEACHER' and 7d is not null then 7d else '' end) as X7d_Teacher_Actives__c
	    , sum(case when user_type='STUDENT' and 7d is not null then 7d else '' end) as X7d_Student_Actives__c
	    , sum(case when user_type='TEACHER' and 28d is not null then 28d else '' end) as X28d_ACtiv__c
	    , sum(case when user_type='STUDENT' and 28d is not null then 28d else '' end) as X28d_Student_Actives__c
	    , case when avg(num_parents) is null then 0 else round(avg(num_parents),0) end as Total_Registered_Parents__c
	    from adoption_dash 
	    where partition_date = '${partition_date}'
	    group by report_date,district_id,district_name,State,subdomain,requester,ip_forward) ad
	    
        join districts d on d.district_id=ad.District_ID_text__c
	    
        left outer join 
	        (select 
	            sad.district_id
	            , sum(28d_snapshot_teacher_count) as 28d_snapshot_teacher
	            , sum(28d_snapshot_student_count) as 28d_snapshot_student
	            , sum(cum_snapshot_teacher_count) as snapshot_teachers
	            , max(case when tipped_status='tipped' then 1 else 0 end) as has_edmodo_tipped_school
	            , sum(case when tipped_status='tipped' then 1 else 0 end) as count_edmodo_tipped_schools
	            , max(case when cum_snapshot_teacher_count>=3 then 1 else 0 end) as has_sales_tipped_school
	            , sum(case when cum_snapshot_teacher_count>=3 then 1 else 0 end) as count_sales_tipped_schools
	            , sum(cum_snapshot_teacher_count) as cumulative_snapshot_teachers
	            , sum(cum_snapshots_given) as cumulative_snapshots_assigned
	            , sum(cum_snapshot_student_count) as cumulative_snapshot_students
	            , sum(cum_snapshots_taken) as cumulative_snapshots_taken
	            , max(case when s.snapshot_expires_at>=to_date(from_unixtime(unix_timestamp())) and s.snapshot_expires_at is not null then 1 else 0 end) as purchasing_district
	            , min(s.snapshot_expires_at) as earliest_expiration
	            from
	            snapshot_adoption_dash sad
	            left outer join
	            default.schools s 
	            on sad.school_id=s.school_id
	            where partition_date = '${partition_date}'
	        group by sad.district_id
	        )    sad
	    on sad.district_id=ad.District_ID_text__c
        
        join taha.salesforce_account_ids sai on sai.district_id = ad.district_id_text__c
) z
	    
	    
                            
					""")

		#Return column info from query
		f = cur.getSchema()
		fields.append(f)
		# print f
		
		#Fetch table results
		for r in cur.fetch():
			results.append(r)

 

# for items in fields:
# 	for row in items:
# 		output.writerow(row['columnName'])

cleaned_results = []
export=open(str(file_name) + ".csv","wb");
output=csv.writer(export, lineterminator='\n')


success = []
errors = []

columns = ['As_of_Date__c', 'District_ID_text__c','Name', 'BillingState', 'District_Subdomain__c', 'Subdomain_Requestor__c', 'IP_Forwarding__c',
'Total_Active_Schools__c', 'Verified_Teachers__c', 'Verified_Registered_Students__c', 'Total_Registered_Teachers__c', 'Total_Registered_Students__c',
'X7d_Teacher_Actives__c', 'X7d_Student_Actives__c', 'X28d_ACtiv__c', 'X28d_Student_Actives__c', 'Total_Registered_Parents__c', 'Subdomain_Creation_Date__c',
'Cumulative_Snapshot_Teachers__c', 'Cumulative_Snapshots_Assigned__c', 'Cumulative_Snapshot_Students__c', 'Cumulative_Snapshots_Taken__c',
'Edmodo_Tipped_School__c', 'Total_Edmodo_Tipped_Schools__c', 'Sales_Tipped_School__c', 'Total_Sales_Tipped_Schools__c', 'Purchased_SFS__c',
'Earliest_Expiration__c']

output.writerow(columns)

for row in results:
	if row[10] > 5:
		print row[2].replace("'","")
		output.writerow(row)


#connection to salesforce 
session = SQLForce.Session('production', '', '','' )


n = 0
for row in results:
	if row[10] > 5:
		new_districtname = str(row[2].replace("'",""))

		if row[5]:
			new_requester = str(row[5].replace("'",""))
		if not row[5]:
			new_requester = ''

		soql = """
				UPDATE Account 
				SET 
				As_of_Date__c = '""" + str(row[0]) + """' ,
				Name = '""" + new_districtname + """' ,
				BillingState = '""" + str(row[3]) + """' ,
				District_Subdomain__c = '""" + str(row[4]) + """' ,
				Subdomain_Requestor__c = '""" + new_requester + """' ,
				IP_Forwarding__c = '""" + str(row[6]) + """' ,
				Total_Active_Schools__c = '""" + str(row[7]) + """' ,
				Verified_Teachers__c = '""" + str(row[8]) + """' ,
				Verified_Registered_Students__c = '""" + str(row[9]) + """' ,
				Total_Registered_Teachers__c = '""" + str(row[10]) + """' ,
				Total_Registered_Students__c = '""" + str(row[11]) + """' ,
				X7d_Teacher_Actives__c = '""" + str(row[12]) + """' ,
				X7d_Student_Actives__c = '""" + str(row[13]) + """' ,
				X28d_ACtiv__c = '""" + str(row[14]) + """' ,
				X28d_Student_Actives__c = '""" + str(row[15]) + """' ,
				Total_Registered_Parents__c = '""" + str(row[16]) + """' ,
				Subdomain_Creation_Date__c = '""" + str(row[17]) + """' ,
				Cumulative_Snapshot_Teachers__c = '""" + str(row[18]) + """' ,
				Cumulative_Snapshots_Assigned__c = '""" + str(row[19]) + """' ,
				Cumulative_Snapshot_Students__c = '""" + str(row[20]) + """' ,
				Cumulative_Snapshots_Taken__c = '""" + str(row[21]) + """' ,
				Edmodo_Tipped_School__c = '""" + str(row[22]) + """' ,
				Total_Edmodo_Tipped_Schools__c = '""" + str(row[23]) + """' ,
				Sales_Tipped_School__c = '""" + str(row[24]) + """' ,
				Total_Sales_Tipped_Schools__c = '""" + str(row[25]) + """' ,
				Purchased_SFS__c = '""" + str(row[26]) + """' ,
				Earliest_Expiration__c = '""" + str(row[27]) + """' 	

				WHERE District_ID_text__c =  '""" + str(row[1]) + """'"""

		try:
			update_ = session.runCommands(soql)
			if update_:
				print " Updated: ", row[1], row[2]
				success.append(row)
			else:
				print "** ERROR: ", row[1], row[2]
				errors.append(row)
			#print soql
			# nUpdated = session.getenv('ROW_COUNT')
			# if nUpdated == '0':
			# 	print "** ERROR: ", row[1], row[2]
			# 	errors.append(row)
			# else:
			# 	print " Updated: ", row[1], row[2]
			# 	success.append(row)
		except:
			pass
			print "Did not update row: ", row[1], row[2]
			errors.append(row)

	n = n + 1


e=open("errors_" + str(file_name),"wb");
err=csv.writer(e, lineterminator='\n')

for row in errors:
	err.writerow(row)


