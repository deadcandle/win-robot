from flask import Flask, jsonify, request
from PIL import ImageGrab
import numpy as np
import pyautogui

app = Flask(__name__)

# Function to capture and resize the screen
def capture_screen(resize_factor=1):
    # Capture the screen using Pillow's ImageGrab
    screenshot = ImageGrab.grab()

    # Calculate new dimensions based on the resize factor (e.g., 0.5 for 50% of the original size)
    width, height = screenshot.size
    new_width = int(width * resize_factor)
    new_height = int(height * resize_factor)

    # Resize the image
    screenshot_resized = screenshot.resize((new_width, new_height))

    # Convert the resized image to an RGB numpy array
    img_array = np.array(screenshot_resized)
    
    # Convert the numpy array to a list of lists (RGB tuples)
    pixel_data = img_array.tolist()
    
    return pixel_data

# Endpoint to get the screen data with a resize option
@app.route('/screenshot', methods=['GET'])
def screenshot():
    # You can adjust the resize factor here. For example, 0.2 will give 20% of the original resolution.
    resize_factor = 0.03  # Resize the image to 20% of its original size
    pixel_data = capture_screen(resize_factor)
    return jsonify({"pixels": pixel_data})

# Endpoint to handle mouse click actions and keystrokes
@app.route('/action', methods=['POST'])
def action():
    data = request.get_json()

    # Get mouse position and type of action (click, move, or keystroke)
    x = data.get('x')
    y = data.get('y')
    action_type = data.get('action')  # 'click', 'move', or 'keypress'
    key = data.get('key')  # Key to press (for 'keypress' action)
    
    if action_type == 'click':
        pyautogui.click(x, y)  # Simulate mouse click
    elif action_type == 'move':
        pyautogui.moveTo(x, y)  # Simulate mouse move
    elif action_type == 'keypress' and key:
        pyautogui.press(key)  # Simulate key press
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)  # Run the server on all IP addresses
