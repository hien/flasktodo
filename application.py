from flask import Flask
app = Flask(__name__)

from google.appengine.ext import db
from google.appengine.api import users

try:
    import json
except ImportError:
    import simplesjon as json

from flask import redirect, url_for, request, render_template, abort, flash, get_flashed_messages

class Task(db.Model):
    user = db.UserProperty()
    name = db.StringProperty(required=True)
    done = db.BooleanProperty()

    def __dict__(self):
        return {
            'id' : self.key().id(),
            'name' : self.name,
            'done' : self.done
        }

@app.route('/')
def list():
    user = users.get_current_user()
    tasks = Task.all().filter('user =', user)
    return render_template('list.html', user=user, logout_url=users.create_logout_url("/"), tasks=tasks, flashes=get_flashed_messages());

@app.route('/', methods=['POST'])
def task_post():
    f = request.form['format']
    name = request.form['name']
    if not name:
        msg = "Oops you forgot to set a task name"
        if f == 'json':
            return json.dumps({ 'message' : msg })
        else:
            flash(msg)
            return redirect(url_for('list'))

    task = Task(name = request.form['name'])
    task.user = users.get_current_user()
    task.put()
    if f == 'json':
        return json.dumps({ 'message' : 'Sucessful added!', 'task' : task.__dict__() })
    else:
        return redirect(url_for('list'))

@app.route('/delete/<int:id>')
@app.route('/delete/<int:id>.<f>')
def task_delete(id, f='html'):
    task = Task.get_by_id(id)
    if task and task.user == users.get_current_user():
        task.delete()
    else:
        abort(404)

    if f == 'json':
        return json.dumps({ 'message' : 'Sucessful deleted!'})
    return redirect(url_for('list'))

@app.route('/done/<int:id>')
def task_done(id):
    task = Task.get_by_id(id)
    if task and task.user == users.get_current_user():
        if task.done:
            task.done = False
        else:
            task.done = True
        task.put()
    else:
        abort(404)

    return redirect(url_for('list'))


# set the secret key.  keep this really secret:
app.secret_key = 'the secret key'

if __name__ == '__main__':
    app.run()
