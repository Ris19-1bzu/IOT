import asyncio
from sanic import Sanic
import sanic.response as sanic_response

from functions import videoProcessing
from identifier import Identifier

loop = asyncio.get_event_loop()
app = Sanic("CvLock")
identifier = Identifier()

@app.get("/")
async def index(request):
    return await sanic_response.file('index/index.html')

@app.route('/image/<uid>')
async def getImage(request, uid):
    img_loc = identifier.getImageLocation(uid)

    if not img_loc:
        return sanic_response.text('not valid')

    return await sanic_response.file(img_loc)


# панель управления разрешениями
@app.route('/access', methods=['GET', 'POST'])
async def allowed(request):
    if request.method == 'POST':  # POSTING a list of new users to add
        data = request.json
        if data is None:
            return sanic_response.text('нет данных')

        uid = None
        try:
            uid = data['uid']
        except Exception:
            return sanic_response.text('неверные данные')

        return sanic_response.text(identifier.toggleAccess(uid))

    return sanic_response.text('исп. POST ')


# удаление
@app.route('/delete', methods=['GET', 'POST'])
async def delete(request):
    if request.method == 'POST':
        data = request.json
        if data is None or type(data) is not list:
            return

        for user in data:
            identifier.delete(user)
        return sanic_response.text('удален')

    return sanic_response.text('исп. POST')


# установка допуска
@app.route('/set', methods=['POST'])
async def set(request):
    data = request.json
    if 'uid' not in data.keys():
        return sanic_response.text('необходим uid')
    if 'name' not in data.keys():
        return sanic_response.text('необходимо имя')

    identifier.setName(data['uid'], data['name'])

    return sanic_response.text('ok')

# вывод видеопотока
@app.route('/mainview')
async def view(request):
    return sanic_response.stream(identifier.stream, content_type='multipart/x-mixed-replace; boundary=frame')


@app.listener('after_server_start')
async def server_start(app, loop):
    asyncio.ensure_future(videoProcessing(identifier, False))


@app.listener('before_server_stop')
async def server_stop(app, loop):
    identifier.quit()
    
    

if __name__ == "__main__":

    app.static('/', './index')
    app.run(host='0.0.0.0', port='80')