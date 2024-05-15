from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.get('/messages')
def messages():
    return [m.to_dict() for m in Message.query.all()], 200

@app.post('/messages')
def new_message():
    new_message = Message(
        body=request.json.get('body'),
        username=request.json.get('username'),  
    )
    db.session.add(new_message)
    db.session.commit()

    return new_message.to_dict(), 201

@app.patch('/messages/<int:id>')
def update_message(id):
    message_to_update = Message.query.where(Message.id == id).first()

    if message_to_update:
        for key in request.json.keys():
            if not key == id:
                setattr(message_to_update, key, request.json[key])
        db.session.add(message_to_update)
        db.session.commit()
        return message_to_update.to_dict(), 202
    else:
        return {"error": "not found"}
    
@app.delete('/messages/<int:id>')
def delete_message(id):
    message_to_delete = Message.query.where(Message.id==id).first()

    if message_to_delete:
        db.session.delete(message_to_delete)
        db.session.commit()
        return {}, 204
    else:
        return {"error": "not found"}

if __name__ == '__main__':
    app.run(port=5555)
