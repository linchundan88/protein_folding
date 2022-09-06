import hashlib

import xmlrpc.client


def CalcSha1_str(str_original):
    sha1obj = hashlib.sha1()
    sha1obj.update(str_original.encode('utf-8'))
    hash = sha1obj.hexdigest()

    return hash

def get_image_quality():

    img_source = "/data/788721#8c02083160d164bb05b8be60fdf48a3c1757fa33.JPG"

    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy1:
        image_quality_score = proxy1.predict_image_quality(img_source)

    print(image_quality_score)


if __name__ == '__main__':

    get_image_quality()

    # password = 'jsiec'
    # encrypt_password = CalcSha1_str(password)
    # print(encrypt_password)
    #
    # password = 'eyepacs'
    # encrypt_password = CalcSha1_str(password)
    # print(encrypt_password)
    #
    # password = '123456'
    # encrypt_password = CalcSha1_str(password)
    # print(encrypt_password)

    # import pdfkit
    # pdfkit.from_url('http://0.0.0.0:5888/', 'out.pdf' )
