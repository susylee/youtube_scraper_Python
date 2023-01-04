from flask import render_template, redirect
from app import app
from app.forms import SearchForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect('/results')
    print(search_form.errors    )
    return render_template('index.html', form=search_form)

@app.route('/results')
def results():
    return render_template('results.html')


