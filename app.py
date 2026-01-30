from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel
import pyotp
import qrcode
import io
import uvicorn

app = FastAPI()

# Generate a base32 secret. In production, store this per user.
SECRET = pyotp.random_base32()
USER = "demo-user"  # For demo only
ISSUER = "PyOTPApp"

def get_totp():
    return pyotp.TOTP(SECRET)


# Home page: show QR and OTP login form (GET) and accept form submission (POST)
@app.get('/', response_class=HTMLResponse)
async def home_get():
    msg = ''
    html = f'''
    <h2>Scan QR Code in Authenticator App</h2>
    <img src="/qrcode" alt="QR Code"><br>
    <p>Secret: <b>{SECRET}</b></p>
    <form method="post" action="/">
        <label>Enter OTP from app:</label>
        <input name="otp" maxlength="6" required>
        <button type="submit">Login</button>
    </form>
    <div>{msg}</div>
    '''
    return HTMLResponse(content=html)

@app.post('/', response_class=HTMLResponse)
async def home_post(otp: str = Form(...)):
    totp = get_totp()
    if totp.verify(otp):
        msg = '<span style="color:green">Login successful!</span>'
    else:
        msg = '<span style="color:red">Invalid OTP. Try again.</span>'
    html = f'''
    <h2>Scan QR Code in Authenticator App</h2>
    <img src="/qrcode" alt="QR Code"><br>
    <p>Secret: <b>{SECRET}</b></p>
    <form method="post" action="/">
        <label>Enter OTP from app:</label>
        <input name="otp" maxlength="6" required>
        <button type="submit">Login</button>
    </form>
    <div>{msg}</div>
    '''
    return HTMLResponse(content=html)


# QR code for TOTP
@app.get('/qrcode')
async def qrcode_img():
    totp_uri = pyotp.totp.TOTP(SECRET).provisioning_uri(name=USER, issuer_name=ISSUER)
    img = qrcode.make(totp_uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')

# API: get secret
@app.get('/generate-secret')
async def generate_secret():
    return JSONResponse({'secret': SECRET})

# API: get current OTP (for demo/testing)
@app.get('/get-otp')
async def get_otp():
    totp = get_totp()
    otp = totp.now()
    return JSONResponse({'otp': otp})

# API: verify OTP
class OTPRequest(BaseModel):
    otp: str

@app.post('/verify-otp')
async def verify_otp(req: OTPRequest):
    totp = get_totp()
    valid = totp.verify(req.otp)
    return JSONResponse({'valid': valid})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3000)
