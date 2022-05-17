import os
from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from query_handler import Handler

views = Blueprint('views', __name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
QUERY_FOLDER = f'static{os.sep}queries'
PACKAGE = 'website'
DATA_FOLDER = f'search_engine{os.sep}data{os.sep}images{os.sep}training'

ALLOWED_EXT = ['jpg', 'png']
selected_image = ''
query_results = []

handler = Handler()


@views.route("/")
def home():
    global selected_image
    return render_template("home.html", selected_image=selected_image)


@views.route("/selected_image", methods=['POST', 'GET'])
def select_query_image():
    if request.method == 'GET':
        return home()

    global selected_image

    target = os.path.join(APP_ROOT, QUERY_FOLDER)

    file = request.files['file']

    if not file:
        flash(f'No file chosen', 'error')
        return redirect('/')

    filename, ext = secure_filename(file.filename).lower().split('.')

    if ext not in ALLOWED_EXT:
        flash(f'Invalid filetype: {ext.upper()}', 'error')
        return redirect('/')

    selected_image = f'{filename}.{ext}'
    print(f'Received: {selected_image}')
    flash(f'{selected_image} is uploaded successfully!', 'success')

    file_path = os.path.join(target, selected_image)
    file.save(file_path)

    return render_template('home.html', selected_image=selected_image)

    # TODO:
    # make a the directory for query images if it is not available i.e os.mkdir(directory name)
    # get the filename and store the file in the query directory


@views.route("/query_result", methods=['POST', 'GET'])
def start_query():
    global selected_image
    global query_results

    if request.method == 'GET':
        if query_results:
            return render_template("query_result.html",
                                   selected_image=selected_image,
                                   query_results=query_results)
        else:
            return redirect('/')

    image_name = selected_image.split('.')[0]

    flash(f'Searching using image {image_name}...', 'success')

    img_path = os.path.join(PACKAGE, QUERY_FOLDER, selected_image)

    query_results = handler.query(img_path)

    return render_template("query_result.html",
                           selected_image=selected_image,
                           query_results=query_results)


@views.route("/settings", methods=['POST', 'GET'])
def settings():
    return redirect('/')
