from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import book
from flask_app.models import comment
import random;


#Helper Functions



# Root
@app.get('/dashboard/', defaults={'x': None})
@app.get('/dashboard/<int:x>')
def index(x):
    if 'id' not in session: return redirect('/')
    book_list = book.Book.get_all()
    booklist_length = len(book_list)
    if x == None:
        random_book = random.choice(book_list)
        x = random_book.idbook
        book_post = book.Book.get_book_with_user(random_book.idbook)
        print(x)
    else:
        book_post = book.Book.get_book_with_user(x)
    next = x + 1
    prev = x - 1
    print(next % booklist_length)
    print(prev % booklist_length)
    return render_template('dashboard.html', books = book_list, post = book_post, x = x,
                            next = next, prev = prev, booklist_length = booklist_length)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Create Users Controller

@app.post('/book_submit')
def book_submit():
    print(session)
    print(request.form)
    if book.Book.validate_info(request.form) == False:
        return redirect('/books/new')
    book.Book.create(request.form)
    return redirect('/dashboard/' )


# Read Users Controller
@app.get('/books/new')
def books_new():
    if 'id' not in session: return redirect('/')
    return render_template('newbook.html')
    
@app.get('/books/<int:x>')
def get_book(x):
    if 'id' not in session: return redirect('/')
    book_info = book.Book.get_book_with_user(x)
    date_of_release = time_converter(book_info.release_date)
    comment_board = book.Book.get_book_with_comments(x)
    print(comment_board.community_comments)
    return render_template('book.html', book = book_info, date_of_release = date_of_release, comment_board = comment_board)
    
@app.get('/books/edit/<int:x>')
def book_edit(x):
    if session:
        this_book = book.Book.get_book(x)
        return render_template('editbook.html', book = this_book)
    else:
        return redirect('/dashboard/')

# Update Controller
@app.post('/book_edit/<int:x>')
def update_book(x):
    index = str(x)
    if not book.Book.validate_info(request.form):
        return redirect('/books/edit/' + index)
    book.Book.update(request.form, index) 
    print(request.form)
    return redirect('/dashboard/')
# Delete Users Controller
@app.get('/books/delete/<int:x>')
def delete_book(x):
    if 'id' not in session: return redirect('/')
    book.Book.delete(x)
    return redirect('/dashboard/')
