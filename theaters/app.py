from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pdb
from sqlalchemy import or_


 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class City(db.Model):
    """
    Describe Model here
    """
  
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), index=True, unique=True)
    theaters = db.relationship('Theater', backref='city', lazy='dynamic')
   
    def __repr__(self):
        return '<City {}>'.format(self.city)


class Theater(db.Model):
    """
    Describe Model here
    """
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(120), index=True, unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    description = db.Column(db.String(128))
    performances = db.relationship('Performance', backref='theater', lazy='dynamic')
    
    
    def __repr__(self):
        return '<Theater {}>'.format(self.name)

class Performance(db.Model):
    """
    Describe Model here
    """
        
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140),  index=True, unique=True)
    times = db.Column(db.String(60))
    price = db.Column(db.Integer)
    description = db.Column(db.String(256))
    main_actors = db.Column(db.String(126))
    genres = db.relationship('Genre', backref='performance', lazy='dynamic')
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))

    def __repr__(self):
        return '<Performance {}>'.format(self.name)
    
class Genre(db.Model):
    """
    Describe Model here
    """
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True)
    performance_id = db.Column(db.Integer, db.ForeignKey('performance.id'))
    
    def __repr__(self):
        return '<Genre {}>'.format(self.name)

@app.route('/city', methods=["GET", "POST"])
def city():
    city = None
    
    if request.method == 'POST':
        try:
            city = City(city=request.form.get("city"))
            db.session.add(city)
            db.session.commit()
        except Exception as e:
            print("Failed to add city")
            print(e)
        finally:
            cities = City.query.all()
    elif request.method == 'GET':
        search = request.args.get("search", '')
#         pdb.set_trace()
        cities = City.query.filter(
            or_(
             (City.id.like('%' + search + '%')),
                 (City.city.like('%' + search + '%'))))
    else:
        pass
    
    return render_template("city.html", cities=cities)


@app.route("/update_city", methods=["POST"])
def update_city():
    new_city = request.form.get("new_city")
    old_city = request.form.get("old_city")
    city = City.query.filter_by(city=old_city).first()
    city.city = new_city
    db.session.commit()
    return redirect("/city")

@app.route("/delete_city", methods=["POST"])
def delete_city():
    id = request.form.get("id")
    c = City.query.filter_by(id=id).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/city")


@app.route('/theater', methods=["GET", "POST"])
def theater():
    theater = None
    if request.form:
        try:
            
            theater = Theater(name=request.form.get("name"), 
                              address=request.form.get("address"), 
                              city_id=request.form.get("city_id"), 
                              description=request.form.get("description"))
            db.session.add(theater)
            db.session.commit()
        except Exception as e:
            print("Failed to add theater")
            print(e)
        finally:
            theaters = Theater.query.all()
    elif request.method == 'GET':
        search = request.args.get("search", '')
#         pdb.set_trace()
        theaters = Theater.query.filter(
            or_( (Theater.id.like('%' + search + '%')),
             (Theater.name.like('%' + search + '%')),
                 (Theater.address.like('%' + search + '%')),
            (Theater.city_id.like('%' + search + '%')),
            (Theater.description.like('%' + search + '%'))))
       
    else:
        pass
    
    cities_id = City.query.all()
    
    return render_template("theater.html", cities_id=cities_id, theaters=theaters)

@app.route("/update_theater", methods=["POST"])
def update_theater():
    new_name = request.form.get("new_name")
    old_name = request.form.get("old_name")
    new_address = request.form.get("new_address")
    old_address = request.form.get("old_address")
    new_city = request.form.get("new_city")
    old_city = request.form.get("old_city")
    new_description = request.form.get("new_description")
    old_description = request.form.get("old_description")
    theater = Theater.query.filter_by(name=old_name, address=old_address, city_id=old_city, description=old_description).first()
    
    theater.name = new_name
    theater.address = new_address
    theater.city_id = new_city
    theater.description = new_description
    db.session.commit()
    return redirect("/theater")

@app.route("/delete_theater", methods=["POST"])
def delete_theater():
 
    id = request.form.get("id")
    theater = Theater.query.filter_by(id=id).first()
    db.session.delete(theater)
    db.session.commit()
    return redirect("/theater")

@app.route('/performance', methods=["GET", "POST"])
def performance():
    performance = None
    if request.form:
        try:
            performance = Performance(name=request.form.get("name"), 
                                      times=request.form.get("times"), 
                                      price=request.form.get("price"), 
                                      description=request.form.get("description"), 
                                      main_actors=request.form.get("main_actors"), 
                                      theater_id=request.form.get("theater_id"))
            db.session.add(performance)
            db.session.commit()
        except Exception as e:
            print("Failed to add performance")
            print(e)
        finally:
            performances = Performance.query.all()
    elif request.method == 'GET':
        search = request.args.get("search", '')
#         pdb.set_trace()
        performances = Performance.query.filter(
            or_( (Performance.id.like('%' + search + '%')),
            (Performance.name.like('%' + search + '%')),
            (Performance.times.like('%' + search + '%')),
            (Performance.price.like('%' + search + '%')),
            (Performance.description.like('%' + search + '%')),
            (Performance.main_actors.like('%' + search + '%')),
            (Performance.theater_id.like('%' + search + '%'))))
       
    else:
        pass
    theaters_id = Theater.query.all()
  
    return render_template("performance.html", theaters_id=theaters_id, performances=performances )



@app.route("/update_performance", methods=["POST"])
def update_performance():
    new_name = request.form.get("new_name")
    old_name = request.form.get("old_name")
    new_times = request.form.get("new_times")
    old_times = request.form.get("old_times")
    new_price = request.form.get("new_price")
    old_price = request.form.get("old_price")
    new_description = request.form.get("new_description")
    old_description = request.form.get("old_description")
    new_main_actors = request.form.get("new_main_actors")
    old_main_actors = request.form.get("old_main_actors")
    new_theater_id = request.form.get("new_theater_id")
    old_theater_id= request.form.get("old_theater_id")
    performance = Performance.query.filter_by(name=old_name, 
                                              times=old_times, 
                                              price=old_price, 
                                              description=old_description, 
                                              main_actors=old_main_actors, 
                                              theater_id=old_theater_id).first()
    
    performance.name = new_name
    performance.times = new_times
    performance.price = new_price
    performance.description = new_description
    performance.main_actors = new_main_actors
    performance.theater_id = new_theater_id
    db.session.commit()
    return redirect("/performance")

@app.route("/delete_performance", methods=["POST"])
def delete_performance():

    id = request.form.get("id")
    performance = Performance.query.filter_by(id=id).first()
    db.session.delete(performance)
    db.session.commit()
    return redirect("/performance")

@app.route('/genre', methods=["GET", "POST"])
def genre():
    genre = None
    if request.form:
        try:
            genre = Genre(name=request.form.get("name"), 
                          performance_id=request.form.get("performance_id"))
            db.session.add(genre)
            db.session.commit()
        except Exception as e:
            print("Failed to add genre")
            print(e)
        finally:
            genres = Genre.query.all()
    elif request.method == 'GET':
        search = request.args.get("search", '')

        #pdb.set_trace()
        genres = Genre.query.filter(
            or_((Genre.id.like('%' + search + '%')),
             (Genre.name.like('%' + search + '%')),
            (Genre.performance_id.like('%' + search + '%'))))
       
    else:
        pass

    performances_id = Performance.query.all()
    return render_template("genre.html",  genres=genres, performances_id=performances_id)


@app.route("/update_genre", methods=["POST"])
def update_genre():
    new_name = request.form.get("new_name")
    old_name = request.form.get("old_name")
    new_performance_id = request.form.get("new_performance_id")
    old_performance_id = request.form.get("old_performance_id")
    genre = Genre.query.filter_by(name=old_name, performance_id=new_performance_id).first()
    genre.name = new_name
    genre.performance_id = new_performance_id
    db.session.commit()
    return redirect("/genre")

@app.route("/delete_genre", methods=["POST"])
def delete_genre():
    id = request.form.get("id")
    genre = Genre.query.filter_by(id=id).first()
    db.session.delete(genre)
    db.session.commit()
    return redirect("/genre")

app.run(host='0.0.0.0', port=5005)
