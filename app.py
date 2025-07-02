from dotenv import load_dotenv
import os
load_dotenv()
from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Gmail 設定
GMAIL_ACCOUNT = os.getenv("GMAIL_ACCOUNT")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")  # 建議部署時改用環境變數

@app.route('/api/email', methods=['POST'])
def send_email():
    if 'pdf' not in request.files:
        return jsonify({"error": "缺少 PDF 檔案"}), 400

    pdf_file = request.files['pdf']
    name = request.form.get('name', '')
    phone = request.form.get('phone', '')
    line_id = request.form.get('line', '')

    pdf_bytes = pdf_file.read()

    msg = EmailMessage()
    msg['Subject'] = f"📨 法律意見書諮詢 - {name}"
    msg['From'] = GMAIL_ACCOUNT
    msg['To'] = GMAIL_ACCOUNT
    msg.set_content(f"""以下為用戶聯絡資訊:

姓名: {name}
電話: {phone}
LINE ID: {line_id}

請參閱附加的法律意見書 PDF 檔案。
""")

    msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename=secure_filename("法律意見書.pdf"))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
            smtp.send_message(msg)
        return jsonify({"status": "ok"})
    except Exception as e:
        print("📧 發送錯誤：", e)
        return jsonify({"error": "Email 發送失敗"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)