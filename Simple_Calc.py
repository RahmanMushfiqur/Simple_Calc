from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")

@app.route('/calc', methods=["GET", "POST"])
def calm():
    
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == "POST":
        try:
            a = int(request.form.get('first_number'))
            b = int(request.form.get('second_number'))
            c = request.form.get('sign')
        except ValueError:
            return "Not a number, try again!", 400
        if c == '+':
            result = a + b
        elif c == '-':
            result = a - b
        elif c == '*':
            result = a * b
        elif c == '/':
            if b == 0:
                return "Cant divide by zero!"
            else:
                result = a / b

        return str(result)
        
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)