from wtforms import Form, StringField, validators, PasswordField, SelectField, ValidationError, TextAreaField
from wtforms.fields import EmailField, DateField, FileField, IntegerField, RadioField, SearchField
from flask_wtf.recaptcha import RecaptchaField


class LoginForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired()])


class CreateCustomerForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    phone = StringField('Phone', [validators.Length(min=8, max=8), validators.DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired(),
                                          validators.EqualTo('confirmpassword', message='Error:Passwords must match')])
    confirmpassword = PasswordField('Confirm Password', [validators.DataRequired()])


    def validate_phone(self, phone):
        if not phone.data[1:8].isdigit():
            raise ValidationError("Phone number must not contain letters")


class SearchCustomerForm(Form):
    searchCustomer = StringField('Search Customer', [validators.DataRequired()])


class UpdateCustomerForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    phone = StringField('Phone', [validators.Length(min=8, max=8), validators.DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])


    def validate_phone(self, phone):
        if not phone.data[1:8].isdigit():
            raise ValidationError("Phone number must not contain letters")


class FeedbackForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()])
    service = SelectField('Rate our Service', [validators.DataRequired()],
                          choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                          default='')
    website = SelectField('Rate our Website', [validators.DataRequired()],
                          choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                          default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    additional = TextAreaField('Additional feedback')


class UpdateCustomerForm2(Form):
    password = PasswordField('Password', [validators.Length(min=10, max=150), validators.DataRequired(),
                                          validators.EqualTo('confirmpassword', message='Error:Passwords must match')])
    confirmpassword = PasswordField('Confirm Password', [validators.DataRequired()])


class UpdateStatus(Form):
    name = StringField('Name', [validators.Length(min=3, max=150), validators.DataRequired()],
                       render_kw={'readonly': True})
    service = SelectField('Rate our Service', [validators.DataRequired()],
                          choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                          default='', render_kw={'readonly': True})
    website = SelectField('Rate our Website', [validators.DataRequired()],
                          choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                          default='', render_kw={'readonly': True})
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={'readonly': True})
    additional = TextAreaField('Additional feedback', render_kw={'readonly': True})
    date = DateField('Date of Creation', format='%Y-%m-%d', render_kw={'readonly': True})
    status = SelectField('Status', [validators.DataRequired()],
                         choices=[('Processing', 'Processing'), ('Processed', 'Processed')],
                         default='Processing')


class ForgetPassword(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])


class OTPform(Form):
    otp = StringField('OTP', [validators.DataRequired()])


class ChangePassword(Form):
    password = PasswordField('Password', [validators.EqualTo('confirmpassword', message='Error:Passwords must match')])
    confirmpassword = PasswordField('Confirm Password')


# START OF LOAN FORMS

class CreateLoanForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    Amount = IntegerField('Amount $', [validators.NumberRange(min=1, max=999999), validators.DataRequired()])
    Plan = RadioField('Loan Plan:', choices=[('S', 'Silver'), ('G', 'Gold'), ('P', 'Platinum'), ('D', 'Diamond')],
                      default='S')
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])


class CreatePlanForm(Form):
    Plan_name = StringField('Plan Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    Plan_Des = StringField('Plan Description', [validators.Length(min=1, max=300), validators.DataRequired()])
    Plan_interest = IntegerField('Interest', [validators.NumberRange(min=1, max=100), validators.DataRequired()])
    Plan_image = FileField('Plan Image', [validators.DataRequired()])


class SearchLoanForm(Form):
    Loan_search = SearchField('Enter Loan Id', [validators.Length(min=1, max=7), validators.DataRequired])

# END OF LOAN FORMS
