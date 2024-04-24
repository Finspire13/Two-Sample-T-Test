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
    # if len(numbers) < 10:
    #     return 'Not enough data yet!'
    # else:
    #     avg = sum(numbers) / len(numbers)
    #     return f'The average value is: {avg}'
    return f'{str(numbers)}, {str(genders)}'


@app.route('/reset')
def reset():
    numbers.clear()
    genders.clear()
    return 'Reset Successfully!'

if __name__ == '__main__':
    app.run(debug=True)