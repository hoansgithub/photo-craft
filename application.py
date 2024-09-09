# application.py

from skimage import data, io
import uuid
from flask import Flask, request
from werkzeug.utils import secure_filename
import  os
import base64
from io import BytesIO
from RMBGPkg.helper import Remover
from Entities.ImageTaskResponse import ImageTaskResponse
from Entities.AppSecurity import key_required
application = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
bg_remover = Remover()

#Helpers
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@application.route("/")
def hello_world():
    return "Hello, World! 1"

@application.route("/api/removebg", methods=['POST', 'GET'])
@key_required
def editor_remove_bg():
    if request.method == 'POST':
        try:
            # check if the post request has the file part
            if 'file' not in request.files:
                return ImageTaskResponse('file extension is invalid', None).to_jsonify()

            file = request.files['file']
            if file.filename == '':
                return ImageTaskResponse('file is missing', None).to_jsonify()
            if file and allowed_file(file.filename):
                # temp_file_name = str(uuid.uuid4())
                # filename = secure_filename(file.filename)
                # path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # file.save(path)
                #remove background
                target_image = io.imread(file)

                output_file = bg_remover.remove_background_for(target_image)

                buffered = BytesIO()
                output_file.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                return ImageTaskResponse('success', img_str).to_jsonify()
            return ImageTaskResponse('unknown error', None).to_jsonify()

        except Exception as e:
            return ImageTaskResponse(str(e), None).to_jsonify()
    else:
        return "editor/rmbg"
#
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
