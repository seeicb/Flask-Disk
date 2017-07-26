import datetime, time
from flask import render_template, request, abort, make_response, current_app,jsonify, flash, session
from flask_login import login_required, current_user
from . import file
from .forms import share_pass
from .. import db, csrf
from ..models import FileTable, ShareTable, RecycleTable
from .libs import hdfs_client, get_md5, set_type, get_file_ext, get_hdfs_filename,get_share_pass



@file.route('/upload/', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_ext = get_file_ext(file.filename)
            file_category = set_type(file_ext)
            create_time = datetime.datetime.now()
            hdfs_path = datetime.date.today().strftime("/%Y/%m/%d/")
            hdfs_filename = get_hdfs_filename()
            user_id = current_user.get_id()
            data = file.read()
            try:
                hdfs_client.write(hdfs_path + hdfs_filename, data=data)
                fileobj = FileTable(filename=file.filename, file_ext=file_ext, file_size=request.form['size'],
                                    file_mime=request.form['type'],
                                    file_category=file_category, create_time=create_time,
                                    hdfs_path=hdfs_path, hdfs_filename=hdfs_filename, user_id=user_id)
                db.session.add(fileobj)
                db.session.commit()
            except Exception as err:
                print(err)
                abort(500)
        else:
            abort(405)
    return render_template('file/upload.html')


@file.route('/download/<int:id>', methods=['GET', 'POST'])
@login_required
def download(id):
    fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=False).first_or_404()
    path = fileobj.hdfs_path + fileobj.hdfs_filename
    filename = fileobj.filename
    with hdfs_client.read(path) as reader:
        buf = reader.read()
    response = make_response(buf)
    try:
        response.headers.add('Content-Disposition', 'attachment', filename=filename.encode())
    except Exception as err:
        raise(err)
    return response




@file.route('/share/download/', methods=['POST', 'GET'])
def down_url():
    url = request.args.get('url')
    shareobj = ShareTable.query.filter_by(share_url=url).first_or_404()
    fileobj = FileTable.query.filter_by(file_id=shareobj.file_id, is_recycle=False).first_or_404()
    if (shareobj.share_pass=='' or session['share_pass'] == shareobj.share_pass):
        path = fileobj.hdfs_path + fileobj.hdfs_filename
        filename = fileobj.filename
        with hdfs_client.read(path) as reader:
            buf = reader.read()
        response = make_response(buf)
        response.headers.add('Content-Disposition', 'attachment', filename=filename.encode())
        return response
    else:
        abort(404)


@file.route('/fid/<int:id>', methods=['GET', 'POST'])
@login_required
def file_detail(id):
    fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=False).first_or_404()
    shareobj = ShareTable.query.filter_by(file_id=id).first()
    return render_template('file/file_detail.html', fileobj=fileobj, shareobj=shareobj)


@file.route('/share/make/', methods=['POST', 'GET'])
@login_required
def make_share():
    if request.method == 'POST':
        id = request.form['id']
        fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=False).first_or_404()
        if fileobj.is_share == True:
            shareobj = ShareTable.query.filter_by(file_id=id).first()
            shareobj.share_pass = ''
            return jsonify(shareobj.share_url)
        else:
            fileobj.is_share = True
        share_url = get_md5(str(fileobj.file_id) + fileobj.hdfs_filename + str(time.time()))
        shareobj = ShareTable(file_id=id, share_url=share_url)
        try:
            db.session.add(fileobj)
            db.session.add(shareobj)
            db.session.commit()
            return jsonify(shareobj.share_url)
        except Exception as err:
            # print(err)
            abort(500)
    else:
        abort(405)


@file.route('/sharepass/make/', methods=['POST', 'GET'])
@login_required
def make_sharepass():
    if request.method == 'POST':
        id = request.form['id']
        fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=False).first_or_404()
        if fileobj.is_share == True:
            shareobj = ShareTable.query.filter_by(file_id=id).first()
            if shareobj.share_pass == '':
                share_pass = get_share_pass()
            else:
                share_pass = shareobj.share_pass
            return jsonify(shareobj.share_url, shareobj.share_pass)
        else:
            fileobj.is_share = True

        share_url = get_md5(str(fileobj.file_id) + fileobj.hdfs_filename + str(time.time()))
        share_pass = get_share_pass()
        shareobj = ShareTable(file_id=id, share_url=share_url, share_pass=share_pass)
        try:
            db.session.add(fileobj)
            db.session.add(shareobj)
            db.session.commit()
            return jsonify(shareobj.share_url, shareobj.share_pass)
        except Exception as err:
            # print(err)
            abort(500)
    else:
        abort(405)
    pass


@file.route('/share/cancel/', methods=['POST', 'GET'])
@login_required
def cancel_share():
    if request.method == 'POST':
        id = request.form['id']
        fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=False).first_or_404()
        shareobj = ShareTable.query.filter_by(file_id=id).first_or_404()
        fileobj.is_share = False
        try:
            db.session.add(fileobj)
            db.session.delete(shareobj)
            db.session.commit()
            return jsonify('success')
        except Exception as err:
            print(err)
            abort(500)
    abort(405)


@file.route('/rename/', methods=['POST', 'GET'])
@login_required
def rename():
    id = request.form['id']
    new_name = request.form['new_name']
    fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=False).first_or_404()
    fileobj.filename = new_name
    fileobj.file_ext = get_file_ext(new_name)
    fileobj.file_category = set_type(fileobj.file_ext)
    db.session.add(fileobj)
    db.session.commit()
    return render_template('file/file_detail.html', fileobj=fileobj)



@csrf.exempt
@file.route('/share/<url>', methods=['POST', 'GET'])
def share_url(url):
    form = share_pass()
    shareobj = ShareTable.query.filter_by(share_url=url).first_or_404()
    fileobj = FileTable.query.filter_by(file_id=shareobj.file_id).first_or_404()

    if shareobj.share_pass == '':
        return render_template('file/share.html', shareobj=shareobj, fileobj=fileobj)
    else:
        if 'share_pass' in session and session['share_pass'] == shareobj.share_pass:
            return render_template('file/share.html', shareobj=shareobj, fileobj=fileobj)
        else:
            if form.validate_on_submit():
                if form.password.data == shareobj.share_pass:
                    session['share_pass'] = shareobj.share_pass
                    return render_template('file/share.html', shareobj=shareobj, fileobj=fileobj)
                else:
                    flash("密码错误")
        return render_template('file/share_pass.html', form=form)


@file.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        id = request.form['id']
        fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=False).first_or_404()
        if fileobj.is_share == True:
            shareobj = ShareTable.query.filter_by(file_id=id).first()
            fileobj.is_share = False
            db.session.delete(shareobj)
        hdfs_trash = current_app.config['HDFS_TRASH']
        hdfs_src_path = fileobj.hdfs_path + fileobj.hdfs_filename
        hdfs_dst_path = hdfs_trash + hdfs_src_path
        trash_dir = hdfs_trash + fileobj.hdfs_path
        hdfs_client.makedirs(trash_dir)

        fileobj.is_recycle = True
        recycle_time = datetime.datetime.now() + datetime.timedelta(days=7)
        recycleobj = RecycleTable(file_id=id, recycle_time=recycle_time, user_id=current_user.get_id())
        try:
            db.session.add(fileobj)
            db.session.add(recycleobj)
            db.session.commit()
            hdfs_client.rename(hdfs_src_path, hdfs_dst_path)
        except Exception as err:
            # print(err)
            abort(500)
        return jsonify('success')


@file.route('/recovery/', methods=['POST', 'GET'])
@login_required
def recovery():
    if request.method == 'POST':
        id = request.form["id"]
        fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=True).first_or_404()
        hdfs_trash = current_app.config['HDFS_TRASH']
        hdfs_dst_path = fileobj.hdfs_path + fileobj.hdfs_filename
        hdfs_src_path = hdfs_trash + hdfs_dst_path
        fileobj.is_recycle = False
        recycleobj = db.session.query(RecycleTable).filter(
            RecycleTable.file_id == id, RecycleTable.user_id == current_user.get_id(),
            RecycleTable.recycle_time > datetime.datetime.now()).first()
        try:
            db.session.add(fileobj)
            db.session.delete(recycleobj)
            db.session.commit()
            hdfs_client.rename(hdfs_src_path, hdfs_dst_path)
        except Exception as err:
            # print(err)
            abort(500)
        return jsonify('success')



@file.route('/rid/<int:id>', methods=['POST', 'GET'])
@login_required
def recycle_detail(id):
    fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=True).first_or_404()
    recycleobj = RecycleTable.query.filter(RecycleTable.file_id == id,
                                           RecycleTable.recycle_time > datetime.datetime.now()).first_or_404()
    return render_template('file/recycle_detail.html', fileobj=fileobj, recycleobj=recycleobj)


@file.route('/rdelete/', methods=['POST', 'GET'])
@login_required
def delete_complete():
    if request.method == 'POST':
        id = request.form["id"]
        fileobj = FileTable.query.filter_by(file_id=id, user_id=current_user.get_id(), is_recycle=True).first_or_404()
        hdfs_trash = current_app.config['HDFS_TRASH']
        file_path = hdfs_trash + fileobj.hdfs_path + fileobj.hdfs_filename
        hdfs_client.delete(file_path)
        db.session.delete(fileobj)
        db.session.commit()
        return jsonify('success')


@file.route('/save/', methods=['POST', 'GET'])
@login_required
def share_save():
    pass
