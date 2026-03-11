# TODO - Start a basic website, with inheritance, and webpages
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

def remove_white_background(input_path, output_path, threshold=240):
    img=Image.open(input_path).convert("RGBA")
    data=img.getdata()
    new_data = []
    for r,g,b,a in data:
        if r>threshold and g>threshold and b>threshold:
            new_data.append((r,g,b,0))
        else:
            new_data.append((r,g,b,a))
    img.putdata(new_data)
    img.save(output_path, "PNG")
remove_white_background("static/images/cafe-drawing.png", "static/images/cafe-drawing-transparent.png")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ofkapkkkk'
bootstrap = Bootstrap5(app)
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    has_toilet = BooleanField('Toilets?')
    has_wifi = BooleanField('WiFi?')
    has_sockets= BooleanField('Sockets?')
    can_take_calls = BooleanField('Can Take Calls?')
    coffee_price = StringField('Coffee Price')
    submit=SubmitField('Add Cafe')
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template('index.html', cafes=all_cafes)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form=CafeForm()
    if form.validate_on_submit():
        new_cafe=Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect('/')
    return render_template('add.html', form=form)

@app.route('/delete/<int:cafe_id>')
def delete(cafe_id):
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
# TODO - Go through the DAY 66 for RESTful APIs
# TODO - Day 63 for SQLAlchemy
if __name__ == "__main__":
    app.run(debug=True, port=5001)