# Intrusion-Resistant Process Management System

## Overview
The Intrusion-Resistant Process Management System is designed to monitor and manage system processes, detect potential intrusions, and mitigate threats in real-time. This project aims to enhance system security by analyzing real system data and simulating attack scenarios.

## Features
- Real-time monitoring of system processes
- Intrusion detection based on CPU usage and process limits
- Automated mitigation actions for suspicious processes
- User-friendly dashboard for visualizing system metrics and alerts
- API endpoints for fetching active processes, CPU and memory usage, and intrusion alerts

## Project Structure
```
intrusion-resistant-pms-phase3
├── run.py                  # Entry point for the application
├── src                     # Source code for the application
│   ├── app.py              # Flask application instance and module initialization
│   ├── config.py           # Configuration settings for the application
│   ├── dashboard            # Dashboard routes and API endpoints
│   │   └── routes.py
│   ├── intrusion_detection   # Intrusion detection logic
│   │   └── detection.py
│   ├── mitigation           # Threat mitigation functions
│   │   └── mitigation.py
│   ├── simulator            # Simulator for process metrics and scheduling
│   │   ├── engine.py
│   │   ├── scheduler.py
│   │   └── system_resources.py
├── gui                     # Frontend files for the dashboard
│   ├── templates
│   │   └── dashboard.html   # HTML template for the dashboard
│   └── static
│       ├── css
│       │   └── styles.css   # CSS styles for the dashboard
│       └── js
│           └── chart.js     # JavaScript for dynamic dashboard updates
├── requirements.txt        # Python dependencies for the project
└── README.md               # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd intrusion-resistant-pms-phase3
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables as needed for configuration.

## Usage
1. Start the application:
   ```
   python run.py
   ```

2. Access the dashboard at `http://localhost:5000` in your web browser.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
