from flask import Blueprint, request, jsonify
import logging
import random
import time
from datetime import datetime
import uuid

# Crear blueprint para los endpoints de API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Loggers específicos
api_logger = logging.getLogger('api_microservice')
security_logger = logging.getLogger('security')
error_logger = logging.getLogger('errors')

@api_bp.route('/user/login', methods=['POST'])
def user_login():
    """Simula login de usuario - genera logs de seguridad"""
    try:
        data = request.get_json() or {}
        username = data.get('username', 'unknown')
        password = data.get('password', '')
        
        # Simular diferentes escenarios de login
        scenarios = ['success', 'invalid_password', 'user_not_found', 'account_locked']
        scenario = random.choice(scenarios)
        
        request_id = getattr(request, 'request_id', str(uuid.uuid4()))
        
        if scenario == 'success':
            security_logger.info("User login successful", extra={
                "event_type": "user_authentication",
                "action": "login",
                "status": "success",
                "username": username,
                "request_id": request_id,
                "source_ip": request.remote_addr,
                "user_agent": request.headers.get('User-Agent', ''),
                "timestamp": datetime.now().isoformat(),
                "session_id": str(uuid.uuid4())
            })
            
            return jsonify({
                "status": "success",
                "message": "Login successful",
                "session_id": str(uuid.uuid4()),
                "user": username
            }), 200
            
        elif scenario == 'invalid_password':
            security_logger.warning("Invalid password attempt", extra={
                "event_type": "user_authentication",
                "action": "login",
                "status": "failed",
                "failure_reason": "invalid_password",
                "username": username,
                "request_id": request_id,
                "source_ip": request.remote_addr,
                "user_agent": request.headers.get('User-Agent', ''),
                "timestamp": datetime.now().isoformat()
            })
            
            return jsonify({
                "status": "error",
                "message": "Invalid credentials"
            }), 401
            
        elif scenario == 'user_not_found':
            security_logger.warning("Login attempt for non-existent user", extra={
                "event_type": "user_authentication",
                "action": "login",
                "status": "failed",
                "failure_reason": "user_not_found",
                "username": username,
                "request_id": request_id,
                "source_ip": request.remote_addr,
                "user_agent": request.headers.get('User-Agent', ''),
                "timestamp": datetime.now().isoformat()
            })
            
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404
            
        else:  # account_locked
            security_logger.error("Login attempt on locked account", extra={
                "event_type": "user_authentication",
                "action": "login",
                "status": "blocked",
                "failure_reason": "account_locked",
                "username": username,
                "request_id": request_id,
                "source_ip": request.remote_addr,
                "user_agent": request.headers.get('User-Agent', ''),
                "timestamp": datetime.now().isoformat(),
                "security_alert": True
            })
            
            return jsonify({
                "status": "error",
                "message": "Account is locked"
            }), 423
            
    except Exception as e:
        error_logger.error("Error in login endpoint", extra={
            "event_type": "application_error",
            "error_type": "login_exception",
            "error_message": str(e),
            "request_id": getattr(request, 'request_id', 'unknown'),
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

@api_bp.route('/user/register', methods=['POST'])
def user_register():
    """Simula registro de usuario"""
    try:
        data = request.get_json() or {}
        username = data.get('username', 'unknown')
        email = data.get('email', 'unknown')
        
        request_id = getattr(request, 'request_id', str(uuid.uuid4()))
        
        # Simular registro exitoso
        api_logger.info("User registration", extra={
            "event_type": "user_management",
            "action": "register",
            "status": "success",
            "username": username,
            "email": email,
            "request_id": request_id,
            "source_ip": request.remote_addr,
            "timestamp": datetime.now().isoformat(),
            "user_id": str(uuid.uuid4())
        })
        
        return jsonify({
            "status": "success",
            "message": "User registered successfully",
            "user_id": str(uuid.uuid4())
        }), 201
        
    except Exception as e:
        error_logger.error("Error in register endpoint", extra={
            "event_type": "application_error",
            "error_type": "registration_exception",
            "error_message": str(e),
            "request_id": getattr(request, 'request_id', 'unknown'),
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "status": "error",
            "message": "Registration failed"
        }), 500

@api_bp.route('/data/process', methods=['POST'])
def process_data():
    """Simula procesamiento de datos"""
    try:
        data = request.get_json() or {}
        processing_time = random.uniform(0.1, 2.0)
        time.sleep(processing_time)
        
        request_id = getattr(request, 'request_id', str(uuid.uuid4()))
        
        # Simular diferentes escenarios de procesamiento
        if random.random() < 0.8:  # 80% éxito
            api_logger.info("Data processing completed", extra={
                "event_type": "data_processing",
                "action": "process",
                "status": "success",
                "processing_time_seconds": round(processing_time, 3),
                "data_size": len(str(data)),
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "records_processed": random.randint(1, 1000)
            })
            
            return jsonify({
                "status": "success",
                "message": "Data processed successfully",
                "processing_time": round(processing_time, 3),
                "records_processed": random.randint(1, 1000)
            }), 200
        else:  # 20% fallo
            error_logger.warning("Data processing failed", extra={
                "event_type": "data_processing",
                "action": "process",
                "status": "failed",
                "processing_time_seconds": round(processing_time, 3),
                "data_size": len(str(data)),
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "error_reason": "data_validation_failed"
            })
            
            return jsonify({
                "status": "error",
                "message": "Data validation failed"
            }), 400
            
    except Exception as e:
        error_logger.error("Error in data processing", extra={
            "event_type": "application_error",
            "error_type": "data_processing_exception",
            "error_message": str(e),
            "request_id": getattr(request, 'request_id', 'unknown'),
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "status": "error",
            "message": "Processing failed"
        }), 500

@api_bp.route('/system/error', methods=['GET'])
def trigger_error():
    """Endpoint para simular errores del sistema"""
    request_id = getattr(request, 'request_id', str(uuid.uuid4()))
    
    error_types = [
        ("database_connection_failed", "Database connection timeout"),
        ("memory_limit_exceeded", "Memory usage exceeded 90%"),
        ("external_service_unavailable", "External API service unreachable"),
        ("disk_space_low", "Disk space below 5%")
    ]
    
    error_type, error_message = random.choice(error_types)
    
    error_logger.error("System error triggered", extra={
        "event_type": "system_error",
        "error_type": error_type,
        "error_message": error_message,
        "request_id": request_id,
        "timestamp": datetime.now().isoformat(),
        "severity": "high",
        "component": "system"
    })
    
    return jsonify({
        "status": "error",
        "type": error_type,
        "message": error_message
    }), 500

@api_bp.route('/system/warning', methods=['GET'])
def trigger_warning():
    """Endpoint para simular warnings del sistema"""
    request_id = getattr(request, 'request_id', str(uuid.uuid4()))
    
    warning_types = [
        ("high_cpu_usage", "CPU usage above 80%"),
        ("slow_response_time", "Response time above 2 seconds"),
        ("cache_miss_rate_high", "Cache miss rate above 50%"),
        ("connection_pool_low", "Connection pool usage above 85%")
    ]
    
    warning_type, warning_message = random.choice(warning_types)
    
    api_logger.warning("System warning triggered", extra={
        "event_type": "system_warning",
        "warning_type": warning_type,
        "warning_message": warning_message,
        "request_id": request_id,
        "timestamp": datetime.now().isoformat(),
        "severity": "medium",
        "component": "system"
    })
    
    return jsonify({
        "status": "warning",
        "type": warning_type,
        "message": warning_message
    }), 200