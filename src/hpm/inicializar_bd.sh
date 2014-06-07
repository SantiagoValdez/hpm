python manage.py flush --noinput
python manage.py syncdb --noinput
python manage.py loaddata data.json 
chmod 666 db.sqlite3

