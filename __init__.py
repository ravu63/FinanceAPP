import Admin
import Customer
import Feedback
import Loan
import random
import shelve
from datetime import date

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message

from Forms import CreateCustomerForm, LoginForm, UpdateCustomerForm, UpdateCustomerForm2, ForgetPassword, OTPform, \
    ChangePassword, FeedbackForm, SearchCustomerForm, UpdateStatus, CreateLoanForm

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "radiantfinancenyp@gmail.com"
app.config['MAIL_PASSWORD'] = "Radiant12345"

mail = Mail(app)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.static_folder = 'static'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html')
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

#Joshua
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST':
        users = shelve.open('signup.db', 'r')
        email = request.form['email']
        password = request.form['password']
        users_dict = users['Customers']

        users_keys = list(users_dict.keys())
        try:
            user = users_dict[email]
            if user.get_email() == email:
                if user.check_password(password):
                    if user.get_role() == 0:
                        session['id'] = user.get_email()
                        users.close()
                        return redirect(url_for('main'))
                    else:
                        users.close()
                        return redirect(url_for('dashboard'))
                else:
                    flash(u'Invalid password or email provided')
            else:
                flash(u'Invalid password or email provided')
        except:
            flash(u'Invalid password or email provided')

    return render_template('login.html', form=login_form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('signup.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")
        try:
            user = shelve.open('signup.db', 'r')
            users_dict = user['Customers']
            users_keys = list(users_dict.keys())
            if create_customer_form.email.data in users_keys:
                flash(u'User exists')
            else:
                customer = Customer.Customer(
                    create_customer_form.name.data,
                    create_customer_form.gender.data,
                    create_customer_form.phone.data,
                    create_customer_form.birthdate.data,
                    create_customer_form.email.data,
                    create_customer_form.password.data
                )
                customers_dict[customer.get_email()] = customer
                db['Customers'] = customers_dict
                db.close()
                return redirect(url_for('login'))

        except:
            customer = Customer.Customer(
                create_customer_form.name.data,
                create_customer_form.gender.data,
                create_customer_form.phone.data,
                create_customer_form.birthdate.data,
                create_customer_form.email.data,
                create_customer_form.password.data
            )
            customers_dict[customer.get_email()] = customer
            db['Customers'] = customers_dict
            db.close()
            return redirect(url_for('login'))


    return render_template('signup.html' , form=create_customer_form)


@app.route('/createAdmin', methods=['GET', 'POST'])
def create_admin():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('signup.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        try:
            user = shelve.open('signup.db', 'r')
            users_dict = user['Customers']
            users_keys = list(users_dict.keys())
            if create_customer_form.email.data in users_keys:
                flash(u'User exists')
            else:
                customer = Admin.Customer(
                    create_customer_form.name.data,
                    create_customer_form.gender.data,
                    create_customer_form.phone.data,
                    create_customer_form.birthdate.data,
                    create_customer_form.email.data,
                    create_customer_form.password.data
                )
                customers_dict[customer.get_email()] = customer
                db['Customers'] = customers_dict
                db.close()
                return redirect(url_for('manage_admin'))

        except:
            customer = Admin.Customer(
                create_customer_form.name.data,
                create_customer_form.gender.data,
                create_customer_form.phone.data,
                create_customer_form.birthdate.data,
                create_customer_form.email.data,
                create_customer_form.password.data
            )
            customers_dict[customer.get_email()] = customer
            db['Customers'] = customers_dict
            db.close()
            return redirect(url_for('manage_admin'))
    return render_template('createAdmin.html', form=create_customer_form)


@app.route('/manageCustomer', methods=['GET', 'POST'])
def manage_customers():
    customers_dict = {}
    db = shelve.open('signup.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
    return render_template('manageCustomer.html', count=len(customers_list), customers_list=customers_list)


@app.route('/manageAdmin', methods=['GET', 'POST'])
def manage_admin():
    customers_dict = {}
    db = shelve.open('signup.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
    return render_template('manageAdmin.html', count=len(customers_list), customers_list=customers_list)


@app.route('/updateCustomer/<id>/', methods=['GET', 'POST'])
def customer_user(id):
    update_customer_form = UpdateCustomerForm(request.form)

    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('signup.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_birthdate(update_customer_form.birthdate.data)
        customer.set_phone(update_customer_form.phone.data)

        db['Customers'] = customer_dict
        db.close()

        return redirect(url_for('manage_customers'))
    else:
        users_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer = customer_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.birthdate.data = customer.get_birthdate()
        update_customer_form.phone.data = customer.get_phone()

        return render_template('updateCustomer.html', form=update_customer_form)


@app.route('/updateAdmin/<id>/', methods=['GET', 'POST'])
def customer_Admin(id):
    update_customer_form = UpdateCustomerForm(request.form)

    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('signup.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_birthdate(update_customer_form.birthdate.data)
        customer.set_phone(update_customer_form.phone.data)

        db['Customers'] = customer_dict
        db.close()

        return redirect(url_for('manage_admin'))
    else:
        users_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer = customer_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.birthdate.data = customer.get_birthdate()
        update_customer_form.phone.data = customer.get_phone()

        return render_template('updateCustomer.html', form=update_customer_form)


@app.route('/deleteCustomer/<id>', methods=['POST'])
def delete_customer(id):
    customer_dict = {}
    db = shelve.open('signup.db', 'w')
    customer_dict = db['Customers']

    customer_dict.pop(id)

    db['Customers'] = customer_dict
    db.close()

    return redirect(url_for('manage_customers'))


@app.route('/deleteAdmin/<id>', methods=['POST'])
def delete_admin(id):
    customer_dict = {}
    db = shelve.open('signup.db', 'w')
    customer_dict = db['Customers']

    customer_dict.pop(id)

    db['Customers'] = customer_dict
    db.close()

    return redirect(url_for('manage_admin'))


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/forgotPassword', methods=['POST', 'GET'])
def forgot_password():
    login_form = ForgetPassword(request.form)
    try:
        if request.method == 'POST':
            users = shelve.open('signup.db', 'r')
            email = request.form['email']
            users_dict = users['Customers']
            users_keys = list(users_dict.keys())
            user = users_dict[email]
            if user.get_email() == email:
                session['id'] = user.get_email()
                users.close()
                return redirect(url_for('getOTP'))
            else:
                flash(u'Invalid email provided')
    except:
        flash(u'Invalid email provided')

    return render_template('forgotPassword.html', form=login_form)


@app.route('/getOTP', methods=['POST', 'GET'])
def getOTP():
    if request.method == 'POST':
        otp = random.randint(1111, 9999)
        session['otp'] = otp
        msg = Message('One Time Password', sender='radiantfinancenyp@gmail.com', recipients=[session['id']])
        msg.body = 'here is your OTP:{}'.format(otp)
        mail.send(msg)
        return redirect(url_for('OTP'))
    return render_template('getOTP.html')


@app.route('/OTP', methods=['POST', 'GET'])
def OTP():
    login_form = OTPform(request.form)
    if request.method == 'POST':
        otp = session['otp']
        otp2 = int(request.form['otp3'])
        if otp == otp2:
            return redirect(url_for('change_password', id=id))
        else:
            flash(u'Invalid OTP provided')
    return render_template('OTP.html', form=login_form)


@app.route('/changePassword/<id>', methods=['POST', 'GET'])
def change_password(id):
    update_customer_form = UpdateCustomerForm2(request.form)
    id = session['id']

    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('signup.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_password(update_customer_form.password.data)

        db['Customers'] = customer_dict
        db.close()

        return redirect(url_for('login'))
    return render_template('customerChangePass.html', form=update_customer_form)


@app.route('/manageAccount/<id>/', methods=['GET', 'POST'])
def manage_account(id):
    update_customer_form = UpdateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('signup.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_phone(update_customer_form.phone.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_birthdate(update_customer_form.birthdate.data)

        db['Customers'] = customer_dict
        db.close()

        return redirect(url_for('main'))
    else:
        users_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer = customer_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone.data = customer.get_phone()
        update_customer_form.birthdate.data = customer.get_birthdate()

    return render_template('manageAccount.html', form=update_customer_form)


@app.route('/customerChangePass/<id>/', methods=['GET', 'POST'])
def customer_change(id):
    update_customer_form = ChangePassword(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('signup.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_password(update_customer_form.password.data)

        db['Customers'] = customer_dict
        db.close()

        return redirect(url_for('main'))
    else:
        users_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer = customer_dict.get(id)
        update_customer_form.password.data = customer.get_password()

    return render_template('customerChangePass.html', form=update_customer_form)


@app.route('/searchCustomer', methods=['GET', 'POST'])
def search_customer():
    search_customer_form = SearchCustomerForm(request.form)
    if request.method == 'POST' and search_customer_form.validate():
        search = search_customer_form.searchCustomer.data
        customer_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer_list = []
        for key in customer_dict:
            customer = customer_dict.get(key)
            if search in customer.get_email():
                if customer.get_role() == 0:
                    customer_list.append(customer)
            # else:
            # continue

        if len(customer_list) > 0:
            return render_template('showCustomer.html', count=len(customer_list), customer_list=customer_list)
        else:
            return redirect(url_for('no_customer'))
    return render_template('searchCustomer.html', form=search_customer_form)


@app.route('/searchAdmin', methods=['GET', 'POST'])
def search_admin():
    search_customer_form = SearchCustomerForm(request.form)
    if request.method == 'POST' and search_customer_form.validate():
        search = search_customer_form.searchCustomer.data
        customer_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer_list = []
        for key in customer_dict:
            customer = customer_dict.get(key)
            if search in customer.get_email():
                if customer.get_role() == 1:
                    customer_list.append(customer)
            # else:
            # continue

        if len(customer_list) > 0:
            return render_template('showAdmin.html', count=len(customer_list), customer_list=customer_list)
        else:
            return redirect(url_for('no_customer'))
    return render_template('searchCustomer.html', form=search_customer_form)


@app.route('/feedback/<id>/', methods=['GET', 'POST'])
def create_feedback(id):
    create_feedback_form = FeedbackForm(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedback_dict = db['Feedback']
        except:
            print("Error in retrieving Customers from Feedback.db.")

        feedback = Feedback.Feedback(
            create_feedback_form.name.data,
            create_feedback_form.email.data,
            create_feedback_form.service.data,
            create_feedback_form.website.data,
            create_feedback_form.additional.data

        )
        feedback.set_status('Processing')
        today = date.today()
        feedback.set_date(today)
        feedback_dict[feedback.get_email()] = feedback
        db['Feedback'] = feedback_dict
        db.close()
        return redirect(url_for('main'))
    else:
        customer_dict = {}
        db = shelve.open('signup.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer = customer_dict.get(id)
        create_feedback_form.name.data = customer.get_name()
        create_feedback_form.email.data = customer.get_email()
    return render_template('feedback.html', form=create_feedback_form)


@app.route('/manageFeedback', methods=['GET', 'POST'])
def manage_feedback():
    feedback_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedback_dict = db['Feedback']
    db.close()

    feedback_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        feedback_list.append(feedback)
    return render_template('manageFeedback.html', count=len(feedback_list), feedback_list=feedback_list)


@app.route('/updateFeedback/<id>/', methods=['GET', 'POST'])
def update_status(id):
    update_customer_form = UpdateStatus(request.form)

    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('feedback.db', writeback=True)
        customer_dict = db['Feedback']

        customer = customer_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_service(update_customer_form.service.data)
        customer.set_website(update_customer_form.website.data)
        customer.set_additional(update_customer_form.additional.data)
        customer.set_date(update_customer_form.date.data)
        customer.set_status(update_customer_form.status.data)

        db['Customers'] = customer_dict
        db.sync()
        db.close()

        return redirect(url_for('manage_feedback'))
    else:
        users_dict = {}
        db = shelve.open('feedback.db', 'r')
        customer_dict = db['Feedback']
        db.close()

        customer = customer_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.service.data = customer.get_service()
        update_customer_form.website.data = customer.get_website()
        update_customer_form.additional.data = customer.get_additional()
        update_customer_form.date.data = customer.get_date()
        update_customer_form.status.data = customer.get_status()

        return render_template('updateStatus.html', form=update_customer_form)


@app.route('/viewFeedback/<id>/', methods=['GET', 'POST'])
def view_feedback(id):
    feedback_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedback_dict = db['Feedback']
    db.close()

    feedback_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        if feedback.get_email() == session['id']:
            feedback_list.append(feedback)
        else:
            continue
    return render_template('viewFeedback.html', count=len(feedback_list), feedback_list=feedback_list)


@app.route('/deleteFeedback/<id>', methods=['POST'])
def delete_feedback(id):
    customer_dict = {}
    db = shelve.open('feedback.db', 'w')
    customer_dict = db['Feedback']

    customer_dict.pop(id)

    db['Feedback'] = customer_dict
    db.close()

    return redirect(url_for('manage_feedback'))


@app.route('/noCustomer')
def no_customer():
    return render_template('noCustomer.html')


@app.route('/showCustomer')
def show_customer():
    return render_template('showCustomer.html')
#Joshua

# APP ROUTES FOR LOAN CREATE/RETRIEVE/UPDATE/DELETE
@app.route('/Loan.html')
def loans():
    return render_template('Loan.html')


@app.route('/createLoan.html', methods=['GET', 'POST'])
def create_loan():
    create_loan_form = CreateLoanForm(request.form)
    if request.method == "POST" and create_loan_form.validate():
        loans_dict = {}
        db = shelve.open('Loan.db', 'c')
        print("User successfully saved")
        try:
            loans_dict = db['Loans']
        except:
            print("Error in retrieving Users from user.db.")
        loanentry = Loan.Loan(create_loan_form.first_name.data,
                              create_loan_form.last_name.data,
                              create_loan_form.Amount.data,
                              create_loan_form.Plan.data,
                              create_loan_form.email.data)
        loans_dict[loanentry.get_loan_id()] = loanentry
        db['Loans'] = loans_dict
        db.close()
        print("user saved with {0} as Loan Id".format(loanentry.get_loan_id()))
        return redirect(url_for('retrieve_loans'))
    return render_template('createLoan.html', form=create_loan_form)


@app.route('/retrieveLoan.html')
def retrieve_loans():
    loans_dict = {}
    db = shelve.open('Loan.db', 'r')
    loans_dict = db['Loans']
    db.close()

    loans_list = []
    for key in loans_dict:
        loan = loans_dict.get(key)
        loans_list.append(loan)

    return render_template('retrieveLoan.html', count=len(loans_list), loans_lists=loans_list)


@app.route('/updateLoan.html/<int:id>/', methods=['GET', 'POST'])
def update_Loan(id):
    update_loan_form = CreateLoanForm(request.form)
    if request.method == 'POST' and update_loan_form.validate():
        loans_dict = {}
        db = shelve.open('Loan.db', 'w')
        loans_dict = db['Loans']

        loan = loans_dict.get(id)
        loan.set_loan_name1(update_loan_form.first_name.data)
        loan.set_loan_name2(update_loan_form.last_name.data)
        loan.set_loan_amount(update_loan_form.Amount.data)
        loan.set_loan_plan(update_loan_form.Plan.data)
        loan.set_loan_email(update_loan_form.email.data)

        db['Loans'] = loans_dict
        db.close()

        return redirect(url_for('retrieve_loans'))
    else:
        loans_dict = {}
        db = shelve.open('Loan.db', 'r')
        loans_dict = db['Loans']
        db.close()

        loan = loans_dict.get(id)
        update_loan_form.first_name.data = loan.get_loan_first()
        update_loan_form.last_name.data = loan.get_loan_last()
        update_loan_form.Amount.data = loan.get_loan_amount()
        update_loan_form.Plan.data = loan.get_loan_plan()

        return render_template('updateLoan.html', form=update_loan_form)


@app.route('/deleteLoan/<int:id>', methods=['POST'])
def delete_loan(id):
    loans_dict = {}
    db = shelve.open('Loan.db', 'w')
    loans_dict = db['Loans']

    loans_dict.pop(id)

    db['Loans'] = loans_dict
    db.close()

    return redirect(url_for('retrieve_Loans'))
# END OF LOAN INIT


if __name__ == '__main__':
    app.run()
    FLASK_DEBUG=True
