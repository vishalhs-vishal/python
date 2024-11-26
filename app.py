from flask import Flask, request, render_template, send_file, redirect, url_for
import qrcode
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.form.get('data')
    if not data:
        return redirect(url_for('home'))

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code to an in-memory file
    global qr_buffer
    qr_buffer = BytesIO()
    img.save(qr_buffer)
    qr_buffer.seek(0)

    # Store the QR code in session for later download
    return render_template('result.html')

@app.route('/download')
def download_qr():
    try:
        global qr_buffer
        if qr_buffer is None:
            return redirect(url_for('home'))
        # Ensure buffer is still open for download
        qr_buffer.seek(0)
        return send_file(qr_buffer, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
    except Exception as e:
        print(f"Error during download: {e}")
        return redirect(url_for('home'))

if __name__ == '__main__':
    # Get port from environment variable or use default 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
