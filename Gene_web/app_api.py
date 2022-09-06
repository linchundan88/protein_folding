from flask import Flask, request, render_template, session, make_response
import os
import uuid
import cv2
from my_module import my_db_helper
import my_config
import shutil
import xmlrpc
import json
from flask import send_from_directory
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xca\x5c\x86\x94\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.config['JSON_AS_ASCII'] = False

# BASE_DIR = my_config.API_file_dir
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__name__)),'static', 'imgs')

def validate_request():
    # if request.remote_addr in ['', '']:
    #     return True
    # else:
    #     return json.dumps({"data": 'request from illegal IP address'}), 200

    return True




@app.route('/showFile/<str_uuid>/<file_name>')
def showFile(str_uuid, file_name):
    if not validate_request():
        return

    dir = os.path.join(BASE_DIR, str_uuid)
    return send_from_directory(dir, file_name)



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=my_config.PORT_API
    )
