import web
from handle import Handle


# 定义 URL 路由
##
urls = (
    '/', 'Index',   # 主页
    '/hello', 'Hello',  # 另一个页面
    '/wx', 'Handle'
)

# 定义视图类
class Index:
    def GET(self):
        return "Hello, world!"

class Hello:
    def GET(self):
        return "Hello, this is another page!"

# 创建应用
app = web.application(urls, globals())

# 启动服务器
if __name__ == "__main__":
    from web.httpserver import runsimple
    runsimple(app.wsgifunc(), ("0.0.0.0", 8080))