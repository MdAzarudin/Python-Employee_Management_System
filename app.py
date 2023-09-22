
from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3 as sql

app = Flask(__name__)

app.secret_key = "Azar123"

def isloggedin():
     return "username" in session

@app.route('/base')
def base():
     return render_template ("base.html")

@app.route('/', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("pass")
        con = sql.connect("user.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from signup where username=? and password=?", (username,password))
        data = cur.fetchall()
        for  i in data:
            if username in i and password == i[1]:
                session["username"] = username
                return redirect (url_for('home'))
            else:
                return "Incorrect Username or Password"
    return render_template ("login.html")

@app.route('/signup', methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        name1 = request.form.get("username")
        pass1 = request.form.get("password")
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("insert into signup (username,password) values(?,?)",
                        (name1,pass1))
        con.commit()
        return redirect (url_for('login'))
    return render_template ("signup.html") 

@app.route("/employee_details")
def home():
    con = sql.connect("user.db")
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM EMPLOYEE")
    data = cur.fetchall()
    return render_template ("index.html", sun=data)

@app.route("/insert",methods = ["GET","POST"])
def add():
    if request.method == "POST":
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("INSERT INTO EMPLOYEE (name,age,Doj,email,gender,contact,address)VALUES(?,?,?,?,?,?,?)",
                      (request.form.get("name"),request.form.get("age"),request.form.get("doj")
                       ,request.form.get("email"),
                       request.form.get("gender"),request.form.get("contact"),request.form.get("address")))
        con.commit()
        return redirect(url_for("home"))
    return render_template ("add_user.html")

@app.route("/edit/<string:id>",methods = ["GET","POST"])
def edit(id):
    if request.method == "POST":
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("UPDATE EMPLOYEE SET NAME=?,AGE=?,DOJ=?,EMAIL=?,GENDER=?,CONTACT=?,ADDRESS=? WHERE ID=?",
                     (request.form.get("name"),request.form.get("age"),request.form.get("doj"),
                      request.form.get("email"),
                      request.form.get("gender"),request.form.get("contact"),request.form.get("address"),id))
        con.commit()
        return redirect(url_for("home"))
    return render_template ("edit_user.html")

@app.route("/delete/<string:id>",methods=["GET","POST"])
def delete(id):
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("DELETE FROM EMPLOYEE WHERE ID=?",(id,))
        con.commit()
        return redirect(url_for("home"))
    
    

if __name__ =="__main__":
     app.run(debug=True)

            


 

