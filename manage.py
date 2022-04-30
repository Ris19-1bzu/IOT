from flask_script import Manager, Server
from cvlock.models import User
from config import Config
from cvlock import create_app, db

app = create_app()
app.config.from_object(Config)
manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port='5010'))


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == '__main__':
    manager.run()