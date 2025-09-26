import os
import re
import gspread # New import
import json # New import
import base64 # New import
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-hard-to-guess-string-for-local-dev')
csrf = CSRFProtect(app)

# --- NEW: Google Sheets Authentication ---
def get_google_sheet():
    """Connects to Google Sheets using credentials from environment variables."""
    # Get the Base64 encoded JSON key from environment variables
    encoded_creds = os.environ.get('GSPREAD_SERVICE_ACCOUNT_KEY_B64')
    if not encoded_creds:
        raise Exception("GSPREAD_SERVICE_ACCOUNT_KEY_B64 environment variable not set.")

    # Decode the Base64 string back into JSON
    decoded_creds = base64.b64decode(encoded_creds)
    creds_json = json.loads(decoded_creds)

    # Authenticate and return the client
    gc = gspread.service_account_from_dict(creds_json)
    # IMPORTANT: Replace 'YourSpreadsheetName' with the exact name of your Google Sheet
    spreadsheet = gc.open("Students_data") 
    return spreadsheet.sheet1 # Return the first sheet

class SearchForm(FlaskForm):
    enrollment_no = StringField('Enrollment Number', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        # MODIFIED: Trim whitespace from the user's input for a cleaner search
        enrollment_no_str = form.enrollment_no.data.strip()
        student_data_dict = None
        error_message = None

        try:
            worksheet = get_google_sheet()
            all_students = worksheet.get_all_records()
            
            student_found = None
            for student in all_students:
                # MODIFIED: This loop now checks for multiple common key names and is case-insensitive
                # This makes your app much more flexible to changes in the Google Sheet
                keys_to_check = ['enrollment_no', 'Enrollment No', 'enrollment']
                enrollment_value_from_sheet = None
                
                for key in keys_to_check:
                    if key in student:
                        enrollment_value_from_sheet = str(student[key])
                        break # Stop checking once a key is found
                
                if enrollment_value_from_sheet and enrollment_value_from_sheet == enrollment_no_str:
                    student_found = student
                    break
            
            if student_found:
                student_data_dict = {k: v for k, v in student_found.items() if v != ''}
            else:
                error_message = f"No student found with Enrollment No: {enrollment_no_str}"

        except gspread.exceptions.SpreadsheetNotFound:
             error_message = "Error: The Google Sheet was not found. Check the name and sharing settings."
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"

        return render_template('results.html', student_data=student_data_dict, error=error_message)
    
    return render_template('home.html', form=form)

if __name__ == '__main__':
    DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=DEBUG_MODE)