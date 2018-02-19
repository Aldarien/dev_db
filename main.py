import os
from shutil import rmtree

from app.config import config
import subprocess

def call(cmd):
    try:
        subprocess.check_output(cmd)
    except Exception as e:
        print(cmd)

def main():
    
    dir = os.path.realpath(config('app.directories.temp'))
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)
    
    cmd1 = 'mysqldump -uroot -paryafoole --no-data --result-file="{0}\schema.sql" {1}'.format(
        dir,
        config('app.databases.source.name')
        )
    call(cmd1)
    cmd2 = 'mysqldump -uroot -paryafoole --no-create-info --skip-triggers --result-file="{}\data.sql" {}'.format(
        dir,
        config('app.databases.source.name')
        )
    call(cmd2)
    cmd3 = 'mysql -hlocalhost -uroot -paryafoole {} < {}\schema.sql'.format(
        config('app.databases.destination.name'),
        dir
        )
    call(cmd3)
    cmd4 = 'mysql -hlocalhost -uroot -paryafoole {} < {}\data.sql'.format(
        config('app.databases.destination.name'),
        dir
        )
    call(cmd4)
    
    '''
    try:
        rmtree(dir)
    except:
        raise e
    '''
    
if __name__ == '__main__':
    main()