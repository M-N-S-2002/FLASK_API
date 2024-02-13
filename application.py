from flask import Flask,request
app=Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/flaskapi"
db = SQLAlchemy(app)


class Drink(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), unique=True,nullable=False)
    description=db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"



@app.route('/')
def index():
    return "Hello"

@app.route('/drinks')
def get_drinks():
    drinks=Drink.query.all()

    output=[]
    for drink in drinks:
        drink_data={'name':drink.name,'description': drink.description}
        output.append(drink_data)
    
    return {"drinks":output}

@app.route('/drinks/<int:id>')
def get_drinks_by_id(id):
    drinks=Drink.query.get_or_404(id)

    return {"name":drinks.name,"description":drinks.description}

@app.route('/drinks',methods=['POST'])
def add_drink():
    new_drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(new_drink) 
    db.session.commit()  
    return {'id': new_drink.id}  



@app.route('/drinks/<int:id>',methods=['DELETE'])
def delete_drink(id):
    drink=Drink.query.get(id)
    if drink is None:
        return {"drink":"Not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message":"Successfully deleted the drink"}

@app.route('/drinks/<string:name>',methods=['GET'])
def get_drink_by_name(name):
    drink=Drink.query.filter_by(name=name).first()
    if drink is None:
        return {"drink":"Not found"}
    return {"name": drink.name, "description": drink.description}

@app.route('/drinks/<int:id>',methods=['PUT'])
def update_drinks(id):
    drink=Drink.query.get(id)

    if drink is None:
        return {"drink":"Not found"}
    
    if 'name' in request.json:
        drink.name=request.json['name']
    if 'description' in request.json:
        drink.description=request.json['description']
    db.session.commit()

    return {"message":"Updated the drink","name":drink.name,"description":drink.description}