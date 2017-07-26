from flask import render_template, url_for,  redirect
from flask_login import login_required, current_user
import datetime
from . import main
from .. import db
from ..models import FileTable,RecycleTable

@main.route('/test/', methods=['GET', 'POST'])
def test():
    return render_template('test.html')

@main.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    fileobj = db.session.query(FileTable).filter_by(user_id=current_user.get_id(), is_recycle=False).all()
    return render_template('index.html', fileobj=fileobj)


@main.route('/share/manage/', methods=['GET', 'POST'])
@login_required
def share_manage():
    fileobj = db.session.query(FileTable).filter_by(user_id=current_user.get_id(),is_share=True, is_recycle=False).all()
    return render_template('index.html', fileobj=fileobj)


@main.route('/category/<cate>', methods=['GET', 'POST'])
@login_required
def category(cate):
    cate = cate.lower()
    cate_list = ['audio', 'image', 'video', 'doc', 'other']
    if cate not in cate_list:
        return redirect(url_for('main.index'))
    else:
        fileobj = db.session.query(FileTable).filter_by(user_id=current_user.get_id(), file_category=cate, is_recycle=False).all()
    return render_template('index.html', fileobj=fileobj)


@main.route('/recycle/', methods=['POST', 'GET'])
@login_required
def recycle():
    fileobj = db.session.query(FileTable,RecycleTable).filter(FileTable.user_id==current_user.get_id(), FileTable.file_id==RecycleTable.file_id,FileTable.is_recycle==True,RecycleTable.recycle_time > datetime.datetime.now()).all()
    return render_template('recycle.html', fileobj=fileobj)
