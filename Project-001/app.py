from flask import Flask, render_template, request, redirect, url_for, flash, session, json, jsonify
from flask_mysqldb import MySQL
import MySQLdb

import mysql.connector
import pymysql
import re

app = Flask(__name__)

app.secret_key = 'xyzsdfg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Parth@123'
app.config['MYSQL_DB'] = 'ip'

mysql = MySQL(app)
# LOGIN


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            session["loginsuccess"] = True
            message = 'Logged in successfully !'
            return redirect(url_for('Index'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message=message)


# Logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
# Main


@app.route('/user')
def Index():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM ip.branch")
        data = cur.fetchall()
        cur.close()
        return render_template('test-index.html', branch=data)
    else:
        return redirect(url_for('login'))


# Debug

def api_response():
    from flask import jsonify
    if request.method == 'POST':
        return jsonify(**request.json)
# Delete


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    if 'loggedin' in session:
        flash("Record Has Been Deleted Successfully")
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM ip.branch WHERE branchid=%s", (id_data,))
        mysql.connection.commit()
        return redirect(url_for('Index'))
    else:
        return redirect(url_for('login'))

# Edit-TODO


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    print(request.method)
    if request.method == 'POST':
        id_data = request.form['id']
        region = request.form['region']
        branch = request.form['branch']
        device = request.form['device']
        type1 = request.form['type']
        device_model = request.form['device-model']
        wan1 = request.form['wan1']
        isp1 = request.form['isp1']
        link1 = request.form['link1']
        circuit1 = request.form['circuit1']
        wan2 = request.form['wan2']
        isp2 = request.form['isp2']
        link2 = request.form['link2']
        circuit2 = request.form['circuit2']
        additional = request.form['additional']
        isp3 = request.form['isp3']
        link3 = request.form['link3']
        circuit3 = request.form['circuit3']
        lan1 = request.form['lan1']
        subnet1 = request.form['subnet1']
        lan2 = request.form['lan2']
        subnet2 = request.form['subnet2']
        if "managed" in request.form:
            managed = request.form['managed']
        else:
            managed = "unmanaged"

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE ip.branch SET region=%s, branch=%s, device=%s, type1=%s, device_model=%s, wan1=%s, isp1=%s, link1=%s, circuit1=%s, wan2=%s,isp2=%s, link2=%s, circuit2=%s,additional=%s,isp3=%s, link3=%s, circuit3=%s,lan1=%s, subnet1=%s,lan2=%s, subnet2=%s,managed=%s
        WHERE branchid=%s
        """, (region, branch, device, type1, device_model,  wan1, isp1, link1, circuit1, wan2, isp2, link2, circuit2, additional, isp3, link3, circuit3, lan1, subnet1, lan2, subnet2, managed, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))

# Add


@app.route('/add', methods=['POST', 'GET'])
def add():
    print("Stage 1")
    if 'loggedin' in session:
        print("Stage 2", request.method)

        print(request.method)
        if request.method == 'POST':
            print("Stage 3")

            print("Hey There")
            region = request.form['region']
            branch = request.form['branch']
            device = request.form['device']
            type1 = request.form['type']
            device_model = request.form['device-model']
            wan1 = request.form['wan1']
            isp1 = request.form['isp1']
            link1 = request.form['link1']
            circuit1 = request.form['circuit1']
            wan2 = request.form['wan2']
            isp2 = request.form['isp2']
            link2 = request.form['link2']
            circuit2 = request.form['circuit2']
            additional = request.form['additional']
            isp3 = request.form['isp3']
            link3 = request.form['link3']
            circuit3 = request.form['circuit3']
            lan1 = request.form['lan1']
            subnet1 = request.form['subnet1']
            lan2 = request.form['lan2']
            subnet2 = request.form['subnet2']
            if "managed" in request.form:
                managed = request.form['managed']
            else:
                managed = "unmanaged"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO  branch(region, branch, device, type1, device_model,  wan1, isp1, link1, circuit1, wan2, isp2, link2, circuit2, additional, isp3, link3, circuit3, lan1, subnet1, lan2, subnet2, Managed) VALUES (%s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)",
                           (region, branch, device, type1, device_model,  wan1, isp1, link1, circuit1, wan2, isp2, link2, circuit2, additional, isp3, link3, circuit3, lan1, subnet1, lan2, subnet2, managed))
            mysql.connection.commit()
            return redirect(url_for('Index'))
            print(cursor)
        return render_template('add.html')
    else:
        return redirect(url_for('login'))

# View


@app.route('/update', methods=['POST', 'GET'])
def update():
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.debug = True
    app.run()
