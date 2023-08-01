import json
from flask import Flask, Response, render_template, request,session     
from storage import names_list
from wtforms import TextField, Form
from rec_ml import recommend



app = Flask(__name__)
app.secret_key = 'gofight'



class SearchForm(Form):
    autocomp = TextField('Insert name', id='name_autocomplete')


@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(names_list()), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        game_name = request.form.get('game_name')
        if game_name:
            session['last_input'] = game_name
        game_count = request.form.get('game_count')
        list_of_games = recommend(game_name, int(game_count))
        form = SearchForm(request.form)
        last = session.get('last_input')
        return render_template("index.html", form=form, list_of_games=list_of_games,last=last)

    form = SearchForm(request.form)
    
    return render_template("index.html", form=form,)
if __name__ == '__main__':
    app.run(debug=True)
