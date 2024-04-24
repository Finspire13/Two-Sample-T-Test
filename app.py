from flask import Flask, request, render_template

app = Flask(__name__)

numbers = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    number = int(request.form['number'])
    numbers.append(number)
    return 'Number submitted successfully!'

@app.route('/average')
def average():
    if len(numbers) < 10:
        return 'Not enough data yet!'
    else:
        avg = sum(numbers) / len(numbers)
        return f'The average value is: {avg}'

if __name__ == '__main__':
    app.run(debug=True)