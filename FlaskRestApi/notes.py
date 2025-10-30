from flask_restful import Resource
from flask import request
from model import User
from model import Note
from app import db
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity


def notes_register(app,api,bcrypt,jwt): 
    class UserRegistration(Resource): 
        def post(self): 
            data = request.get_json()
            username = data['username']
            password = data['password']

            hash_password = bcrypt.generate_password_hash(password)

            if not username or not password: 
                return {'message ':'Missing username or password'},400
            if User.query.filter_by(username = username).first(): 
                return {'message' : 'Username already exist'},400
            
            new_user = User(username = username,password = hash_password)
            db.session.add(new_user)
            db.session.commit()
            return {'message':'user created successfully'},200
        
    class UserLogin(Resource): 
        def post(self): 

            data = request.get_json()
            username = data['username']
            password = data['password']

            user = User.query.filter_by(username = username).first()

            if user and bcrypt.check_password_hash(user.password ,password): 
                access_token = create_access_token(identity = str(user.id)) 
                return {'access token': access_token},200
            return {'Message':'Invalid credentials'},401
            

    class NotesResource(Resource):
        @jwt_required()
        def post(self): 
            current_user_id = get_jwt_identity()

            data = request.get_json()
            title = data.get('title')
            content = data.get('content')

            if not title or not content: 
                return {'message':'Title and Content required'},400
            new_notes = Note(title = title ,content = content ,owner_id = current_user_id)

            db.session.add(new_notes)
            db.session.commit()
            return {'message':'note created successfully'},201         
        
        @jwt_required()
        def get(self):
            current_user_id = get_jwt_identity()
            notes = Note.query.filter_by(owner_id = current_user_id).all()

            if not notes: 
                return {'message':'No notes found'},400
            
            notes_data = []
            for note in notes: 
                notes_data.append({
                    'id': note.id, 
                    'title' : note.title, 
                    'content': note.content
                })
            return {'notes': notes_data},200
        
    class UpadteResource(Resource):    
        @jwt_required()
        def put(self,id): 
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            notes = Note.query.filter_by(id = id, owner_id = current_user_id).first()

            if not notes: 
                return {'message':'Note not found or not authorized'},404 
            
            notes.title = data.get('title',notes.title)
            notes.content = data.get('content',notes.content)

            db.session.commit()
            return {'message':'Note updated successfully'}
        
        @jwt_required()
        def delete(self,id): 
            current_user_id = get_jwt_identity()
            
            notes = Note.query.filter_by(id=id, owner_id = current_user_id).first()

            if not notes: 
                return {'message':'Note not found or not authorized'},404 
            
            db.session.delete(notes)
            db.session.commit()
            return {'message':'Note deleted successfully'}
                      

 

    api.add_resource(UserRegistration,'/register')
    api.add_resource(UserLogin,'/login')
    api.add_resource(NotesResource,'/notes')
    api.add_resource(UpadteResource,'/notes/<int:id>')

    

