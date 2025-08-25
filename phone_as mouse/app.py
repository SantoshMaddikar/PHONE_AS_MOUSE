from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_cors import CORS
import pyautogui
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder="templates")
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

CORS(app)

# Configuration
MOUSE_SPEED_MULTIPLIER = 2.0  # Adjust this for mouse speed
DOUBLE_TAP_SCALING = 1.2  # Adjust this for double-tap accuracy

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('connect')
def handle_connect():
    logger.info('Client connected: %s', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Client disconnected: %s', request.sid)

@socketio.on('mousemove')
def handle_mouse_move(data):
    try:
        dx = data.get('dx', 0) * MOUSE_SPEED_MULTIPLIER
        dy = data.get('dy', 0) * MOUSE_SPEED_MULTIPLIER
        pyautogui.moveRel(dx, dy, _pause=False)
    except Exception as e:
        logger.error("Mouse move error: %s", str(e))

@socketio.on('leftclick')
def handle_left_click():
    try:
        pyautogui.click()
    except Exception as e:
        logger.error("Left click error: %s", str(e))

@socketio.on('rightclick')
def handle_right_click():
    try:
        pyautogui.rightClick()
    except Exception as e:
        logger.error("Right click error: %s", str(e))

@socketio.on('doubleclick_position')
def handle_double_click(data):
    try:
        # Just perform a double-click at the current cursor position
        pyautogui.doubleClick()
        logger.info("Double-click performed at current cursor position")
    except Exception as e:
        logger.error(f"Double click error: {str(e)}")
if __name__ == '__main__':
    try:
        pyautogui.FAILSAFE = False
        logger.info("Starting server...")
        socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.critical("Critical error: %s", str(e))
