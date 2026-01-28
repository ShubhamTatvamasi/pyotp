import pyotp
import qrcode
import io
import base64
from flask import Flask, request, jsonify, send_file, render_template_string

app = Flask(__name__)


# Generate a base32 secret. In production, store this per user.
SECRET = pyotp.random_base32()
USER = "demo-user"  # For demo only
ISSUER = "PyOTPApp"

def get_totp():
    return pyotp.TOTP(SECRET)


# Home page: show QR and OTP login form
@app.route('/', methods=['GET', 'POST'])
def home():
    msg = ''
    if request.method == 'POST':
        otp = request.form.get('otp')
        totp = get_totp()
        if totp.verify(otp):
            msg = '<span style="color:green">Login successful!</span>'
        else:
            msg = '<span style="color:red">Invalid OTP. Try again.</span>'
    html = f'''
    <h2>Scan QR Code in Authenticator App</h2>
    <img src="/qrcode" alt="QR Code"><br>
    <p>Secret: <b>{SECRET}</b></p>
    <form method="post">
        <label>Enter OTP from app:</label>
        <input name="otp" maxlength="6" required>
        <button type="submit">Login</button>
    </form>
    <div>{msg}</div>
    '''
    return render_template_string(html)

# QR code for TOTP
@app.route('/qrcode')
def qrcode_img():
    totp_uri = pyotp.totp.TOTP(SECRET).provisioning_uri(name=USER, issuer_name=ISSUER)
    img = qrcode.make(totp_uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# API: get secret
@app.route('/generate-secret', methods=['GET'])
def generate_secret():
    return jsonify({'secret': SECRET})


# API: get current OTP (for demo/testing)
@app.route('/get-otp', methods=['GET'])
def get_otp():
    totp = get_totp()
    otp = totp.now()
    return jsonify({'otp': otp})


# API: verify OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    otp = data.get('otp')
    totp = get_totp()
    valid = totp.verify(otp)
    return jsonify({'valid': valid})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
