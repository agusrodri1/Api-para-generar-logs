import logging
import logging.config
import os
from pythonjsonlogger import jsonlogger

def get_logging_config():
    """
    Configuración detallada de logging para el microservicio
    Genera logs en formato JSON optimizado para Wazuh
    """
    
    # Asegurar que el directorio de logs existe
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(name)s %(levelname)s %(pathname)s %(lineno)d %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'file_all': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f'{log_dir}/api_all.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'json'
            },
            'file_errors': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f'{log_dir}/api_errors.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'json'
            },
            'file_security': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f'{log_dir}/api_security.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'json'
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            }
        },
        'loggers': {
            'api_microservice': {
                'handlers': ['file_all', 'console'],
                'level': 'INFO',
                'propagate': False
            },
            'security': {
                'handlers': ['file_security', 'file_all'],
                'level': 'INFO',
                'propagate': False
            },
            'errors': {
                'handlers': ['file_errors', 'file_all'],
                'level': 'WARNING',
                'propagate': False
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['file_all', 'console']
        }
    }
    
    return config

def setup_custom_loggers():
    """
    Configura loggers específicos para diferentes tipos de eventos
    """
    logging.config.dictConfig(get_logging_config())
    
    # Loggers específicos
    api_logger = logging.getLogger('api_microservice')
    security_logger = logging.getLogger('security')
    error_logger = logging.getLogger('errors')
    
    return api_logger, security_logger, error_logger