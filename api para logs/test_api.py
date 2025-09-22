#!/usr/bin/env python3
"""
Script de ejemplo para probar la API de Logs
Genera diferentes tipos de eventos para demostrar el monitoreo con Wazuh
"""

import requests
import json
import time
import random
from datetime import datetime

API_BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, data=None, description=""):
    """Función helper para probar endpoints"""
    print(f"\n🔄 {description}")
    print(f"   {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(f"{API_BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(
                f"{API_BASE_URL}{endpoint}",
                json=data,
                headers={"Content-Type": "application/json"}
            )
        
        print(f"   Status: {response.status_code}")
        if response.headers.get('content-type', '').startswith('application/json'):
            print(f"   Response: {response.json()}")
        else:
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Error: No se pudo conectar a la API. ¿Está ejecutándose?")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def simulate_user_activity():
    """Simula actividad normal de usuarios"""
    print("\n📊 SIMULANDO ACTIVIDAD DE USUARIOS")
    
    usernames = ["juan_perez", "maria_garcia", "admin", "test_user", "developer"]
    
    for i in range(5):
        username = random.choice(usernames)
        
        # Registro de usuario
        test_endpoint(
            "POST", 
            "/api/user/register",
            {"username": username, "email": f"{username}@example.com"},
            f"Registro de usuario #{i+1}"
        )
        
        time.sleep(1)
        
        # Login de usuario (la mayoría exitosos)
        password = "password123" if random.random() < 0.8 else "wrong_password"
        test_endpoint(
            "POST",
            "/api/user/login", 
            {"username": username, "password": password},
            f"Login de usuario #{i+1}"
        )
        
        time.sleep(1)

def simulate_data_processing():
    """Simula procesamiento de datos"""
    print("\n🔄 SIMULANDO PROCESAMIENTO DE DATOS")
    
    for i in range(3):
        test_data = {
            "operation": "process_batch",
            "data": [f"record_{j}" for j in range(random.randint(10, 100))],
            "priority": random.choice(["high", "medium", "low"])
        }
        
        test_endpoint(
            "POST",
            "/api/data/process",
            test_data,
            f"Procesamiento de datos #{i+1}"
        )
        
        time.sleep(2)

def simulate_system_events():
    """Simula eventos del sistema"""
    print("\n⚠️  SIMULANDO EVENTOS DEL SISTEMA")
    
    # Generar algunos warnings
    for i in range(2):
        test_endpoint(
            "GET",
            "/api/system/warning",
            description=f"Warning del sistema #{i+1}"
        )
        time.sleep(1)
    
    # Generar algunos errores
    for i in range(2):
        test_endpoint(
            "GET", 
            "/api/system/error",
            description=f"Error del sistema #{i+1}"
        )
        time.sleep(1)

def simulate_brute_force_attack():
    """Simula un ataque de fuerza bruta"""
    print("\n🚨 SIMULANDO ATAQUE DE FUERZA BRUTA")
    
    target_user = "admin"
    passwords = ["123456", "password", "admin", "qwerty", "letmein", "password123"]
    
    for i, password in enumerate(passwords):
        test_endpoint(
            "POST",
            "/api/user/login",
            {"username": target_user, "password": password},
            f"Intento de fuerza bruta #{i+1} - {target_user}:{password}"
        )
        time.sleep(0.5)  # Rápido para simular ataque automatizado

def perform_health_checks():
    """Realiza health checks"""
    print("\n💚 REALIZANDO HEALTH CHECKS")
    
    test_endpoint("GET", "/", description="Endpoint principal")
    test_endpoint("GET", "/health", description="Health check")

def main():
    """Función principal del script de prueba"""
    print("🚀 INICIANDO PRUEBAS DE LA API DE LOGS")
    print("=" * 50)
    
    # Verificar que la API esté funcionando
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        print(f"✅ API está funcionando (Status: {response.status_code})")
    except:
        print("❌ Error: La API no está disponible en http://localhost:5000")
        print("   Asegúrate de ejecutar: python app.py")
        return
    
    # Ejecutar diferentes tipos de pruebas
    perform_health_checks()
    
    simulate_user_activity()
    
    simulate_data_processing()
    
    simulate_system_events()
    
    # Advertencia antes del ataque de fuerza bruta
    print("\n" + "="*50)
    print("⚠️  ATENCIÓN: El siguiente test simulará un ataque de fuerza bruta")
    print("   Esto generará múltiples alertas en Wazuh")
    input("   Presiona Enter para continuar o Ctrl+C para cancelar...")
    
    simulate_brute_force_attack()
    
    print("\n" + "="*50)
    print("✅ PRUEBAS COMPLETADAS")
    print("📋 Revisa los siguientes archivos de log:")
    print("   - logs/api_all.log")
    print("   - logs/api_errors.log") 
    print("   - logs/api_security.log")
    print("🔍 Revisa las alertas en tu dashboard de Wazuh")
    print("=" * 50)

if __name__ == "__main__":
    main()