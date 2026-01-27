from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder="templates")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Integer, nullable=False)
    b = db.Column(db.Integer, nullable=False)
    sign = db.Column(db.String(1), nullable=False)
    result = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Calculation {self.id}: {self.a}{self.sign}{self.b}={self.result}>"

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            a = int(request.form.get('first_number'))
            b = int(request.form.get('second_number'))
            sign = request.form.get('sign')
        except ValueError:
            return "Not a number, try again!", 400
        
        sign = (request.form.get('sign'))
        
        if sign == '+':
            result = a + b
        elif sign == '-':
            result = a - b
        elif sign == '*':
            result = a * b
        elif sign == '/':
            if b == 0:            
                history = Calculation.query.order_by(Calculation.created.desc()).limit(10).all()
                return render_template("index.html", error="Can't divide by zero", history=history)
            else:
                result = a / b
        
        row = Calculation(a=a, b=b, sign=sign, result=result)
        db.session.add(row)
        db.session.commit()

        history = Calculation.query.order_by(Calculation.created.desc()).limit(10).all()
        return render_template("index.html", result=result, history=history)

    history = Calculation.query.order_by(Calculation.created.desc()).limit(10).all()
    return render_template("index.html", history=history)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
