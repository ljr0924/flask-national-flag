import os
import time

from PIL import Image

from flask import Flask, request, render_template, send_from_directory, jsonify, url_for

from config import Config

app = Flask(__name__)

app.config.from_object(Config())


@app.route('/api/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        upload_file = request.files.get('image')
        # 拼接新的文件名
        new_file_name = f'{int(time.time())}&{upload_file.filename}'
        # 保存文件
        upload_file.save(os.path.join(os.path.join(app.root_path, 'media'), new_file_name))
        result_file_name = get_national_flag_head(new_file_name)
        file_url = get_file_url(request.host, result_file_name)
        return jsonify({
            'status': 200,
            'file_url': file_url
        })


@app.route('/api/download/<string:file_name>', methods=['GET'])
def download(file_name):
    file_path = os.path.join(app.root_path, 'media')
    if os.path.exists(os.path.join(file_path, file_name)):
        return send_from_directory(file_path, file_name, as_attachment=True)
    else:
        return jsonify({
            'status': 40004,
            'msg': '不存在文件'
        })


def get_file_url(host, file_name):
    """
    获取文件URL
    :param host:
    :param file_name:
    :return:
    """
    return f'http://{host}{url_for("download", file_name=file_name)}'


def get_national_flag_head(file_name):
    # 图片初始化
    media_root = app.config.get('MEDIA_ROOT')
    background = Image.open(os.path.join(media_root, file_name)).convert('RGBA')
    foreground = Image.open(os.path.join(media_root, 'foreground.png'))
    # 图片尺寸调整
    if background.size[0] < foreground.size[0]:
        foreground = foreground.resize(background.size)
    else:
        background = background.resize(foreground.size)
    # 图片叠加
    background.paste(foreground, (0, 0), foreground)

    # 保存到文件
    new_file_name = f'new{file_name.split(".")[0]}.png'
    new_file_path = os.path.join(media_root, new_file_name)
    background.save(new_file_path)
    print(f'图片合成成功 >> {new_file_name}')
    return new_file_name


if __name__ == '__main__':
    app.run()
