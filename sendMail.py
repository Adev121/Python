import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

msg = MIMEMultipart()

server = smtplib.SMTP('smtp.gmail.com',587)

server.starttls()
server.login('kumarramabhishek89@gmail.com','odnkegekctmaxlou')
toaddr = 'megh00sh@gmail.com'
fromaddr= 'kumarramabhishek89@gmail.com'


msg['From'] = fromaddr 
  
# storing the receivers email address  
msg['To'] = toaddr 
  
# storing the subject  
msg['Subject'] = "Subject of the Mail"
  
# string to store the body of the mail 
body = "Mail is sent from Python"
  
# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 
  
# open the file to be sent  
filename = "RECON_060824_215810.xlsx"
attachment = open(filename, "rb") 

# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
p.set_payload((attachment).read()) 
  
# encode into base64 
encoders.encode_base64(p) 
   
p.add_header('Content-Disposition', f"attachment; filename= {filename}") 
  
# attach the instance 'p' to instance 'msg' 
msg.attach(p) 
  

server.send_message(msg)
print('Mail Sent ! please check your mail.')