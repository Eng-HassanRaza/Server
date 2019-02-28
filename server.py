dir# uncompyle6 version 3.2.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.15rc1 (default, Apr 15 2018, 21:51:34) 
# [GCC 7.3.0]
# Embedded file name: /var/www/html/server.py
# Compiled at: 2019-02-08 20:21:48
from flask import Flask, render_template
from subprocess import call
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/work/<string:id>')
def work(id):
    if id == 'books':
        call(['python', 'books.py', '-r'])
    else:
        if id == 'music':
            call(['python', 'music.py', '-r'])
        else:
            if id == 'movies':
                call(['python', 'movies.py', '-r'])
            else:
                if id == 'bookss':
                    call(['python', 'books.py', '-s'])
                else:
                    if id == 'musics':
                        call(['python', 'music.py', '-s'])
                    else:
                        if id == 'moviess':
                            call(['python', 'movies.py', '-s'])
    return 'done'

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
