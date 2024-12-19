from flask import Flask, request, render_template, redirect, url_for
import datetime
from flask import Flask, session, redirect, url_for, request, render_template
from flask_session import Session

app = Flask(__name__)

# Cấu hình session
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'your_secret_key'  # Khóa bí mật để mã hóa session
Session(app)

# Load initial data
with open("Data.txt", "r", encoding="utf-8") as file:
    money = [int(line.strip()) for line in file][0]

account_number = 1234
password = 123456789
name = "Đỗ Minh Quân"

# Function to log transactions
def log_transaction(action, amount=0, target_account=None):
    with open("TransactionLogs.txt", "a", encoding="utf-8") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if action == "transfer":
            log_file.write(f"{timestamp}: Transferred {amount} VND to {target_account}\n")
        elif action == "withdraw":
            log_file.write(f"{timestamp}: Withdrew {amount} VND\n")
        elif action == "deposit":
            log_file.write(f"{timestamp}: Deposited {amount} VND\n")
        elif action == "login":
            log_file.write(f"{timestamp}: Successful login\n")

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    global money
    entered_password = int(request.form['password'])
    if entered_password == password:
        log_transaction("login")
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Sai mật khẩu. Vui lòng thử lại!")
"""
@app.route('/dashboard')
def dashboard():
    with open("TransactionLogs.txt", "r", encoding="utf-8") as log_file:
        logs = log_file.readlines()
    return render_template('dashboard.html', name=name, money=money, logs=logs)
"""
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:  # Kiểm tra nếu người dùng chưa đăng nhập
        return redirect(url_for('login'))  # Chuyển hướng về trang đăng nhập

    # Nếu đã đăng nhập, hiển thị dashboard
    with open("TransactionLogs.txt", "r", encoding="utf-8") as log_file:
        logs = log_file.readlines()
    return render_template('dashboard.html', name=name, money=money, logs=logs)



@app.route('/total_money')
def total_money():
    return f"Hiện tại, {name} có {money} VND!", 200

@app.route('/transfer_money', methods=['POST'])
def transfer_money():
    global money
    amount = int(request.form['amount'])
    account_name = request.form['account_name']
    if amount > money:
        return render_template('dashboard.html', name=name, money=money, error="Số tiền vượt quá số dư hiện tại!")
    money -= amount
    log_transaction("transfer", amount, account_name)
    with open("TransactionLogs.txt", "r", encoding="utf-8") as log_file:
        logs = log_file.readlines()
    return render_template('dashboard.html', name=name, money=money, message=f"Đã chuyển thành công {amount} VND cho {account_name}!", logs=logs)

@app.route('/money_out', methods=['POST'])
def money_out():
    global money
    amount = int(request.form['amount'])
    if amount > money:
        return render_template('dashboard.html', name=name, money=money, error="Số tiền vượt quá số dư hiện tại!")
    money -= amount
    log_transaction("withdraw", amount)
    with open("TransactionLogs.txt", "r", encoding="utf-8") as log_file:
        logs = log_file.readlines()
    return render_template('dashboard.html', name=name, money=money, message=f"Đã rút thành công {amount} VND!", logs=logs)

@app.route('/money_in', methods=['POST'])
def money_in():
    global money
    amount = int(request.form['amount'])
    money += amount
    log_transaction("deposit", amount)
    with open("TransactionLogs.txt", "r", encoding="utf-8") as log_file:
        logs = log_file.readlines()
    return render_template('dashboard.html', name=name, money=money, message=f"Đã nạp thành công {amount} VND vào tài khoản!", logs=logs)
"""
@app.route('/exit')
def exit():
    with open("Data.txt", "w", encoding="utf-8") as file:
        file.write(f"{money}")
    return "Cảm ơn bạn đã sử dụng dịch vụ!", 200

"""
@app.route('/exit')
def exit():
    global money
    # Save the current balance to the file
    with open("Data.txt", "w", encoding="utf-8") as file:
        file.write(f"{money}")
    
    # Optionally, clear the session or authentication data if you were using sessions
    
    session.clear()  # Uncomment if using sessions for login
     
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    entered_password = int(request.form['password'])
    if entered_password == password:
        session['logged_in'] = True  # Lưu trạng thái đăng nhập vào session
        log_transaction("login")
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Sai mật khẩu. Vui lòng thử lại!")




if __name__ == '__main__':
    app.run(debug=True)
