# -*- coding: utf-8 -*-
#第三版  用了wtf来显示
import os
from flask import Flask, render_template,url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
app = Flask(__name__)
# 这两个可以写到config.py里面
app.config['SECRET_KEY'] = 'I have a dream'
# app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()
app.config['UPLOADED_PHOTOS_DEST'] = r'D:\uploadfile\static\img'
# 实例化UploadSet
photos = UploadSet('photos', IMAGES)
# 注册photos
configure_uploads(app, photos)
# 这一句可以写到config文件里面 限制上传文件的大小
patch_request_class(app)  # set maximum file size, default is 16MB
# 继承了faskform 可以直接加到你的表单里面 不用继承也可以
class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image only!'), FileRequired(u'File was empty!')])
    submit = SubmitField(u'Upload')
# 定义路由
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        print('点击了上传')
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)
if __name__ == '__main__':
    app.run()

# 代码复制自 https://zhuanlan.zhihu.com/p/24423891?refer=flask