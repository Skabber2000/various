from flask import Flask, request, jsonify
import qrcode
import io
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the QR Code Generator!"

@app.route('/generate', methods=['POST'])
def generate_qr_code():
    data = request.json
    product_name = data.get('product_name')
    production_number = data.get('production_number')
    batch_release_date = data.get('batch_release_date')

    if not (product_name and production_number and batch_release_date):
        return jsonify({"error": "Missing required fields"}), 400

    # Generate QR code
    qr_data = f"Product name: {product_name}\nProduction: {production_number}\nBatch release date: {batch_release_date}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return (
        buffer.read(),
        200,
        {'Content-Type': 'image/png', 'Content-Disposition': 'inline; filename="qrcode.png"'}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
