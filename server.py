from flask import Flask, render_template, request, redirect, session
from user import User
import pprint

app = Flask(__name__)

app.secret_key = "khsdfughpaiuhgioasdhvihgharoighvoisdhvkshgiahsdivhlskhgoisdhvs43956723]"

@app.route("/")
def home():
    return render_template("index.html")

# ! CREATE
@app.route('/create/user', methods=['POST'])
def create_user():
    # pprint.pp("session!!!!!!!!!!!!!!")
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    # print("before!!!!!!!!!")
    User.create_user(request.form)
    # print("after!!!!!!!!!!!!")
    return redirect("/users")

# ! READ (all)
@app.route('/users')
def show_users():
    users = User.get_all_users()
    # pprint.pp(users)
    # print("___________________________")
    return render_template("users.html", first_name=session['first_name'], last_name=session['last_name'], email=session['email'],users=users)

# ! READ (one)
@app.route('/user/<int:id>')
def show_user(id):
    data = {"id": id}
    user = User.get_one_user_by_id(data)
    return render_template('show.html', first_name=session['first_name'], last_name=session['last_name'], email=session['email'], user = user)


# ! UPDATE
@app.route('/update/<int:id>')
def update_form(id):
    data = {"id": id}
    user = User.get_one_user_by_id(data)
    print(user)
    return render_template('update.html', user = user)

# ! UPDATE
@app.route('/update/user', methods=['POST'])
def update_user():
    data = {
        "id": request.form['id'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    User.update_user_by_id(data)
    return redirect('/users')

# ! DELETE
@app.route('/delete/user/<int:id>')
def delete_one_user(id):
    User.delete_one_user(id)
    return redirect('/users')


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)