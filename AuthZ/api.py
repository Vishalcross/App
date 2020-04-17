import flask
from flask import request, jsonify, render_template, redirect,session,json
from forms import LoginForm
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'

# Create some test data for our catalog in the form of a list of dictionaries.

userdata = {'user1': 'Flag Not Found',
        'user2': 'Flag Found',
        'user3': 'Flag Not Found',
        }

userdb = {'user1': 'user1pass',
'user2': 'qwerty',
'user3': 'qwerty'}




@app.route('/', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    session['loggedin']=False
    if form.validate_on_submit():
        print(form.username.data in userdb.keys(),file=sys.stderr)
        print(form.password.data==userdb[form.username.data ],file=sys.stderr)
        if form.username.data in userdb.keys() and userdb[form.username.data] == form.password.data:
            print(form.username.data in userdb.keys(),file=sys.stderr)
            session['loggedin']=True
            return redirect("/user/"+str(form.username.data))

        else:
            return redirect("/")
  


    return render_template('login.html', title='Sign In', form=form)



@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    print("ii",file=sys.stderr)
    if session.get('loggedin',None)==True:  
       
        return json.dumps({'message': 'Hello User', 'data': userdata[username]}), 200
    else:
        print("i",file=sys.stderr)
        return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
