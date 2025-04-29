from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import mysql.connector
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

def create_app():
    app = Flask(__name__,
                static_folder='static',
                static_url_path='/static')

    app.secret_key = 'abc@123'


    def get_db_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="laptrinhweb"
        )

    def __get_user_row(username: str) -> dict:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT id,password FROM users WHERE username='{username}';")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    @app.route('/')
    def login_page():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login():
        username = request.json.get('username')
        password = request.json.get('password')
        user = __get_user_row(username=username)
        if user and user['password'] == password:
            session['username'] = username
            return jsonify({'success': True, 'message': 'Đăng nhập thành công!'})
        return jsonify({'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu.'})

    @app.route('/register')
    def register_page():
        return render_template('register.html')

    @app.route('/api/register', methods=['POST'])
    def register():
        username = request.json.get('username')
        password = request.json.get('password')
        existing_user = __get_user_row(username=username)
        if existing_user:
            return jsonify({'success': False, 'message': 'Tên đăng nhập đã tồn tại.'})
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            return jsonify({'success': True})
        except mysql.connector.Error:
            return jsonify({'success': False, 'message': 'Đăng ký thất bại!'})
        finally:
            cursor.close()
            conn.close()

    @app.route('/dashboard')
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('login_page'))
        return render_template('dashboard.html', username=session['username'])

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login_page'))

    return app



# Gắn app vào prefix /loginsys
application = DispatcherMiddleware(
    Flask('dummy'),  # root app không dùng
    {'/loginsys': create_app()}
)

if __name__ == '__main__':
    run_simple('127.0.0.1', 4000, application, use_reloader=True, use_debugger=True)