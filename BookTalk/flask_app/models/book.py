
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, comment, like
class Book:
    DB = "booktok" 
    def __init__(self, data):
        self.idbook = data['idbook']
        self.title = data['title']
        self.review = data['review']
        self.image = data['image']
        self.author = data['author']
        self.book_id = data['book_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

   # CREATE books Models


    @classmethod
    def create(cls, data):
        query = """INSERT INTO book (title, review, image, author, book_id, ) 
                    VALUES(%(title)s, %(review)s, %(image)s, %(author)s, %(book_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        print({
            "title": cls.title,
            "reivew": cls.review,
            "image": cls.image,
            "author": cls.author,
            "book_id": cls.book_id})
        return result


    # READ books Models


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM book;"
        results = connectToMySQL(cls.DB).query_db(query)
        books = []
        for u in results:
            books.append(cls(u))
            print("one time")
        return books
    
    @classmethod
    def get_book(cls, idbook):
        query = "SELECT * FROM book WHERE idbook = %(idbook)s"
        data = {"idbook": idbook}
        results = connectToMySQL(cls.DB).query_db(query, data)
        books = []
        for u in results:
            books.append(cls(u))
            print("one time")
        return books[0]
    

    # UPDATE books Models


    @classmethod
    def update(cls, data):
        query = """UPDATE books 
                SET book (title, review, image, author, book_id, ) 
                    VALUES(%(title)s, %(review)s, %(image)s, %(author)s, %(book_id)s);"""
        return connectToMySQL(cls.DB).query_db(query, data)


    # DELETE books Models

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM books WHERE idbook = %(idbook)s;"
        data = {"idbook": id}
        return connectToMySQL(cls.DB).query_db(query, data)
   
    # VALIDATIONS