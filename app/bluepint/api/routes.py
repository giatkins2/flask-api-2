from ....api import bp as api
from app.blueprints.api.auth import token_auth
from flask import request, make_response, abort
from ...helpers import require_admin
from .store_routes import Book, User


###### USERS #####

@api.get('/user')
@token_auth.login_required()
def get_users():
    users=User.query.all()
    user_dicts =[user.to_dict() for user in users]    
    return make_response({"users": user_dicts}, 200) 

@api.post("/user")
def post_item():
    user_dict=request.get_json()
    users = User()
    users.from_dict(user_dict)
    users.save()
    return make_response(f"User {users.id} with name {users.first_name} created", 200)    

@api.put("/user/<int:id>")
@token_auth.login_required()
@require_admin
def put_user(id):
    user_dict = request.get_json()
    user = User.query.get(id)
    if not user:
        abort(404)
    user.from_dict(user_dict)
    user.save()
    return make_response(f"User {user} with ID {user.id} has been updated", 200)

@api.delete('/user/<int:id>')
@token_auth.login_required()
@require_admin
def delete_user(id):
    user_to_delete = User.query.get(id)
    if not user_to_delete:
        abort(404)
    user_to_delete.delete()
    return make_response(f"User with id: {id} has been deleted", 200)


###### BOOKS ######

@api.get('/book')
def get_book():
    books=Book.query.all()
    book_dicts=[book.to_dict() for book in books]
    return make_response({"books":book_dicts},200)

@api.get('/book/<int:id>')
def get_post(id):
    book = Book.query.get(id)
    if not book:
        abort(404)
    book_dict= book.to_dict() 
    return make_response(book_dict, 200) 

@api.post('/book')
def post_book():
    book_dict = request.get_json()
    books = Book()
    books.from_dict(book_dict)
    books.save()
    return make_response(f"book {books.id} with name {books.title} created", 200)  

@app.put('/book/<int:id>')
@token_auth.login_required()
@require_admin
def put_book(id):
    book_dict = request.get_json()
    book = Book.query.get(id)
    if not book:
        abort(404)
    book.from_dict(book_dict)
    book.save()
    make_response(f"Book {book.title} with ID {book.id} has been updated", 200)

@app.delete('/item/<int:id>')
@token_auth.login_required()
@require_admin
def delete_book(id):
    book_to_delete = Book.query.get(id)
    if not book_to_delete:
        abort(404)
    book_to_delete.delete()
    return make_response(f"Book with id: {id} has been removed",200)