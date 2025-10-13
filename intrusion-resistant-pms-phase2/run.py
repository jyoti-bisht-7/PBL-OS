from flask import Flask, render_template

app = Flask(__name__, template_folder='gui/templates', static_folder='gui/static')

@app.route('/')
def dashboard():
    processes = [
        {'pid': 1234, 'name': 'idle', 'cpu': 5.0, 'memory': 30.0, 'priority': 'Normal', 'user': 'root'},
        {'pid': 9123, 'name': 'malware', 'cpu': 70.0, 'memory': 25.0, 'priority': 'High', 'user': 'user2'},
        # ... add more mock processes ...
    ]
    alerts = [
        {'time': '12:34:56', 'message': 'Fork bomb detected'},
        {'time': '12:35:01', 'message': 'CPU hog detected'},
    ]
    cpu_labels = ['10:00', '10:01', '10:02']
    cpu_data = [40, 55, 60]
    mem_labels = ['idle', 'malware', 'myapp']
    mem_data = [30, 25, 45]
    return render_template('dashboard.html',
                          processes=processes,
                          alerts=alerts,
                          cpu_labels=cpu_labels,
                          cpu_data=cpu_data,
                          mem_labels=mem_labels,
                          mem_data=mem_data)

if __name__ == '__main__':
    app.run(debug=True)