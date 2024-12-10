
""" 識別名をpictappにしてBlueprintオブジェクトを生成

    ・テンプレートフォルダーは同じディレクトリの'templates_pict'
    ・staticフォルダーは同じディレクトリの'static_pict'
"""
from flask import Blueprint

pictapp = Blueprint(
    'pictapp',
    __name__,
    template_folder='templates_pict',
    static_folder='static_pict',
    )

"""pictappのトップページのルーティングとビューの定義
"""
from flask import render_template
from flask_login import login_required # login_required
from sqlalchemy import select # sqlalchemy.select()
from flask import request # flask.request
from flask_paginate import Pagination, get_page_parameter

# ログイン必須にする
@pictapp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # 投稿記事のレコードをidの降順で全件取得するクエリ
    stmt = select(
        modelpict.UserPicture).order_by(modelpict.UserPicture.create_at.desc())
    # データベースにクエリを発行
    entries = db.session.execute(stmt).scalars().all()

    # 現在のページ番号を取得
    page = request.args.get(
        get_page_parameter(), type=int, default=1)
    # entriesから現在のページに表示するレコードを抽出
    res = entries[(page - 1)*6: page*6]
    # Paginationオブジェクトを生成
    pagination = Pagination(
        page=page,          # 現在のページ
        total=len(entries), # 全レコード数を取得
        per_page=6)         # 1ページあたりのレコード数

    # top.htmlをレンダリングする際に
    # user_pictsでレコードデータres
    # paginationでPaginationオブジェクトを引き渡す
    return render_template('top.html', user_picts=res, pagination=pagination)

"""imagesフォルダー内の画像ファイルのパスを返す機能
"""
from flask import send_from_directory # send_from_directory

@pictapp.route('/images/<path:filename>')
def image_file(filename):
    # imagesフォルダーのパスに<path:filename>で取得した
    # ファイル名filenameを連結して返す
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'], filename)

"""ログアウトのルーティングとビューの定義
"""
from flask_login import logout_user
from flask import render_template, url_for, redirect

@pictapp.route('/logout')
@login_required
def logout():
    # flask_loginのlogout_user()関数でログイン中のユーザーを
    # ログアウトさせる
    logout_user()
    # ログイン画面のindexビューにリダイレクト
    return redirect(url_for('authapp.index'))

"""画像アップロードページのルーティングとビューの定義
"""
import uuid # uuid
from pathlib import Path # pathlibのPath
from flask_login import current_user # current_user
from flask import current_app # current_app

from apps.app import db # apps.pyのSQLAlchemyインスタンスapp
from apps.pictapp import forms # pictapp.formsモジュール
from apps.pictapp import models as modelpict # pictapp.modelsモジュール

@pictapp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # UploadImageFormをインスタンス化
    form = forms.UploadImageForm()
    # アップロードフォームのsubmitボタンが押されたときの処理
    if form.validate_on_submit():
        # フォームで選択された画像ファイルをFileStorageオブジェクトとして取得
        file = form.image.data
        # 画像のファイル名から拡張子を抽出する
        suffix = Path(file.filename).suffix
        # uuid4()でランダムな識別子を生成して画像ファイルの拡張子を連結する
        imagefile_uuid = str(uuid.uuid4()) + suffix
        # imagesフォルダーのパスにimagefile_uuidを連結してパスを作る
        image_path = Path(
            current_app.config['UPLOAD_FOLDER'], imagefile_uuid)
        # 画像データをファイル名をimage_pathにして保存
        file.save(image_path)

        # UserPictureをインスタンス化してフォームのデータを格納
        upload_data = modelpict.UserPicture(
            # user_idに現在ログイン中のユーザーのidを格納
            user_id=current_user.id,
            # usernameに現在ログイン中のユーザー名を格納
            username = current_user.username,
            # titleにフォームのtitleの入力データを格納
            title=form.title.data,
            # contentsにフォームのmessageの入力データを格納
            contents=form.message.data,
            # image_pathに画像のファイル名(uuid+実際のファイル名)を格納
            image_path=imagefile_uuid
        )

        # UserPictureオブジェクトをレコードのデータとして
        # データベースのテーブルに追加
        db.session.add(upload_data)
        # データベースを更新
        db.session.commit()
        # 処理完了後、pictapp.indexにリダイレクト
        return redirect(url_for('pictapp.index'))
    
    # トップページへのアクセスは、index.htmlをレンダリングして
    # SignupFormのインスタンスformを引き渡す
    return render_template('upload.html', form=form)

"""詳細ページのルーティングとビューの定義
"""
@pictapp.route('/detail/<int:id>')
@login_required
def show_detail(id):
    # apps.modelsモジュールmodelpictのUserPictureモデルで
    # データベーステーブルから<int:id>で取得したidのレコードを抽出
    detail = db.session.get(modelpict.UserPicture, id)
    # 抽出したレコードをdetail=detailに格納して
    # detail.htmlをレンダリングする
    return render_template('detail.html', detail=detail)

"""ユーザーの投稿一覧ページのルーティングとビューの定義
"""
@pictapp.route('/user-list/<int:user_id>')
@login_required
def user_list(user_id):
    # apps.modelsモジュールmodelpictのUserPictureモデルで
    # データベーステーブルのuser_idカラムが<int:user_id>のレコードを抽出し、
    # create_atの降順で並べ替えるクエリ
    stmt = select(
        modelpict.UserPicture).filter_by(user_id=user_id).order_by(
            modelpict.UserPicture.create_at.desc())
    # データベースにクエリを発行
    userlist = db.session.execute(stmt).scalars().all()

    # 抽出したレコードをuserlist=userlistに格納して
    # userlist.htmlをレンダリングする
    return render_template(
        'userlist.html', userlist=userlist)

"""マイページのルーティングとビューの定義
"""
@pictapp.route('/mypage/<int:user_id>')
@login_required
def mypage(user_id):
    # apps.modelsモジュールmodelpictのUserPictureモデルで
    # データベーステーブルのuser_idカラムが<int:user_id>のレコードを抽出し、
    # create_atの降順で並べ替えるクエリ
    stmt = select(
        modelpict.UserPicture).filter_by(user_id=user_id).order_by(
            modelpict.UserPicture.create_at.desc())
    # データベースにクエリを発行
    mylist = db.session.execute(stmt).scalars().all()

    # 抽出したレコードをuserlist=userlistに格納して
    # mypage.htmlをレンダリングする
    return render_template('mypage.html', mylist=mylist)

"""テーブルからレコードを削除する機能のルーティングとビューの定義

マイページ(mypage.html)の削除用リンクからのみ呼ばれる
<int:id>で削除対象レコードのidを取得
"""
@pictapp.route('/delete/<int:id>')
@login_required
def delete(id):
    # 削除対象のidのレコードをデータベースから取得
    entry = db.session.get(modelpict.UserPicture, id)
    # データベースのインスタンスからsession.delete()を実行し、
    # 引数に指定したレコードを削除する
    db.session.delete(entry)
    # 削除した結果をデータベースに反映する
    db.session.commit()
    # 投稿画像一覧ページにリダイレクト
    return redirect(url_for('pictapp.index'))
