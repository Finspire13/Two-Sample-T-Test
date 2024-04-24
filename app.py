from flask import Flask, request, render_template
import os
from flask import url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Sample(db.Model):
    sample_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Sample {self.sample_id}>'




numbers = []
genders = []

@app.route('/', methods=["GET","POST"])
def index():

    if request.method == "POST":
        number = str(request.form['wkp-time'])
        gender = str(request.form['gender'])
        numbers.append(number)
        genders.append(gender)

    output = ''
    for i in range(len(numbers)):
        output += f'{numbers[i]}, {genders[i]}\n'

    return render_template('index.html', output=output)


# @app.route('/submit', methods=['POST'])
# def submit():

#     return 'Submitted Successfully!'

# @app.route('/result')
# def result():
#     return_text = ''
#     for i in range(len(numbers)):
#         return_text += f'{numbers[i]}, {genders[i]}\n'
#     return return_text

@app.route('/reset')
def reset():
    numbers = []
    genders = []
    return 'Reset Successfully!'

if __name__ == '__main__':
    app.run(debug=True)