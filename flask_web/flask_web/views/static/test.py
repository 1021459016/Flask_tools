import os
os.chdir('/opt/nsfocus/flask_web/flask_web/views/static/')
file_list = os.popen('find ./ -name "basic_info.log"').readlines()
report = open("/opt/nsfocus/flask_web/flask_web/views/static/report.log","w+")
num_pat = "\d+"
for f in file_list:
    fpath = f.strip().rstrip("basic_info.log")
    print(fpath)
    file_name = fpath.split("/")[2]+fpath.split("/")[3]+fpath.split("/")[4]
    print(file_name)