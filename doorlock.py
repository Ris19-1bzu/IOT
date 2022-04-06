from sanic import Sanic
from sanic.response import text

app = Sanic("CvLock")

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")



if __name__ == "__main__":

    app.static('/', './index')
    app.run(host='0.0.0.0', port='80')