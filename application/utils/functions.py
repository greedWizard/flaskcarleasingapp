import secrets
import os
from PIL import Image
from flaskcarleasing.config import app


def save_picture(form_pic):
    size = (250, 250)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)

    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static{os.path.sep}pics', picture_fn)

    i = Image.open(form_pic)
    i.thumbnail(size)

    i.save(picture_path)

    return picture_fn