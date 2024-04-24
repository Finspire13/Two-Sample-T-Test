from flask import Flask, request, render_template
import os
from flask import url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vseryxnppudcar:9b8024182a9e9b69cf2cf7ea5da8446142c4a83219cf6f9d358e50742f9af8fc@ec2-44-206-204-65.compute-1.amazonaws.com:5432/da5jm4vashv4et'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Sample {self.id}>'

@app.route('/', methods=["GET","POST"])
def index():

    if request.method == "POST":
        time = str(request.form['wkp-time'])
        gender = str(request.form['gender'])
        sample = Sample(time=time, gender=gender)
        db.session.add(sample)
        db.session.commit()

    all_samples = Sample.query.all()
    output = str(all_samples)
    print(all_samples)

    # output = ''
    # for i in range(len(numbers)):
    #     output += f'{numbers[i]}, {genders[i]}\n'

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
    db.drop_all()
    db.create_all()
    db.session.commit()
    return 'Reset Successfully!'

if __name__ == '__main__':
    app.run(debug=True)