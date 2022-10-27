import zipfile,os,re

os.chdir('/opt/nsfocus/flask_web/flask_web/views/static/')
os.system('find /opt/nsfocus/flask_web/flask_web/views/static/ -name "*.zip" | xargs -n1 unzip -o ')
os.system('find /opt/nsfocus/flask_web/flask_web/views/static/  -name "debug*.rar" |xargs -I {} mv {} {}.zip')
file1_list = os.popen('find /opt/nsfocus/flask_web/flask_web/views/static/ -name "*.zip"').readlines()
file_list = file1_list[0:len(file1_list)-1]
print(file_list)
for fpath in file_list:
    path = fpath.strip()
    output_path = path.split("debug")[0]+path.split("debug")[1].split(".rar")[0]
    print(output_path)
    zip_log = zipfile.ZipFile(path, 'r')
    zip_log.extractall(output_path,pwd=b'"nsf0cus."')
    
os.chdir('/opt/nsfocus/flask_web/flask_web/views/static/')
file_list = os.popen('find ./ -name "basic_info.log"').readlines()
report = open("/opt/nsfocus/flask_web/flask_web/views/static/report.log","w+")
num_pat = "\d+"
for f in file_list:
    fpath = f.strip().rstrip("basic_info.log")
    file_name = fpath.split("/")[2]+fpath.split("/")[3]+fpath.split("/")[4]
    lines = open(f.strip(),"r").readlines()
    now_time = ''
    for l in lines:
        if "#########################################" in l :
            now_time=l.strip().rstrip("#")
        if "Inactive(file):" in l :
            n = re.search(num_pat,l).group(0)
            if int(n) > 1024*1024*4:
                report.write(file_name+" at "+ now_time+": inactvie > 4G -"+n+"\n")
        
        if "Mem:" in l:
            n = l.split()[3]
            if int(n) < 1024:
                report.write(file_name+" at "+ now_time+": free < 1G -"+n+"\n")
        if "/mnt/cf" in l and re.search("\d{2}%\s/mnt/cf",l):
            n = l.split()[4].rstrip("%")
            if int(n) > 90:
                report.write(file_name+" at "+ now_time+": cf card < 10% -"+n+"\n")
        if "/opt/nsfocus/log" in l and re.search("\d{2}%\s/opt/nsfocus/log",l):
            n = l.split()[4].rstrip("%")
            if int(n) > 60:
                report.write(file_name+" at "+ now_time+": log dir < 40% -"+n+"\n")
        if "/tmp" in l and re.search("\d{2}%\s/tmp",l):
            n = l.split()[4].rstrip("%")
            if int(n) > 60:
                report.write(file_name+" at "+ now_time+": tmp dir < 40% -"+n+"\n")
report.close()
