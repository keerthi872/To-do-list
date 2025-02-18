from flask import Flask,render_template,request
import pymysql

db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'root',
    'database' : 'FLASKEXAMPLE2'
}

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register1",methods=["POST","GET"])
def register1():
    if request.method == "POST":
        fname = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        pwd1 = request.form['password']
        pwd2 = request.form['createpassword']
        print(fname,email,mobile,pwd1,pwd2)
        if pwd1 == pwd2:
            try:
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor()
                q = "INSERT INTO USERS VALUES (%s,%s,%s,%s)"
                cursor.execute(q,(fname,email,mobile,pwd1))
                conn.commit()
            except:
                return "Data storage Uncessfull !"
            else:
                return render_template("login.html")
        else:
            return "Make sure Password and Confirm Password mathces"
    else:
        return "Method is not Post"

@app.route("/login1",methods = ["POST","GET"])
def login1():
    if request.method == "POST":
        email = request.form['email']
        pwd = request.form['password']
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        q = "SELECT * FROM USERS WHERE EMAIL=(%s) AND PWD=(%s)"
        cursor.execute(q,(email,pwd))
        x = cursor.fetchall()
        conn.commit()
        print(x)
        if len(x) > 0:
            return render_template("userhome.html",email=x[0][1])
        else:
            return "Invalid Credintials"
    else:
        return "Method is not Post"
    
@app.route("/addtask",methods=["POST","GET"])
def addtask():
    if request.method == "POST":
        email = request.form['email']
        return render_template("addtask.html",email=email)

@app.route("/add_task1",methods = ["POST","GET"])
def add_task1():
    if request.method == "POST":
        email = request.form["email"]
        taskname = request.form["name"]
        tasktime = request.form["task_time"]
        taskdescription = request.form["description"]
        print(email,taskname,tasktime,taskdescription)
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            q = "SELECT * FROM TASKS WHERE EMAIL= (%s) AND TASKTIME = (%s)"
            cursor.execute(q,(email,tasktime))
            x1 = cursor.fetchall()
            conn.commit()
            if len(x1) == 0:
                conn = pymysql.connect(**db_config)
                cursor = conn.cursor()
                q = "INSERT INTO TASKS VALUES (%s,%s,%s,%s)"
                cursor.execute(q,(email,taskname,tasktime,taskdescription))
                conn.commit()
            else:
                return "Time Slot not available"
        except:
            return "Data storage Uncessfull !"
        else:
            return render_template("userhome.html",email=email)
    else:
        return "Method was not post"
@app.route("/removetask",methods=["POST","GET"])
def removetask():
    if request.method == "POST":
        email = request.form['email']
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            q = "SELECT * FROM TASKS WHERE EMAIL=(%s)"
            cursor.execute(q,(email))
            x = cursor.fetchall()
            print(x)
            conn.commit()
        except:
            return "Error Occured"
        else:
            return render_template("removetask.html",email=email,data=x)
    else:
        return "Method is not Post"
@app.route("/deletetask",methods = ["POST","GET"])
def deletetask():
    if request.method == "POST":
        email = request.form["mail"]
        ttime = request.form["ttime"]
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            q = "DELETE FROM TASKS WHERE EMAIL = (%s) and TASKTIME = (%s)"
            cursor.execute(q,(email,ttime))
            conn.commit()

            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            q = "SELECT * FROM TASKS WHERE EMAIL=(%s)"
            cursor.execute(q,(email))
            x = cursor.fetchall()
            conn.commit()
        except:
            return "Function Un sucess"
        else:
            return render_template("removetask.html",email=email,data=x)
    else:
        return "Method is not POST"
if __name__ == "__main__":
    app.run(port=5015)