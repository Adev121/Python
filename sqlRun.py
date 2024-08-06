# Python script for runing the sql query and export the file and mail

import cx_Oracle
import pandas as pd
import time
from datetime import datetime
import schedule
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import smtplib


con = cx_Oracle.connect('hr/hr@localhost:1521')
cur = con.cursor()

# SQL query to fetch the employee details
query = 'select * from departments'

cur.execute(query)

print("Query Executed successfully")


# Fetch all rows from the executed query
rows = cur.fetchall()
# Get the column names from the cursor
column_names = [col[0] for col in cur.description]

# Generate the filename with the current date and time
current_time = datetime.now().strftime("%d%m%y_%H%M%S")


# Create a DataFrame from the fetched data
df = pd.DataFrame(rows, columns=column_names)

output_file = f'RECON_{current_time}.xlsx'
df.to_excel(output_file, index=False)

print(f"Query executed successfully and results exported to {output_file}")
cur.close()
con.close()

#Mail sending Part
msg= MIMEMultipart()

#SMTP server setup
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

toaddr = 'megh00sh@gmail.com'
fromaddr = 'kumarramabhishek89@gmail.com'
password = 'odnkegekctmaxlou'

#login credentials
server.login(fromaddr,password)

msg['Subject'] = 'Employee Data Reconciliation Report'
msg['From'] = fromaddr
msg['to'] = toaddr
body = 'Hi this is a test attachment !'

msg.attach(MIMEText(body, 'plain'))

# Open the file in binary mode

filename = output_file
attachment = open(filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())

# Encode the attachment

encoders.encode_base64(part)

part.add_header('Content-Disposition', f"attachment; filename= {filename}")

msg.attach(part)

# Sending the email
server.send_message(msg)
print('Mail Sent ! please check your mail.')