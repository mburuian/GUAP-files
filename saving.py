from flask import Flask, request, redirect, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mburuian'
app.config['MYSQL_DB'] = 'guapdata'

mysql = MySQL(app)

# Route to display the newsletter subscription form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form['email']
        # Save email to database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO emails (email) VALUES (%s)", [email])
        mysql.connection.commit()
        cur.close()
        return redirect('/thank-you')


    # Route for the thank-you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(debug=True)
