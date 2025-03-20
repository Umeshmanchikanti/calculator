from flask import Flask, request, render_template

app = Flask(__name__)

def calculate(num1, num2, operation):
    try:
        num1, num2 =float(num1), float(num2)
        if operation == "add":
            return num1 + num2
        elif operation == "subtract":
            return num1 - num2
        elif operation == "multiply":
            return num1 * num2
        elif operation == "divide":
            return num1 / num2 if num2 != 0 else "Error! Division by zero."
        else:
            return "Invalid operation!"
    except ValueError:
        return "Invalid input!"
    
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        num1 = request.form["num1"]
        num2 = request.form["num2"]
        operation = request.form["operation"]
        result = calculate(num1, num2, operation)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)