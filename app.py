from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Inicia la captura de la cámara
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Lee un frame de la cámara
        success, frame = camera.read()
        if not success:
            break
        else:
            # Convierte la imagen a formato JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Devuelve el frame como un stream de bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
