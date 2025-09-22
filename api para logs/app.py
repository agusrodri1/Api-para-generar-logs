from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import json
import os
from datetime import datetime
import uuid
from pythonjsonlogger import jsonlogger
from config.logging_config import setup_custom_loggers
from api_endpoints import api_bp

app = Flask(__name__)
CORS(app)

# Configurar logging personalizado
api_logger, security_logger, error_logger = setup_custom_loggers()

# Registrar blueprint de API
app.register_blueprint(api_bp)

@app.before_request
def log_request_info():
    """Log de cada request que llega a la API"""
    request_id = str(uuid.uuid4())
    request.request_id = request_id
    
    api_logger.info("Incoming request", extra={
        "event_type": "api_request",
        "request_id": request_id,
        "method": request.method,
        "endpoint": request.endpoint,
        "remote_addr": request.remote_addr,
        "user_agent": request.headers.get('User-Agent', ''),
        "content_type": request.headers.get('Content-Type', ''),
        "timestamp": datetime.now().isoformat()
    })

@app.after_request
def log_response_info(response):
    """Log de cada response que devuelve la API"""
    api_logger.info("Outgoing response", extra={
        "event_type": "api_response",
        "request_id": getattr(request, 'request_id', 'unknown'),
        "status_code": response.status_code,
        "content_length": response.content_length,
        "timestamp": datetime.now().isoformat()
    })
    return response

@app.route('/')
def home():
    """Endpoint principal de la API"""
    api_logger.info("Home endpoint accessed", extra={
        "event_type": "endpoint_access",
        "endpoint": "/",
        "request_id": getattr(request, 'request_id', 'unknown')
    })
    
    return jsonify({
        "message": "API de Logs - Microservicio para Monitoreo con Wazuh",
        "version": "1.0.0",
        "status": "active",
        "endpoints": [
            "/health",
            "/api/user/login",
            "/api/user/register",
            "/api/data/process",
            "/api/system/error",
            "/api/system/warning"
        ]
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    api_logger.info("Health check performed", extra={
        "event_type": "health_check",
        "status": "healthy",
        "request_id": getattr(request, 'request_id', 'unknown')
    })
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running"
    })

if __name__ == '__main__':
    api_logger.info("Starting API microservice", extra={
        "event_type": "application_start",
        "port": 5000,
        "debug": True
    })
    
    app.run(debug=True, host='0.0.0.0', port=5000)