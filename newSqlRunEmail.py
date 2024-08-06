import schedule
import time
import cx_Oracle
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def run_sql_script():
    try:
        # Establish connection to the Oracle database
        con = cx_Oracle.connect('hr/hr@localhost:1521/xe')
        cur = con.cursor()

        # SQL query to fetch the department details
        query = 'SELECT * FROM departments'

        # Execute the query
        cur.execute(query)

        # Fetch all rows from the executed query
        rows = cur.fetchall()

        # Get the column names from the cursor
        column_names = [col[0] for col in cur.description]

        # Create a DataFrame from the fetched data
        df = pd.DataFrame(rows, columns=column_names)

        # Generate the filename with the current date and time
        current_time = datetime.now().strftime("%d%m%y_%H%M%S")
        output_file = f'departments_{current_time}.xlsx'

        # Export the DataFrame to an Excel file
        df.to_excel(output_file, index=False)

        print(f"Query executed successfully and results exported to {output_file}")

        # Send email with the generated file as attachment
        send_email(output_file)

    except cx_Oracle.Error as error:
        print(f"Error: {error}")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
        print("Oracle connection is closed")

def send_email(attachment):
    fromaddr = "kumarramabhishe89@gmail.com"
    toaddr = "megh00sh@gmail.com"
    subject = "Departments Report"
    body = "Please find attached the latest departments report."

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Open the file to be sent
    with open(attachment, "rb") as attachment_file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment}")

        # Attach the instance 'part' to instance 'msg'
        msg.attach(part)

    # Create SMTP session for sending the mail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use the appropriate SMTP server and port
        server.starttls()
        server.login(fromaddr, "odnkegekctmaxlou")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Schedule the task to run every minute
schedule.every(1).minutes.do(run_sql_script)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
