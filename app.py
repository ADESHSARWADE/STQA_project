import os
import re
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-hard-to-guess-string-for-local-dev')
csrf = CSRFProtect(app)

STUDENT_DATA_FILE = 'students.xlsx'

class SearchForm(FlaskForm):
    enrollment_no = StringField(
        'Enrollment Number', 
        validators=[
            DataRequired(message="Please enter an enrollment number."),
            Length(min=10, max=15, message="Enrollment number must be between 10 and 15 characters.")
        ]
    )
    submit = SubmitField('Search')

def find_enrollment_column(df):
    possible_keywords = ['enrollment', 'enrolment', 'enrol', 'enroll']
    for col in df.columns:
        clean_col = re.sub(r'[\s_]', '', col.lower())
        if any(keyword in clean_col for keyword in possible_keywords):
            return col
    return None

# MODIFIED: The home route now handles both displaying the form and showing the results
@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    
    # This logic runs ONLY when the form is submitted and is valid
    if form.validate_on_submit():
        enrollment_no_str = form.enrollment_no.data
        student_data_dict = None
        error_message = None

        try:
            df = pd.read_excel(STUDENT_DATA_FILE)
            enrollment_col_name = find_enrollment_column(df)
            
            if not enrollment_col_name:
                raise KeyError("Could not automatically find an 'Enrollment No' column in the Excel file.")
            
            df[enrollment_col_name] = df[enrollment_col_name].astype(str)
            student_series = df.loc[df[enrollment_col_name] == enrollment_no_str].iloc[0]
            student_series_cleaned = student_series.dropna()
            student_data_dict = student_series_cleaned.to_dict()

        except FileNotFoundError:
            error_message = f"Error: The data file '{STUDENT_DATA_FILE}' was not found."
        except KeyError as e:
            error_message = f"Error: {e}"
        except IndexError:
            error_message = f"No student found with Enrollment No: {enrollment_no_str}"
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"

        # Instead of redirecting, render the results template directly
        return render_template('results.html', student_data=student_data_dict, error=error_message)

    # If it's a GET request or the form is invalid, show the home page with the search form
    return render_template('home.html', form=form)

if __name__ == '__main__':
    DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=DEBUG_MODE)