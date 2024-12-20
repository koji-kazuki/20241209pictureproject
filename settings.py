import os

basedir = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) or 'sqlite:///' + os.path.join(basedir,'app.sqlite')                                

# シークレットキーの値として10バイトの文字列をランダムに生成
SECRET_KEY = os.urandom(10)

# 画像のアップロード先のフォルダーを登録
from pathlib import Path
# basedirにapps、imagesを連結してPathオブジェクトを生成し、
# str()で文字列に変換
UPLOAD_FOLDER = str(Path(basedir,'images'))

