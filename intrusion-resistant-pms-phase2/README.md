# Intrusion-Resistant Process Management System - Phase 2

## Overview
The Intrusion-Resistant Process Management System (IRPMS) Phase 2 is a comprehensive simulator that integrates operating system scheduling concepts with advanced cybersecurity defense mechanisms. This project aims to provide a robust framework for managing processes while ensuring system integrity against potential intrusions.

## Features
- **Flask Backend**: A lightweight web framework that serves as the backbone of the application, handling requests and responses.
- **Intrusion Detection Module**: Monitors system behavior to identify suspicious activities based on CPU and memory usage patterns, process creation rates, and waiting times.
- **Mitigation Module**: Implements strategies to manage malicious processes by adjusting their priority or terminating them when they exceed predefined limits.
- **GUI Dashboard**: A user-friendly interface that displays real-time data on active processes, resource usage, and alerts related to potential intrusions.

## Project Structure
```
intrusion-resistant-pms-phase2
├── src
│   ├── app.py
│   ├── simulator
│   │   ├── __init__.py
│   │   └── scheduler.py
│   ├── intrusion_detection
│   │   ├── __init__.py
│   │   └── detection.py
│   ├── mitigation
│   │   ├── __init__.py
│   │   └── mitigation.py
│   ├── dashboard
│   │   ├── __init__.py
│   │   └── routes.py
│   └── config.py
├── requirements.txt
├── README.md
└── run.py
```

## Setup Instructions
1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd intrusion-resistant-pms-phase2
   ```

2. **Install Dependencies**: 
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the Application**: 
   Start the Flask application by executing:
   ```
   python run.py
   ```

4. **Access the Dashboard**: 
   Open your web browser and navigate to `http://localhost:5000` to access the GUI dashboard.

## Usage
- Monitor active processes and their resource usage.
- View alerts for any detected intrusions.
- Adjust process priorities and manage system resources effectively.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.