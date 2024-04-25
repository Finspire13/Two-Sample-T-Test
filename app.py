from flask import Flask, request, render_template
import os
from flask import url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import numpy as np
from scipy.stats import ttest_ind

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# 'postgres://ygzfzfiokzvpky:73247d53a2bef12c9a8f20e8f039ff07dd81b7217c76e900a8aaa3399f54d6eb@ec2-52-20-188-247.compute-1.amazonaws.com:5432/ddnf73h9ceb9ct'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"


db = SQLAlchemy(app)

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Sample {self.id}>'

def convert_time(time):
    hour, minute = time.split(':')
    return float(hour) + float(minute) / 60

@app.route('/', methods=["GET","POST"])
def index():

    if request.method == "POST":
        time = str(request.form['wkp-time'])
        gender = str(request.form['gender'])
        sample = Sample(time=time, gender=gender)
        db.session.add(sample)
        db.session.commit()

    all_samples = Sample.query.all()

    sample1 = [convert_time(i.time) for i in all_samples if i.gender == 'female']
    sample2 = [convert_time(i.time) for i in all_samples if i.gender == 'male']
    sample3 = [convert_time(i.time) for i in all_samples if i.gender == 'nonbinary']



    if len(sample1) > 1:
        dsp_line1 = f'Female - Mean: {np.mean(sample1):.2f}, Std: {np.std(sample1):.3f}, Number: {len(sample1)}'
    else:
        dsp_line1 = f'Female - Mean: {np.mean(sample1)}, Std: {np.std(sample1)}, Number: {len(sample1)}'

    if len(sample2) > 1:
        dsp_line2 = f'Male - Mean: {np.mean(sample2):.2f}, Std: {np.std(sample2):.3f}, Number: {len(sample2)}'
    else:
        dsp_line2 = f'Male - Mean: {np.mean(sample2)}, Std: {np.std(sample2)}, Number: {len(sample2)}'

    if len(sample3) > 1:
        dsp_line3 = f'Non-Binary - Mean: {np.mean(sample3):.2f}, Std: {np.std(sample3):.3f}, Number: {len(sample3)}'
    else:
        dsp_line3 = f'Non-Binary - Mean: {np.mean(sample3)}, Std: {np.std(sample3)}, Number: {len(sample3)}'

    if len(sample1) > 1 and len(sample2) > 1:
        pv12 = ttest_ind(sample1, sample2, equal_var=False).pvalue
        dsp_line4 = f'P-Value: {pv12:.6f} (Female vs. Male)'
    else:
        dsp_line4 = f'P-Value: No enough data (Female vs. Male)'

    if len(sample1) > 1 and len(sample3) > 1:
        pv13 = ttest_ind(sample1, sample3, equal_var=False).pvalue
        dsp_line5 = f'P-Value: {pv13:.6f} (Female vs. Non-Binary)'
    else:
        dsp_line5 = f'P-Value: No enough data (Female vs. Non-Binary)'

    if len(sample2) > 1 and len(sample3) > 1:
        pv23 = ttest_ind(sample2, sample3, equal_var=False).pvalue
        dsp_line6 = f'P-Value: {pv23:.6f} (Male vs. Non-Binary)'
    else:
        dsp_line6 = f'P-Value: No enough data (Male vs. Non-Binary)'

    # output = str(all_samples)
    # print(all_samples)

    # output = ''
    # for i in range(len(numbers)):
    #     output += f'{numbers[i]}, {genders[i]}\n'

    return render_template('index.html', all_lines_1=[dsp_line1, dsp_line2, dsp_line3], all_lines_2=[dsp_line4, dsp_line5, dsp_line6])


# @app.route('/submit', methods=['POST'])
# def submit():

#     return 'Submitted Successfully!'

# @app.route('/result')
# def result():
#     return_text = ''
#     for i in range(len(numbers)):
#         return_text += f'{numbers[i]}, {genders[i]}\n'
#     return return_text

@app.route('/reset_secure')
def reset_secure():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return 'Reset Successfully!'

if __name__ == '__main__':
    app.run(debug=True)