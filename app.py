
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import mysql.connector 

app = Flask(__name__)
# them
app.secret_key = 'abc@123'

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="laptrinhweb"
    )


@app.route('/')
def login_page():
    return render_template('login.html')


def __get_user_row(username: str) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT id,password FROM users WHERE username='{username}';")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = __get_user_row(username=username)
    if user and user['password'] == password:
        # them
        session['username'] = username
        # end
        return jsonify({'success': True, 'message': 'Đăng nhập thành công!'})
    return jsonify({'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu.'})

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    # Check if user exists
    existing_user = __get_user_row(username=username)
    if existing_user:
        return jsonify({'success': False, 'message': 'Tên đăng nhập đã tồn tại.'})

    # Insert new user
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
    # them
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', username=session['username'])
    # end
    # return "Chao mung!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)



# test
# from flask import Flask, request, render_template, jsonify
# import mysql.connector

# app = Flask(__name__)

# def get_db_connection():
#     return mysql.connector.connect(
#         host="127.0.0.1",
#         user="root",
#         password="",
#         database="laptrinhweb"
#     )

# @app.route('/')
# def login_page():
#     return render_template('login.html')

# def __get_user_row(username: str) -> dict:
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute(f"SELECT id,password FROM users WHERE username='{username}';")
#     result = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return result

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     user = __get_user_row(username=username)
#     if user and user['password'] == password:
#         return jsonify({'success': True, 'message': 'Đăng nhập thành công!'})
#     return jsonify({'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu.'})

# @app.route('/register', methods=['POST'])
# def register():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     if not username or not password:
#         return jsonify({'success': False, 'message': 'Vui lòng nhập đầy đủ thông tin.'})

#     # Kiểm tra username đã tồn tại
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
#     existing_user = cursor.fetchone()

#     if existing_user:
#         cursor.close()
#         conn.close()
#         return jsonify({'success': False, 'message': 'Tên đăng nhập đã tồn tại.'})

#     # Chưa có user thì insert
#     try:
#         cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
#         conn.commit()
#         return jsonify({'success': True, 'message': 'Đăng ký thành công!'})
#     except mysql.connector.Error:
#         return jsonify({'success': False, 'message': 'Lỗi khi đăng ký.'})
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/dashboard')
# def dashboard():
#     return "Chào mừng!"

# if __name__ == '__main__':
#     app.run(debug=True)
