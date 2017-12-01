from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

# template_dir = os.path.join(os.path.dirname(__file__), 'templates')  save2
# jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('signup.html')

def common_edits(field1):
    error_msg = ''
    if not field1:
        error_msg = 'must be entered'
        return error_msg
    if len(field1) < 3 or len(field1) > 20:
        error_msg = ' must be greater than 3 characters but no more 20 characters'
        return error_msg
    if ' ' in field1:
        error_msg = ' cannot contain spaces'
        return error_msg 

    return error_msg

def email_edits(field2):
    error_msg = ''
    if len(field2) < 3 or len(field2) > 20:
        error_msg = 'The email must be greater than 3 characters but no more 20 characters'
        return error_msg

    astrik_edit = field2.count('@')
    period_edit = field2.count('.')

    if astrik_edit != 1 or period_edit != 1 :
        print('asterik', astrik_edit)
        print('period', period_edit)
        error_msg = 'A valid email must contain one @ and one period '
        return error_msg 

    return error_msg   


@app.route("/signup", methods=['POST'])


def validate_signup():
    no_errors = True
    user_error = ''
    name_error = ''
    pass_error = ''
    ver_error = ''
    email_error = ''
    username = request.form['username']
    err_check = common_edits(username)
    if len(err_check) > 0:
       no_errors = False
       name_error = 'User ' + err_check
    password = request.form['password']
    err_check = common_edits(password)
    if len(err_check) > 0:
       no_errors = False
       pass_error = 'Password ' +  err_check
    verify = request.form['verify']
    err_check = common_edits(verify)
    if len(err_check) > 0:
       no_errors = False
       ver_error = 'Password verification ' +  err_check
    if password != verify:
       no_errors = False
       ver_error = 'Password and verification must match'
    
    email = request.form['email']
    if email:
        email_check = email_edits(email)
        if len(email_check) > 0:
            no_errors = False
            email_error = email_check
            email = ''

    if no_errors:
        name = username
        print('name 1', name)
        return redirect('/welcome?name=' + name)
    else:
        return render_template('signup.html', user_error = name_error, pass_error = pass_error, 
          ver_error = ver_error, username = username, email = email, email_error = email_error)




@app.route('/welcome')
def valid_time():
    name = request.args.get('name')
    print('name 2', name)
    return render_template('welcome.html', name = name)


app.run()