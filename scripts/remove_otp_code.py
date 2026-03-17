from pathlib import Path

# Remove mobile OTP route block from auth_router.py
path = Path("app/routers/auth_router.py")
lines = path.read_text(encoding="utf-8").splitlines(True)
start = None
end = None
for i, line in enumerate(lines):
    if start is None and "# MOBILE OTP (PHONE VERIFICATION)" in line:
        start = i
    if start is not None and "# LOGIN" in line:
        end = i
        break

if start is not None and end is not None:
    del lines[start:end]
    path.write_text("".join(lines), encoding="utf-8")
    print("Removed MOBILE OTP section from auth_router.py")
else:
    print("Could not find OTP section in auth_router.py (start/end):", start, end)

# Remove send_mobile_otp helper from email_service.py
path = Path("app/utils/email_service.py")
lines = path.read_text(encoding="utf-8").splitlines(True)
start = None
end = None
for i, line in enumerate(lines):
    if start is None and "# SEND OTP (SMS + FALLBACK EMAIL)" in line:
        start = i
    if start is not None and "# EMAIL TEMPLATES" in line:
        end = i
        break

if start is not None and end is not None:
    del lines[start:end]
    path.write_text("".join(lines), encoding="utf-8")
    print("Removed send_mobile_otp helper from email_service.py")
else:
    print("Could not find send_mobile_otp helper section (start/end):", start, end)
