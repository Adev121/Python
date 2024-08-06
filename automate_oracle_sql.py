import schedule
import time
import cx_Oracle

# Function to run the SQL script
def run_sql_script():
    try:
        # Establish connection to the Oracle database
        dsn_tns = cx_Oracle.makedsn('localhost', 1521, service_name='xe')
        connection = cx_Oracle.connect(user='hr', password='hr', dsn=dsn_tns)

        cursor = connection.cursor()

        # Read the SQL script
        with open('your_sql_script.sql', 'r') as file:
            sql_script = file.read()

        # Execute the SQL script
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
                connection.commit()

        print("SQL script executed successfully")

    except cx_Oracle.Error as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Oracle connection is closed")

# Schedule the task to run every hour
schedule.every().hour.do(run_sql_script)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
