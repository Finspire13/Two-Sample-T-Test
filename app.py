from flask import Flask, request, render_template

app = Flask(__name__)

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