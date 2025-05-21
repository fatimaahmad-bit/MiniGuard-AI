# MiniGuard-AI

MiniGuard-AI is a real-time child safety monitoring system designed to detect dangerous objects near children. It triggers alarms and sends email notifications to parents. The system is built using YOLO object detection, Flask, and integrated with email services to ensure child safety in various environments.

## Features

- Real-time Monitoring: Detect dangerous objects near children (e.g., knives, scissors, coins).
- Alarm System: Triggers an alarm when a dangerous object is detected.
- Email Alerts: Sends email notifications to the parent’s email when a dangerous object is detected.
- YOLO Model: Uses YOLO object detection for accurate and fast object detection.

## Requirements

Before you start, make sure to install the following:

1. Python 3.x
2. Install dependencies via requirements.txt.

```bash
pip install -r requirements.txt

Dependencies:

- opencv-python: For video capture and image processing.

- ultralytics: YOLOv5 object detection model.

- Flask: Web framework for running the backend.

- playsound: For playing alarm sounds.

- smtplib: To send email notifications.

- email: For composing email messages.

- numpy: For mathematical operations.


Setup

1. Clone the repository:
git clone https://github.com/your-username/MiniGuard-AI.git
cd MiniGuard-AI

2. Install dependencies:
pip install -r requirements.txt

3. Place your YOLO model weights (best.pt) and alarm sound file (e.g., alarm.mp3) in the project directory.

4. Configure your email settings in miniguardai.py (sender email, recipient email, app password).


## Running the Application

To start the system:
- Run the backend using cmd.
- Start the GUI.py file and run it.
- Click the START MONITORING button. 
Now,
The system will start detecting objects through your webcam.

If a dangerous object is detected near the child, an alarm will sound, and an email notification will be sent.


## Troubleshooting

Ensure your webcam is working.

Make sure the email configurations are correct.

Verify that the best.pt model file is in the correct path.


## License

This project is licensed under the MIT License - see the LICENSE file for details.
