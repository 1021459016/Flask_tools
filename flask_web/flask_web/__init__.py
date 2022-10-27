from  flask import  Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII']=False
from  .views import  python_tools
app.register_blueprint(python_tools.ts)
