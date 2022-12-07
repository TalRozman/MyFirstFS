from flask import Flask,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDb.sqlite3'
db = SQLAlchemy(app)

class Airport(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    terminal = db.Column(db.Integer)
    flight_num = db.Column(db.String,unique = True)
    gate = db.Column(db.Integer)
    std = db.Column(db.String)
    etd = db.Column(db.String)

    def __init__(self,terminal,flight_num,gate,std,etd):
        self.terminal = terminal
        self.flight_num = flight_num
        self.gate = gate
        self.std = std
        self.etd = etd

@app.route('/',methods=["GET","POST"])
@app.route('/<id>',methods=["PUT","DELETE"])
def main(id = 0):
    # get all flights
    if request.method == "GET":
        res = []
        for flight in Airport.query.all():
            res.append({"id":flight.id,"terminal":flight.terminal,"flight_num":flight.flight_num,"gate":flight.gate,"std":flight.std,"etd":flight.etd})
        return json.dumps(res)
    # add a new flight
    elif request.method == "POST":
        flight = request.get_json()
        terminal = flight["terminal"]
        flight_num = flight["flight_num"]
        gate = flight["gate"]
        std = flight["std"]
        etd = flight["std"]
        new_flight = Airport(terminal,flight_num,gate,std,etd)
        db.session.add(new_flight)
        db.session.commit()
        return "New flight added"
    #upadte teminal,gate,etd
    elif request.method == "PUT":
        flight = request.get_json()
        upd_flight = Airport.query.filter_by(id = id).first()
        upd_flight.etd = flight["etd"]
        upd_flight.terminal = flight["terminal"]
        upd_flight.gate = flight["gate"]
        db.session.commit()
        return f"flight {upd_flight.flight_num} updated"
    elif request.method == "DELETE":
        del_me = Airport.query.filter_by(id = id).first()
        db.session.delete(del_me)
        db.session.commit()
        return f"flight {del_me.flight_num} deleted"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)