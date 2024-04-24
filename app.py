from flask import Flask, request, render_template

app = Flask(__name__)

numbers = []
genders = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    number = str(request.form['wkp-time'])
    gender = str(request.form['gender'])
    numbers.append(number)
    genders.append(gender)
    return 'Submitted Successfully!'

@app.route('/result')
def result():
    return_text = ''
    for i in range(len(numbers)):
        return_text += f'{numbers[i]}, {genders[i]}\n'
    return return_text

@app.route('/reset')
def reset():
    numbers = []
    genders = []
    return 'Reset Successfully!'

if __name__ == '__main__':
    app.run(debug=True)