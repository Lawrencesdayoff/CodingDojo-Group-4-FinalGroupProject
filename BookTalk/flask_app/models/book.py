
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
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_info = []

   # CREATE books Models


    @classmethod
    def create(cls, data):
        query = """INSERT INTO book (title, review, image, author, user_id ) 
                    VALUES(%(title)s, %(review)s, %(image)s, %(author)s, %(user_id)s);"""
        data = {
        "title": data['title'],
        "review": data['review'],
        "image": data['image'],
        "author": data['author'],
        "user_id": session['id']
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        print(data)
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
    
    @classmethod
    def get_all_books_with_user_id(cls, data):
        query = "SELECT * FROM user RIGHT JOIN book ON book.user_id = %(data)s"
        results = connectToMySQL(cls.DB).query_db(query)
        return results
    
    @classmethod
    def get_by_title(cls, title):
        query = "SELECT * FROM book WHERE title = %(title)s;"
        data = { "title" : title }
        result = connectToMySQL(cls.DB).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_book_with_user(cls, id ):
        query = """
        SELECT * FROM book
        LEFT JOIN user 
        ON book.user_id = user.iduser 
        WHERE book.idbook = %(id)s;"""
        data = {"id": id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        posted_by = cls(results[0])
        for row_from_db in results:
            user_data = {
                "iduser": row_from_db["iduser"],
                "firstname": row_from_db["firstname"],
                "lastname": row_from_db['lastname'],
                "email": row_from_db['email'],
                "password": row_from_db['password'],
                "created_at": row_from_db['user.created_at'],
                "updated_at": row_from_db['user.updated_at']
            }
            posted_by.user_info.append(user.User(user_data))
            print(posted_by)
        return posted_by
    # UPDATE books Models


    @classmethod
    def update(cls, form_info, index):
        query = """UPDATE book 
                SET title=%(title)s, 
                review=%(review)s, image= %(image)s, author = %(author)s,
                user_id=%(user_id)s WHERE idbook = %(idbook)s;"""
        data = {
        "title": form_info['title'],
        "review": form_info['review'],
        "image": form_info['image'],
        "author": form_info['author'],
        "user_id": session['id'],
        "idbook": index
        }
        return connectToMySQL(cls.DB).query_db(query, data)


    # DELETE books Models

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM book WHERE idbook = %(idbook)s;"
        data = {"idbook": id}
        return connectToMySQL(cls.DB).query_db(query, data)
   
    # VALIDATIONS


    # @classmethod
    # def update(cls, updated_book):
    #     query = """UPDATE books 
    #             SET book (title, review, image, author, book_id, ) 
    #                 VALUES(%(title)s, %(review)s, %(image)s, %(author)s, %(book_id)s)"""
    #     data = {
    #     "title": updated_book['title'],
    #     "author": updated_book['author'],
    #     "review": updated_book['review'],
    #     "user_id": session['id']
    #     }
    #     return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM book WHERE idbook = %(idbook)s;"
        data = {"idbook": id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_info(book):
        print(book)
        is_valid = True
        if len(book['title'])< 2:
            flash('book title needs to be longer than two characters')
            is_valid = False
        if len(book['author'])< 2:
            flash('book network needs to be longer than two characters')
            is_valid = False
        if len(book['review'])< 2:
            flash('book comments needs to be longer than two characters')
            is_valid = False
        return is_valid


