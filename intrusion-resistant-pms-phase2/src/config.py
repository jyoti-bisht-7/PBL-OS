from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    INTRUSION_DETECTION_THRESHOLD = int(os.getenv('INTRUSION_DETECTION_THRESHOLD', 80))
    MITIGATION_ACTIONS = os.getenv('MITIGATION_ACTIONS', 'throttle,terminate').split(',')
    PROCESS_MONITOR_INTERVAL = int(os.getenv('PROCESS_MONITOR_INTERVAL', 5))  # in seconds
    MAX_MEMORY_USAGE = int(os.getenv('MAX_MEMORY_USAGE', 1024))  # in MB
    MAX_CPU_USAGE = int(os.getenv('MAX_CPU_USAGE', 80))  # in percentage