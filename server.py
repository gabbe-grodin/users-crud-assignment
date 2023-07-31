from flask import Flask, render_template, request, redirect
from user import User
app = Flask(__name__)

@app.route("/")
def index():
    users = User.get_all()
    print(users)
    return render_template("index.html", users = users)

@app.route('/users', methods=['POST'])
def create_user():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    User.save(request.form)
    return redirect('users.html')

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)