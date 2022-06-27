from app import db
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name =  db.Column(db.String)
    email =  db.Column(db.String, unique=True, index=True)
    password =  db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, index=True, unique=True)
    token_exp = db.Column(db.DateTime)
    books = db.relationship('Book', backref='shopper', lazy="dynamic")

    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=60)
    
    @staticmethod
    def check_token(token):
        u  = User.query.filter_by(token=token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u

    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password = self.hash_password(data['password'])

    def save(self):
        db.session.add(self) 
        db.session.commit() 

    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/avataaars/{self.icon}.svg'
    
    def to_dict(self):
        return {
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'created_on':self.created_on,
            'is_admin':self.is_admin,
            'token':self.token
        }

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.String)
    pages = db.Column(db.Integer)
    summary = db.Column(db.Text)
    img = db.Column(db.String)
    subject = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post: {self.id} | {self.body[:15]}>'

    def edit(self, new_body):
        self.body=new_body

    def from_dict(self, data):
        self.title = data['title']
        self.author = data['author']
        self.pages=data['pages']
        self.summary = data['summary']
        self.img = data['img']
        self.subject = data['subject']

    def to_dict(self):
        return {
            'id':self.id,
            'title':self.title,
            'author':self.author,
            'pages':self.pages,
            'summary':self.summary,
            'img': self.img,
            'subject':self.subject,
            
        }
    def save(self):
        db.session.add(self) 
        db.session.commit() 
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()