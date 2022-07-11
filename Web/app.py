import requests
from flask import Flask,render_template

app = Flask(__name__)

# data_list = list(DWdb_url.CrawlingInfo_URL.fine()) # index.html 에 존재하는 태그로 넘길 데이터 
# 리턴 함수 리다이렉션 함수로 수정해야함
@app.route("/")
def index():
    return render_template('index.html') # 페이지 경로 설정 

@app.route('/login')
def login():
    return render_template('login.html') # 각 페이지들에 대해 경로 설정

@app.route('/light_Sidenav')
def light_Sidenav():
    return render_template('layout-sidenav-light.html')

@app.route('/static_Navigation')
def static_Navigation():
    return render_template('layout-static.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

def menu():
    return render_template('menu.html')

@app.route('/401')
def error_401():
    return render_template('401.html')

@app.route('/404')
def error_404():
    return render_template('404.html')

@app.route('/500')
def error_500():
    return render_template('500.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/password')
def password():
    return render_template('password.html')

# @app.route('/post', methods=['GET', ['POST']])
# def post():
#     if requests.method == 'POST':
#         value = requests.form['id_name']
#         value = str(value)
#         print(value)
#     return render_template('post.html') # 해당 html 수정 필요 


if __name__ == '__main__': ## 서버 실행
    app.run(host = '0.0.0.0', debug=True)
