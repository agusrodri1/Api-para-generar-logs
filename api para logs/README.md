# API de Logs - Microservicio para Monitoreo con Wazuh

Este proyecto implementa una API sencilla en Python Flask que genera logs estructurados para ser monitoreados con Wazuh. Es ideal para aprender sobre monitoreo de microservicios y análisis de logs de seguridad.

## 📋 Características

- **API REST** con endpoints que simulan diferentes escenarios
- **Logs estructurados en JSON** optimizados para Wazuh
- **Diferentes niveles de logging** (INFO, WARNING, ERROR)
- **Eventos de seguridad** (autenticación, intentos de acceso)
- **Logs de sistema** (errores, warnings, métricas de rendimiento)
- **Configuración completa de Wazuh** incluida

## 🚀 Instalación y Configuración

### Requisitos

- Python 3.8+
- pip
- Wazuh Agent instalado (para monitoreo)

### 1. Clonar y configurar el proyecto

```bash
# Navegar al directorio del proyecto
cd "api para logs"

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar la API

```bash
# Modo desarrollo
python app.py

# Modo producción
gunicorn --bind 0.0.0.0:5000 app:app
```

La API estará disponible en `http://localhost:5000`

## 📡 Endpoints Disponibles

### Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información general de la API |
| `/health` | GET | Health check del servicio |

### Endpoints de Usuario

| Endpoint | Método | Descripción | Logs Generados |
|----------|--------|-------------|----------------|
| `/api/user/login` | POST | Simula login de usuario | Eventos de autenticación |
| `/api/user/register` | POST | Simula registro de usuario | Eventos de gestión de usuarios |

### Endpoints de Sistema

| Endpoint | Método | Descripción | Logs Generados |
|----------|--------|-------------|----------------|
| `/api/data/process` | POST | Simula procesamiento de datos | Eventos de procesamiento |
| `/api/system/error` | GET | Genera errores del sistema | Logs de errores críticos |
| `/api/system/warning` | GET | Genera warnings del sistema | Logs de warnings |

## 🔍 Ejemplos de Uso

### 1. Login de Usuario

```bash
curl -X POST http://localhost:5000/api/user/login \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario_test", "password": "password123"}'
```

### 2. Procesar Datos

```bash
curl -X POST http://localhost:5000/api/data/process \
  -H "Content-Type: application/json" \
  -d '{"data": "información a procesar"}'
```

### 3. Generar Error del Sistema

```bash
curl http://localhost:5000/api/system/error
```

## 📊 Logs Generados

La API genera logs en formato JSON en el directorio `logs/`:

- **`api_all.log`**: Todos los logs de la aplicación
- **`api_errors.log`**: Solo logs de errores y warnings
- **`api_security.log`**: Solo eventos de seguridad

### Ejemplo de Log JSON

```json
{
  "asctime": "2024-01-15 10:30:45",
  "name": "security",
  "levelname": "INFO",
  "pathname": "/app/api_endpoints.py",
  "lineno": 25,
  "message": "User login successful",
  "event_type": "user_authentication",
  "action": "login",
  "status": "success",
  "username": "usuario_test",
  "request_id": "abc123-def456",
  "source_ip": "192.168.1.100",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## ⚙️ Configuración de Wazuh

### 1. Configuración del Agente

Edita el archivo `/var/ossec/etc/ossec.conf` en el agente de Wazuh:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/ruta/a/tu/api/logs/api_all.log</location>
  <label key="log_type">api_microservice</label>
  <label key="service">api_logs</label>
</localfile>

<localfile>
  <log_format>json</log_format>
  <location>/ruta/a/tu/api/logs/api_errors.log</location>
  <label key="log_type">api_errors</label>
  <label key="service">api_logs</label>
  <label key="severity">high</label>
</localfile>

<localfile>
  <log_format>json</log_format>
  <location>/ruta/a/tu/api/logs/api_security.log</location>
  <label key="log_type">api_security</label>
  <label key="service">api_logs</label>
  <label key="security">true</label>
</localfile>
```

### 2. Reglas Personalizadas

Copia el archivo `config/wazuh_rules.xml` a `/var/ossec/etc/rules/` en el servidor Wazuh.

### 3. Decodificadores Personalizados

Copia el archivo `config/wazuh_decoders.xml` a `/var/ossec/etc/decoders/` en el servidor Wazuh.

### 4. Reiniciar Servicios

```bash
# En el agente
sudo systemctl restart wazuh-agent

# En el servidor
sudo systemctl restart wazuh-manager
```

## 🔧 Tipos de Eventos Monitoreados

### Eventos de Seguridad
- **Autenticación exitosa**: Login correcto
- **Autenticación fallida**: Credenciales incorrectas
- **Usuario no encontrado**: Intento de login con usuario inexistente
- **Cuenta bloqueada**: Intento de acceso a cuenta bloqueada
- **Múltiples intentos fallidos**: Detección de ataques de fuerza bruta

### Eventos del Sistema
- **Errores críticos**: Fallas de base de datos, memoria, etc.
- **Warnings**: Uso alto de CPU, tiempo de respuesta lento
- **Procesamiento de datos**: Éxito/fallo en procesamiento
- **Health checks**: Estado del servicio

### Eventos de Aplicación
- **Requests**: Todas las peticiones HTTP
- **Responses**: Todas las respuestas HTTP
- **Errores de aplicación**: Excepciones no manejadas
- **Inicio/parada**: Ciclo de vida de la aplicación

## 🎯 Casos de Uso para Wazuh

### 1. Detección de Ataques de Fuerza Bruta
La regla `100010` detecta múltiples intentos de login fallidos del mismo usuario.

### 2. Monitoreo de Errores Críticos
La regla `100006` alerta sobre errores de alta severidad del sistema.

### 3. Actividad Sospechosa
La regla `100014` detecta alta frecuencia de requests desde una sola IP.

### 4. Compliance y Auditoría
Los logs incluyen campos compatibles con PCI DSS para auditorías de seguridad.

## 📈 Dashboard y Alertas

### Métricas Recomendadas
- Número de requests por minuto
- Tasa de errores (4xx, 5xx)
- Intentos de autenticación fallidos
- Tiempo de respuesta promedio
- Uso de recursos del sistema

### Alertas Críticas
- Múltiples intentos de login fallidos
- Errores de sistema de alta severidad
- Actividad sospechosa (DoS)
- Cuentas bloqueadas
- Fallas en servicios externos

## 🛠️ Desarrollo y Personalización

### Añadir Nuevos Endpoints

1. Edita `api_endpoints.py`
2. Añade el nuevo endpoint con logging apropiado
3. Actualiza las reglas de Wazuh si es necesario

### Personalizar Logs

1. Modifica `config/logging_config.py` para nuevos formatos
2. Añade campos adicionales en los logs JSON
3. Actualiza los decodificadores de Wazuh

## 🐛 Troubleshooting

### Problema: Los logs no aparecen en Wazuh

**Solución:**
1. Verifica que las rutas en `ossec.conf` sean correctas
2. Comprueba permisos de lectura en los archivos de log
3. Revisa el log del agente: `/var/ossec/logs/ossec.log`

### Problema: Reglas no se activan

**Solución:**
1. Verifica que las reglas estén en `/var/ossec/etc/rules/`
2. Comprueba la sintaxis XML
3. Reinicia el servidor Wazuh

### Problema: Formato JSON incorrecto

**Solución:**
1. Verifica la configuración de `pythonjsonlogger`
2. Comprueba que `log_format` sea `json` en Wazuh
3. Valida el JSON de los logs generados

## 📝 Licencia

MIT License - Ver archivo LICENSE para detalles.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📧 Soporte

Para preguntas o soporte, por favor abre un issue en el repositorio.

---

**¡Disfruta monitoreando tu microservicio con Wazuh!** 🚀