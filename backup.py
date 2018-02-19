command = 'mysqldump -uroot -paryafoole --no-create-info --skip-triggers --result-file="%s" %s'.format(
    config('app.directories.temp'),
    config('app.databases.source.name')
    )