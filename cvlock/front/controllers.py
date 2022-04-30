from flask import Blueprint, render_template, Response, request
from cvlock.recog.capture import Capture, capture

module = Blueprint('panel', __name__)


@module.route('/', methods=['GET'])
@module.route('/panel', methods=['GET'])
def panel():
    return render_template('front/main.html')


@module.route('/video_feed')
def video_feed():
    c = Capture()
    return Response(c.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@module.route('/newUser', methods=['GET', 'POST'])
def newUser():

    states = {
        1: {'action': 'allow', 'translate': u'Пропустить'},
        2: {'action': 'deny', 'translate': u'Изгнать'},
    }

    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            capture = 1


    return render_template('front/new_user.html', states=states)

@module.route('/users', methods=['GET'])
def users():
    return  render_template('front/users.html')
