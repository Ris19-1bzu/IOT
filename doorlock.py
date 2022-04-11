from sanic import Sanic
import sanic.response as sanic_response

app = Sanic("CvLock")

@app.get("/")
async def index(request):
    return await sanic_response.file('index/index.html')



if __name__ == "__main__":

    app.static('/', './index')
    app.run(host='0.0.0.0', port='80')