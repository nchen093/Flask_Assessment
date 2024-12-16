from flask import Flask, render_template, redirect
from flask_migrate import Migrate

from .config import Configuration
from .forms import NewInstrument
from .models import db, Instrument

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
Migrate(app, db)

@app.route("/")
def index():
    return render_template("main_page.html")

@app.route("/new_instrument")
def new_instrument():
    form = NewInstrument()
    
    return render_template('simple_form.html', form=form) 

@app.route('/new_instrument', methods=["POST"])
def new_instrument_post():
    form = NewInstrument()

    if form.validate_on_submit():
        new_instrumenton = Instrument()
        form.populate_obj(new_instrumenton)

        db.session.add(new_instrumenton)
        db.session.commit()

        return redirect("/instrument_data")



    #return render_template("simple_form.html", form=form)
    return 'Bad Data'

@app.route('/instrument_data')
def instrument_data():
    m_instrumentons = Instrument.query.filter(Instrument.nickname.like("M%")).all()
    return render_template("simple_form_data.html", instruments=m_instrumentons )

