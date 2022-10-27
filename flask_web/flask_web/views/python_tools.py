from flask import Blueprint,render_template,request,redirect,Response,jsonify,send_file
import os
from werkzeug.utils import secure_filename

ts = Blueprint('ts',__name__)
download_path_dir = '/opt/nsfocus/flask_web/flask_web/views/static/'

@ts.route('/upload/',methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if str(f.filename).split('.')[1] != 'zip':
            data = {
            'code': 1
            , 'msg': '文件格式错误，必须是zip结尾'
            , 'data': {}
        }
            return jsonify(data)
        basepath = os.path.dirname(__file__) # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static',secure_filename(f.filename)) #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        print(upload_path)
        f.save(upload_path)
        f.close()
        print(f.filename)
        os.chdir('/opt/nsfocus/flask_web/flask_web/views/static/')
        os.system('python3 /opt/nsfocus/flask_web/flask_web/views/static/debug_get_info.py')
        print('==========================================================')
        print(f.filename.split('.zip')[0])
        os.system('rm -rf /opt/nsfocus/flask_web/flask_web/views/static/' + f.filename.split('.zip')[0])
        os.system('rm -rf /opt/nsfocus/flask_web/flask_web/views/static/' + f.filename)
        data = {
            'code': 0
            , 'msg': '上传成功，程序运行成功，请下载report.log文件'
            , 'data': {}
        }
        return jsonify(data)
        # return redirect('/download')
    return render_template('test.html')

@ts.route('/download/filename/<string:filename>/',methods = ['GET'])
def download(filename):
    download_file_path = download_path_dir + filename
    return send_file(download_file_path,as_attachment=True)


@ts.route('/filelist/',methods = ['GET'])
def filelist():
    file_name = os.popen("ls -lh /opt/nsfocus/flask_web/flask_web/views/static/ | grep report.log | awk '{print $8}'").readlines()
    file_time = os.popen("ls -lh /opt/nsfocus/flask_web/flask_web/views/static/ | grep report.log | awk '{print $6,$7}'").readlines()
    file_size = os.popen("ls -lh /opt/nsfocus/flask_web/flask_web/views/static/ | grep report.log | awk '{print $5}'").readlines()
    data = {
            "status": 200
            ,'code': 0
            ,"message": ""
            ,"total": 8
            ,"rows": {
                "item": [
                    ]
            }
        }
    for i in range(0,len(file_name)):
        dict = {
            'id':i+1,
            'filename':file_name[i],
            'filetime':file_time[i],
            'filesize':file_size[i]
        }
        data['rows']['item'].append(dict)
    
    return jsonify(data)

@ts.route('/delete/filename/<string:filename>',methods = ['GET','POST'])
def delete():
    pass