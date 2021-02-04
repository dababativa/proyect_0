from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project0.db'

db = SQLAlchemy(app)



### Utils ###
def array_to_dict(arr):
    dict_arr = []
    for element in arr:
        dict_arr.append(element.to_dict())
    return dict_arr

def success(body):
    return {"message": "Success", "body": body}


### Models ### 
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    fk_category = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    virtual_event = db.Column(db.Boolean, nullable=False)
    fk_organizer = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return "Event: {} - {} - {}".format(self.id, self.name, self.fk_organizer)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "fk_category": self.fk_category,
            "location": self.location,
            "address": self.address,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "virtual_event": self.virtual_event,
            "fk_organizer": self.fk_organizer,
            "create_date": self.create_date
        }

class EventCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "Category: {} - {}".format(self.id, self.name)

    def to_dict(self):
        return {"id": self.id, "name":self.name}
        


class User(db.Model):
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), primary_key=True)
    is_active = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "User: {} {} - {}".format(self.first_name, self.last_name, self.email)

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "password": self.password,
        }

### Router ###

@app.route('/')
def index():
    return "Salu2"


@app.route('/event', methods=["GET", "POST", "PUT", "DELETE"])
def event_handler():
    if request.method == "GET":
        fk_organizer = request.args.get("fk_organizer")
        print(fk_organizer)
        events = Event.query.order_by(Event.create_date.desc()).filter(Event.fk_organizer==fk_organizer).all()
        events = array_to_dict(events)
        print(success(events))
        return success(events)

    if request.method == "POST":
        body = request.form
        print(body)
        name = body.get("name")
        fk_category= int(body.get("fk_category"))
        location = body.get("location")
        address = body.get("address")
        start_date_str = body.get("start_date")
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') 
        end_date_str = body.get("end_date")
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') 
        virtual_event = bool( body.get("virtual_event"))
        fk_organizer = body.get("fk_organizer")
        print(type(end_date))

        new_event = Event(name=name, fk_category=fk_category,
        location=location, address=address, start_date=start_date, end_date=end_date,
        virtual_event=virtual_event, fk_organizer=fk_organizer)
        try:
            db.session.add(new_event)
            db.session.commit()
            return 'Succesfully created event'
        except:
            return "There was an error whilst creating the event"

    if request.method == "PUT":
        body = request.form
        id = body.get("id")
        start_date_str = body.get("start_date")
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') 
        end_date_str = body.get("end_date")
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') 
        event_to_update = Event.query.get_or_404(id)
        event_to_update.name = body.get("name")
        event_to_update.fk_category = body.get("fk_category")
        event_to_update.location = body.get("location")
        event_to_update.address = body.get("address")
        event_to_update.start_date = start_date
        event_to_update.end_date = end_date
        event_to_update.virtual_event = bool(body.get("virtual"))
        event_to_update.fk_organizer = body.get("fk_organizer")
        try:
            db.session.commit()
            return success("Updated event {} successfully".format(id))
        except:
            return "Couldn't update the event"
        

    if request.method == "DELETE":
        body = request.form
        id = body.get("id")
        event_to_delete = Event.query.get_or_404(id)
        try:
            db.session.delete(event_to_delete)
            db.session.commit()
            return "Event with id {} deleted succesfully".format(id)
        except: 
            return "Error whilst deleting the event"

@app.route("/category", methods=["GET", "POST"])
def category_handler():
    if request.method == "GET":
        categories = EventCategory.query.all()
        print(categories)
        categories = array_to_dict(categories)
        print(categories, "YA SOY DICT")
        return success(categories)

    if request.method == "POST":
        body = request.form
        print(body)
        name = body.get("name")
        print(name)
        new_category = EventCategory(name=name)
        try:
            db.session.add(new_category)
            print("pre commit")
            db.session.commit()
            print("pot")
            return 'Succesfully created a category'
        except:
            return "Whoops I'm a teapot"


@app.route("/user", methods=["GET", "POST"])
def user_handler():
    if request.method == "GET":
        users = User.query.all()
        users = array_to_dict(users)
        return success(users)

    if request.method == "POST":
        body = request.form
        first_name = body.get("first_name")
        last_name = body.get("last_name")
        password = body.get("password")
        email = body.get("email")
        is_admin = bool(body.get("is_admin"))

        new_user = User(
            first_name=first_name, 
            last_name=last_name,
            email = email,
            password = password,
            is_active = True,
            is_admin = is_admin
            )
        try:
            db.session.add(new_user)
            db.session.commit()
            return success('Succesfully created user')
        except:
            return "Whoops I'm a teapot"

@app.route("/activate-user", methods=["GET"])
def activate_user():
    email = request.args.get("email")
    user = User.query.get_or_404(email)
    user.is_active = True
    try:
        db.session.commit()
        return "User {} is now active".format(user.email)
    except:
        return "mega teapot, why am I here?"
    
@app.route("/login", methods=["POST"])
def login():
    print(request.form)
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.get_or_404(email)
    if(user.is_active):
        if(password == user.password):
            return success("success")
        else:
            return "Wrong password"
    else:
        return "Inactive user, please confirm your email address first"



if __name__ == "__main__":
    app.run(debug=True)  
        

