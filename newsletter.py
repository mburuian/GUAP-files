from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import schedule
import time
import threading

app = Flask(__name__)

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mburuian",
        database="guapdata"
    )

# Route to display the form (subscribe page)
@app.route('/')
def index():
    return render_template('index4.html')

# Route to handle form submission
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')

    # Insert the email into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subscribers (email) VALUES (%s)", (email,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

# Function to send newsletters
def send_newsletter():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM subscribers")
    subscribers = cursor.fetchall()
    cursor.close()
    conn.close()

    # Setup email
    sender_email = "guapgiveaways@gmail.com"
    subject = "Weekly Newsletter"

    for subscriber in subscribers:
        recipient_email = subscriber[0]
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email

        # Create the body of the message
        html = """\
        <html>
          <body>
            <p>Hi,<br>
               Here is this week's newsletter!<br>
               Check out our latest updates and giveaways.
            </p>
          </body>
        </html>
        """
        part = MIMEText(html, "html")
        message.attach(part)

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, "ilovecoding247")
                server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")

# Schedule the newsletter to be sent weekly
def run_scheduler():
    schedule.every().week.do(send_newsletter)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run Flask app and scheduler in separate threads
if __name__ == '__main__':
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Start the Flask app
    app.run(debug=True)
