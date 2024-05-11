from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import book
from flask_app.models import comment

@app.post('/process_comment/<int:comment_id>')
def process_comment(comment_id):
    bookid = str(comment_id)
    comment.Comment.new_comment( comment_id,request.form)
    return redirect('/dashboard/' + bookid)

@app.get('/comments/delete/<int:x>')
def delete_comment(x):
    if 'id' not in session: return redirect('/')
    comment.Comment.delete(x)
    return redirect('/dashboard/')
