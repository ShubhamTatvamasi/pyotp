# pyotp FastAPI Example


This is a minimal FastAPI app demonstrating [pyotp](https://pyauth.github.io/pyotp/) integration for Time-based One-Time Passwords (TOTP), with a full login experience using a QR code and OTP.


## Features
- Scan QR code in authenticator app (Google Authenticator, Authy, etc) ✅
- Enter OTP to login ✅
- API endpoints for secret, OTP, and verification ✅


## Endpoints
- `/` — Home page: scan QR, enter OTP to login
- `/qrcode` — PNG QR code for scanning
- `GET /generate-secret` — Returns the TOTP secret (base32)
- `GET /get-otp` — Returns the current OTP (for demo/testing)
- `POST /verify-otp` — Verifies an OTP. JSON body: `{ "otp": "123456" }`


## Running Locally

```bash
# Build the Docker image
docker build -t pyotp-demo .

# Run the container
docker run --rm -p 3000:3000 pyotp-demo
```

Or run locally with Python and uvicorn:

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 3000
```

## Example Usage

1. Open [http://localhost:3000/](http://localhost:3000/) in your browser
   - Scan the QR code in your authenticator app
   - Enter the OTP from your app to login

2. API Endpoints:
   - Get the secret:
     ```bash
     curl http://localhost:3000/generate-secret
     ```
   - Get the current OTP:
     ```bash
     curl http://localhost:3000/get-otp
     ```
   - Verify an OTP:
     ```bash
     curl -X POST -H "Content-Type: application/json" \
          -d '{"otp": "<otp>"}' \
          http://localhost:3000/verify-otp
     ```

## API Docs

FastAPI generates API documentation automatically from your code. When the server is running, open the following in your browser:

- **Swagger UI (interactive)**: `http://localhost:3000/docs` ✅
- **Redoc (read-only)**: `http://localhost:3000/redoc` ✅
- **OpenAPI JSON**: `http://localhost:3000/openapi.json`

These docs reflect your Pydantic models, `response_model` annotations, example values, and endpoint descriptions. To hide or move these endpoints in production, create the app with `FastAPI(docs_url=None, redoc_url=None, openapi_url=None)` or set custom paths.

