from flask import Flask, render_template
import os

app = Flask(__name__)

# Krug's 1st Law: Don't Make Me Think. 
# This headless UI exists solely on the Pi's local hotspot for instant field calibration.
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tare', methods=['POST'])
def tare_scale():
    # In production, this IPC triggers the hardware layer to zero the HX711
    return {"status": "success", "message": "Scale reset to zero."}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)