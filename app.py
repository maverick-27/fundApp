from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from multiprocessing import Value
from flask import flash
# import re
from werkzeug.utils import redirect

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'fundsapp'

mysql = MySQL(app)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        fund_short_name = request.form['fund_short_name']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM fundsapp WHERE fund_short_name=%s", (fund_short_name,))
        fund = cursor.fetchone()
        if fund:
            mysql.connection.commit()
            cursor.close()
            return render_template("duplicateError.html")
        version = '1'
        fund_short_name = request.form['fund_short_name']
        supplier = request.form['supplier']
        fund_type = request.form['fund_type']
        created_date = datetime.now()
        updated_date = datetime.now()
        created_by = request.form["created_by"]
        updated_by = request.form["updated_by"]
        active_indicator = 'Y'
        print("Second")

        data = (
            version, fund_short_name, supplier, fund_type, created_date, updated_date, created_by, updated_by,
            active_indicator)
        print(data)
        cursor.execute("INSERT INTO fundsapp VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
        mysql.connection.commit()
        cursor.close()
        msg = 'You have Added fund successfully'
        return redirect('/')


@app.route('/')
def RetrieveList():
    cursor = mysql.connection.cursor()
    active_indicator = 'Y'

    cursor.execute("select a.fund_short_name, a.supplier, a.fund_type, a.version  from fundsapp a Inner Join(select "
                   "fund_short_name, max(fund_type), max(supplier), max(version) version from fundsapp group by "
                   "fund_short_name) b ON a.fund_short_name = b.fund_short_name and a.version = b.version where "
                   "active_indicator =%s", (active_indicator))

    funds = cursor.fetchall()
    return render_template("datalist.html", funds=funds)


@app.errorhandler(500)
def resource_not_found(e):
    return render_template('duplicateError.html')


# @app.route('/<int:id>', methods=['GET', 'POST'])
# def RetrieveFunds(id):
#     conn = mysql.connect()
#     cursor = mysql.connection.cursors.DictCursor
#     cursor.execute("SELECT * FROM fundsapp WHERE fund_id=%s", (id,))
#     fund = cursor.fetchone()


# return render_template("data.html", fund=fund)


@app.route('/<id>/edit', methods=['GET', 'POST'])
def update(id):
    data = 0
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT  max(version) ,max(fund_short_name) , max(supplier) , max(fund_type) ,created_date, updated_date , "
        "created_by, updated_by ,active_indicator FROM fundsapp WHERE "
        "fund_short_name=%s", (id,))

    fund = cursor.fetchone()
    print(fund)
    if request.method == 'POST':
        if fund:
            data = int(fund[0])
            print(fund)
            print(type(data))
            data += 1
            print(data)
            print(type(data))
            fund_short_name = request.form.get('fund_short_name')
            supplier = request.form.get('supplier')
            if supplier is None:
                supplier = fund[2]
            fund_type = request.form.get('fund_type')
            created_date = fund[4]
            created_by = fund[6]
            updated_date = datetime.now()
            updated_by = fund[7]
            active_indicator = "Y"
            cursor = mysql.connection.cursor()
            data = (
                str(data), fund_short_name, supplier, fund_type, created_date, updated_date, created_by,
                updated_by,
                active_indicator)
            cursor.execute("INSERT INTO fundsapp VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
            mysql.connection.commit()
            cursor.close()
            msg = 'You have Edit fund successfully'
            return redirect('/')
    return render_template("edit.html", fund=fund)


@app.route('/<id>/delete', methods=['GET', "POST"])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM fundsapp WHERE fund_short_name=%s", (id,))
    fund = cursor.fetchone()
    if request.method == 'POST':
        if fund:
            print("Delete")
            print(fund)
            sql = "Update fundsapp set active_indicator='N' where fund_short_name=%s"
            data = id
            cursor.execute(sql, (id,))
            mysql.connection.commit()
            cursor.close()
            return redirect('/')
    return render_template('delete.html')


app.run(host='localhost', port=5000)
