from flask import Flask, request, render_template,flash
from flask_sqlalchemy import SQLAlchemy
from survivepredict import if_survive

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///titanicsurvive.db'
db = SQLAlchemy()
app.secret_key = 'vai shen patrons'

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(255))
    pclass = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    age = db.Column(db.String(255))
    sibsp = db.Column(db.String(255))
    parch = db.Column(db.String(255))
    embarked = db.Column(db.String(255))

    def __init__(self, result, pclass, sex, age, sibsp, parch, embarked):
        self.result = result
        self.pclass = pclass
        self.sex = sex
        self.age = age
        self.sibsp = sibsp
        self.parch = parch
        self.embarked = embarked

db.init_app(app)

@app.route('/')
def index():
    flash('Luka Vardanidze\n'
          'Demetre Mikaberidze\n'
          'Data Tchanukvadze')
    return render_template('index.html')

@app.route('/qartpred', methods=['GET', 'POST'])
def qartpred():
    if request.method == 'POST':
        pclass = request.form.get('pclass')
        sex = request.form.get('sex')
        age = request.form.get('age')
        sibling_on_board = request.form.get('sibsp')
        parents_on_board = request.form.get('parch')
        embarked = request.form.get('embarked')

        if not all([pclass, sex, age, sibling_on_board, parents_on_board, embarked]):
            return render_template('qartpred.html', res='Invalid input')

        try:
            age = float(age)
            sibling_on_board = float(sibling_on_board)
            parents_on_board = float(parents_on_board)
        except ValueError:
            return render_template('qartpred.html', res='Invalid input')

        res = if_survive(pclass=pclass, sex=sex, age=age, sibsp=sibling_on_board, parch=parents_on_board, embarked=embarked)

        prediction = Prediction(pclass=pclass, sex=sex, age=age, sibsp=sibling_on_board, parch=parents_on_board, embarked=embarked, result=res)
        db.session.add(prediction)
        db.session.commit()
        if res == "Congratulations, you've just won a one-way trip to the 'Resting in Pieces' resort!":
            res ='ბეწვზე გადარჩი '
        else:
            res = 'ნათელი სანთელი'
        return render_template('qartpred.html', res=res)

    return render_template('qartpred.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        pclass = request.form.get('pclass')
        sex = request.form.get('sex')
        age = request.form.get('age')
        sibling_on_board = request.form.get('sibsp')
        parents_on_board = request.form.get('parch')
        embarked = request.form.get('embarked')

        if not all([pclass, sex, age, sibling_on_board, parents_on_board, embarked]):
            return render_template('predict.html', res='Invalid input')

        try:
            age = float(age)
            sibling_on_board = float(sibling_on_board)
            parents_on_board = float(parents_on_board)
        except ValueError:
            return render_template('predict.html', res='Invalid input')

        res = if_survive(pclass=pclass, sex=sex, age=age, sibsp=sibling_on_board, parch=parents_on_board, embarked=embarked)

        prediction = Prediction(pclass=pclass, sex=sex, age=age, sibsp=sibling_on_board, parch=parents_on_board, embarked=embarked, result=res)
        db.session.add(prediction)
        db.session.commit()

        return render_template('predict.html', res=res)

    return render_template('predict.html')

@app.route('/facts')
def facts():
    return render_template('facts.html')

@app.route('/game')
def game():
    return render_template('game.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
