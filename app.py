from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///operations.db'
db = SQLAlchemy(app)

# Model for storing operations
class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operand1 = db.Column(db.Float, nullable=False)  # Ensure this matches your needs
    operand2 = db.Column(db.Float, nullable=False)
    operator = db.Column(db.String(5), nullable=False)
    result = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')  # Home page with form and result

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        operand1 = float(data.get('operand1'))  # Get the first number from input
        operand2 = float(data.get('operand2'))  # Get the second number from input
        operator = data.get('operator')  # Get the operator

        # Perform calculation based on operator
        if operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        elif operator == '*':
            result = operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                return jsonify({'error': 'Division by zero is not allowed'})
            result = operand1 / operand2
        else:
            return jsonify({'error': 'Invalid operator'})

        # Save to database
        new_operation = Operation(operand1=operand1, operand2=operand2, operator=operator, result=result)
        db.session.add(new_operation)
        db.session.commit()

        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/history')
def history():
    operations = Operation.query.all()
    return render_template('history.html', operations=operations)  # Show previous calculations

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
