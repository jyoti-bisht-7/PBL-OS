from flask import Flask
from src.dashboard.routes import dashboard_routes
from src.intrusion_detection.detection import IntrusionDetection
from src.mitigation.mitigation import MitigationModule
from src.simulator.scheduler import Scheduler
from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize modules
intrusion_detection = IntrusionDetection()
mitigation_module = MitigationModule()
scheduler = Scheduler()

# Register routes
app.register_blueprint(dashboard_routes)

@app.route('/')
def index():
    return "Welcome to the Intrusion-Resistant Process Management System"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)