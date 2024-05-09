from flask_app import app
from flask import render_template, redirect, request, session, flash
import time
from datetime import datetime, date
from flask_app.models import book
from flask_app.models import comment

@app.get('/dashboard')
def index():
    if 'id' not in session: return redirect('/')
    book_list = book.Book.get_all()
    book_date_list = []
    for item in book_list:
        book_date_list.append(time_converter(item.release_date))
    return render_template('dashboard.html', books = book_list, book_dates = book_date_list)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Create Users Controller

@app.post('/book_submit')
def book_submit():
    print(session)
    if book.Book.validate_info(request.form, True) == False:
        return redirect('/books/new')
    book.Book.save(request.form)
    return redirect('/dashboard')

@app.post('/process_comment/<int:comment_id>')
def process_comment(comment_id):
    bookid = str(comment_id)
    comment.Comment.new_comment( comment_id,request.form)
    return redirect('/books/' + bookid)

# Read Users Controller
@app.get('/books/new')
def books_new():
    if 'id' not in session: return redirect('/')
    today = date.today()
    return render_template('new_book.html', maxdate = today)
    
@app.get('/books/<int:x>')
def get_book(x):
    if 'id' not in session: return redirect('/')
    book_info = book.book.get_book_with_user(x)
    date_of_release = time_converter(book_info.release_date)
    comment_board = book.book.get_book_with_comments(x)
    print(comment_board.community_comments)
    return render_template('book.html', book = book_info, date_of_release = date_of_release, comment_board = comment_board)
    
@app.get('/books/edit/<int:x>')
def book_edit(x):
    if session:
        today = date.today()
        this_book = book.book.get_book(x)
        return render_template('edit_book.html', book = this_book, maxdate = today)
    else:
        return redirect('/')

# Update Controller
@app.post('/book_edit/<int:x>')
def update_book(x):
    index = str(x)
    if not book.book.validate_info(request.form, False):
        return redirect('/books/edit/' + index)
    book.book.update(request.form, index) 
    return redirect('/dashboard')
# Delete Users Controller
@app.get('/books/delete/<int:x>')
def delete_book(x):
    if 'id' not in session: return redirect('/')
    book.book.delete(x)
    return redirect('/dashboard')

@app.get('/comments/delete/<int:x>')
def delete_comment(x):
    if 'id' not in session: return redirect('/')
    comment.Comment.delete(x)
    return redirect('/dashboard')