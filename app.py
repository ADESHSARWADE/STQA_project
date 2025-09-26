import os
import re
import gspread
import json
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-hard-to-guess-string-for-local-dev')
csrf = CSRFProtect(app)

def get_google_sheet():
    encoded_creds = os.environ.get('GSPREAD_SERVICE_ACCOUNT_KEY_B64')
    if not encoded_creds:
        raise Exception("GSPREAD_SERVICE_ACCOUNT_KEY_B64 environment variable not set.")
    decoded_creds = base64.b64decode(encoded_creds)
    creds_json = json.loads(decoded_creds)
    gc = gspread.service_account_from_dict(creds_json)
    spreadsheet = gc.open("Students_data") 
    return spreadsheet.sheet1

class SearchForm(FlaskForm):
    enrollment_no = StringField(
        'Enrollment Number', 
        validators=[
            DataRequired(),
            Length(min=13, max=13, message="Please enter a valid 13-digit enrollment number.")
        ]
    )
    submit = SubmitField('Search')

# MODIFIED: The home route now uses flash messaging
@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    # If the form is submitted and is valid...
    if form.validate_on_submit():
        enrollment_no_str = form.enrollment_no.data.strip()
        # ... (The entire success logic for finding a student remains the same)
        try:
            worksheet = get_google_sheet()
            all_students = worksheet.get_all_records()
            student_found = None
            for student in all_students:
                keys_to_check = ['enrollment_no', 'Enrollment No', 'enrollment']
                enrollment_value_from_sheet = None
                for key in keys_to_check:
                    if key in student:
                        enrollment_value_from_sheet = str(student[key])
                        break
                if enrollment_value_from_sheet and enrollment_value_from_sheet == enrollment_no_str:
                    student_found = student
                    break
            
            if student_found:
                student_data_dict = {k: v for k, v in student_found.items() if v != ''}
                return render_template('results.html', student_data=student_data_dict, error=None)
            else:
                flash(f"No student found with Enrollment No: {enrollment_no_str}", 'danger')
                return redirect(url_for('home'))

        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')
            return redirect(url_for('home'))

    # If the form submission is invalid (e.g., not 13 digits)
    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                # Flash each validation error with the 'danger' category
                flash(error, 'danger')
        return redirect(url_for('home'))

    # If it's a GET request, just show the page
    return render_template('home.html', form=form)


if __name__ == '__main__':
    DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=DEBUG_MODE)