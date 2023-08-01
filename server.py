from flask import Flask, render_template, request, redirect, session
from user import User

app = Flask(__name__)

app.secret_key = "khsdfughpaiuhgioasdhvihgharoighvoisdhvkshgiahsdivhlskhgoisdhvs43956723]"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/users/create', methods=['POST'])
def create_user():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    # print("session!!!!!!!!!!!!!!")
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    # print("before!!!!!!!!!")
    User.save(data)
    # print("after!!!!!!!!!!!!")
    return redirect("/users")

@app.route('/users')
def show_users():
    users = User.get_all(request.form)
    print(request.form)
    # print("___________________________")
    return render_template("users.html", first_name=session['first_name'], last_name=session['last_name'], email=session['email'],users=users)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)