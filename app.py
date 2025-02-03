from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

# Initialize Flask extensions
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/todo.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath("instance/todo.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['DEBUG'] = True


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # Checking if email is unique
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"Message": "Email already exists"}), 400
        
        new_user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        token = create_access_token(identity=new_user.id)
        return jsonify({"token": token}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/login',methods=["POST"])
def login():
    data=request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and bcrypt.check_password_hash(user.password,data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}),200
    return jsonify({"message":"Invalid Credentials"}),401

@app.route('/todos', methods=["POST"])
@jwt_required()
def create_todo():
    data = request.get_json()
    # if not data.get('title') or not data.get('description'):
    #     return jsonify({"msg": "Title and description are required and must be strings."}), 400
    current_user_id = get_jwt_identity()

    new_todo = Todo(
        title=data['title'],
        description=data['description'],
        user_id=current_user_id
    )
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"id": new_todo.id, "title": new_todo.title, "description": new_todo.description}), 201


@app.route('/todos/<int:todo_id>',methods=["PUT"])
@jwt_required() 
def update_todo(todo_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    todo = Todo.query.get(todo_id)

    if todo.user_id != current_user_id:
        return jsonify({"message": "Forbidden"}),403
    
    todo.title = data.get('title',todo.title) 
    todo.description = data.get('description',todo.description)
    db.session.commit()

    return jsonify({"id":todo.id,"title":todo.title,"description":todo.description}),200

@app.route('/todos/<int:todo_id>',methods=['DELETE'])
@jwt_required() 
def delete_todo(todo_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    todo = Todo.query.get(todo_id)

    if todo.user_id != current_user_id:
        return jsonify({"message": "Forbidden"}),403
    
    db.session.delete(todo)
    db.session.commit()

    return '',204

@app.route("/todos",methods=['GET'])
@jwt_required() 
def get_todos():
    page = request.args.get('page',1,type=int)
    limit = request.args.get('limit',10,type=int)

    current_user_id = get_jwt_identity()

    todos_query = Todo.query.filter_by(user_id=current_user_id)
    total  = todos_query.count()
    todos = todos_query.paginate(page=page,per_page=limit,error_out=False)

    data = []
    for todo in todos.items:
        data.append(
            {"id": todo.id,"title":todo.title,"description":todo.description}
        )

    return jsonify({"data":data,"page":page,"limit": limit,"total":total})

if __name__ == '__main__':
    app.run(debug=True)