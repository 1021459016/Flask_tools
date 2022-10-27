# encoding=utf-8

import os
import sys
import time
import datetime

LOG_PATH = '/opt/nsfocus/flask_web/flask_web/views/static/report.log'
SLEEP_TIME = 120
FILE_NAME = ('report.log','report.log.1','report.log.2')


def main():
    """
    主函数入口
    """
    
    while True:
        file_list = os.popen("ls -lh /opt/nsfocus/flask_web/flask_web/views/static/ | grep report.log | awk '{print $8}'").readlines()
        for i in file_list:
            filename = i.split('\n')[0]
            print(filename)
            if filename not in FILE_NAME:
                os.system('rm -rf /opt/nsfocus/flask_web/flask_web/views/static/{0}'.format(filename))
        if os.path.exists(LOG_PATH):
            backup_path = LOG_PATH + '.1'
            if os.path.exists(backup_path):
                backup_path_2 = backup_path.split('.1')[0] + '.2'
                if os.path.exists(backup_path_2):
                    os.remove(backup_path_2)
                    os.rename(backup_path, backup_path_2)
            os.rename(LOG_PATH, backup_path)
        global SLEEP_TIME
        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            SLEEP_TIME = int(sys.argv[1]) if int(sys.argv[1]) > 0 else 10
        except Exception:
            pass
    main()
