from flask import Blueprint, jsonify, render_template
from intrusion_detection.detection import check_intrusion_alerts
from simulator.scheduler import get_active_processes
from src.simulator import system_resources
import json

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/active-processes', methods=['GET'])
def active_processes():
    processes = get_active_processes()
    return jsonify(processes)

@dashboard_bp.route('/api/cpu-memory-usage', methods=['GET'])
def cpu_memory_usage():
    usage = system_resources.get_cpu_memory_usage()
    return jsonify(usage)

@dashboard_bp.route('/api/intrusion-alerts', methods=['GET'])
def intrusion_alerts():
    alerts = check_intrusion_alerts()
    return jsonify(alerts)

@dashboard_bp.route('/')
def dashboard():
    # Mock data for demonstration
    cpu_labels = ["10:00", "10:01", "10:02", "10:03", "10:04"]
    cpu_data = [30, 45, 50, 40, 60]
    mem_labels = ["idle", "malware", "myapp", "db"]
    mem_data = [30, 25, 40, 65]
    return render_template(
        'dashboard.html',
        cpu_labels=json.dumps(cpu_labels),
        cpu_data=json.dumps(cpu_data),
        mem_labels=json.dumps(mem_labels),
        mem_data=json.dumps(mem_data),
    )