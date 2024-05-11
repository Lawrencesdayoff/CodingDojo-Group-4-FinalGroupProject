from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, comment, like


class Comment:
    DB = "booktok"
    def __init__(self, data):
        self.idcomment = data['idcomment']
        self.book_id = data['book_id']
        self.user_id = data['user_id']
        self.comment_text = data['comment_text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.likes = []

    @classmethod
    def create(cls, request):
        query = """INSERT INTO book (book_id, user_id, comment_text) 
                    VALUES(%(book_id)s, %(user_id)s, %(comment_text)s);"""
        data = {
            "book_id": request['book_id'],
            "user_id": session['id'],
            "comment_text": request['comment_text']
        }

        result = connectToMySQL(cls.DB).query_db(query, data)
        print(data)
        return result
    
    