import requests
import json
import time
from typing import Dict, Any

# Configuración para el test de Vercel
BASE_URL = "https://notesia.vercel.app/api"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Variables globales para el test
test_user_data = {
    "username": f"testuser_vercel_{int(time.time())}",
    "email": f"testuser_vercel_{int(time.time())}@example.com",
    "password": "testpassword123"
}

auth_token = None
test_note_id = None

def print_test_result(test_name: str, success: bool, message: str = ""):
    """Imprime el resultado de un test con formato"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if message:
        print(f"    {message}")
    print()

def make_request(method: str, endpoint: str, data: Dict[Any, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
    """Realiza una petición HTTP con manejo de errores"""
    url = f"{BASE_URL}{endpoint}"
    request_headers = HEADERS.copy()
    if headers:
        request_headers.update(headers)
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=request_headers, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=request_headers, timeout=30)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=request_headers, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=request_headers, timeout=30)
        else:
            raise ValueError(f"Método HTTP no soportado: {method}")
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición: {e}")
        raise

def test_health_check():
    """Test 1: Verificar que la API esté funcionando"""
    try:
        # El endpoint de health está en la raíz, no en /api
        url = "https://notesia.vercel.app/health"
        response = requests.get(url, headers=HEADERS, timeout=30)
        success = response.status_code == 200
        message = f"Status: {response.status_code}"
        if success:
            try:
                data = response.json()
                message += f", Response: {data}"
            except:
                message += f", Response: {response.text}"
        print_test_result("Health Check", success, message)
        return success
    except Exception as e:
        print_test_result("Health Check", False, f"Error: {str(e)}")
        return False

def test_docs_access():
    """Test 2: Verificar acceso a la documentación"""
    try:
        # El endpoint de docs está en la raíz, no en /api
        url = "https://notesia.vercel.app/docs"
        response = requests.get(url, headers=HEADERS, timeout=30)
        success = response.status_code in [200, 307]  # 307 es redirect
        message = f"Status: {response.status_code}"
        print_test_result("Docs Access", success, message)
        return success
    except Exception as e:
        print_test_result("Docs Access", False, f"Error: {str(e)}")
        return False

def test_user_registration():
    """Test 3: Registro de usuario"""
    try:
        response = make_request("POST", "/auth/register", test_user_data)
        success = response.status_code in [200, 201]
        message = f"Status: {response.status_code}"
        if not success:
            try:
                error_data = response.json()
                message += f", Error: {error_data}"
            except:
                message += f", Response: {response.text}"
        print_test_result("User Registration", success, message)
        return success
    except Exception as e:
        print_test_result("User Registration", False, f"Error: {str(e)}")
        return False

def test_user_login():
    """Test 4: Login de usuario"""
    global auth_token
    try:
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = make_request("POST", "/auth/login", login_data)
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                auth_token = data.get("access_token")
                if auth_token:
                    message = "Login exitoso, token obtenido"
                else:
                    success = False
                    message = "Login exitoso pero no se obtuvo token"
            except:
                success = False
                message = "Respuesta inválida del servidor"
        else:
            try:
                error_data = response.json()
                message = f"Status: {response.status_code}, Error: {error_data}"
            except:
                message = f"Status: {response.status_code}, Response: {response.text}"
        
        print_test_result("User Login", success, message)
        return success
    except Exception as e:
        print_test_result("User Login", False, f"Error: {str(e)}")
        return False

def test_get_user_info():
    """Test 5: Obtener información del usuario autenticado"""
    if not auth_token:
        print_test_result("Get User Info", False, "No hay token de autenticación")
        return False
    
    try:
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("GET", "/auth/me", headers=auth_headers)
        success = response.status_code == 200
        
        message = f"Status: {response.status_code}"
        if success:
            try:
                data = response.json()
                message += f", User: {data.get('username', 'N/A')}"
            except:
                message += ", Respuesta inválida"
        
        print_test_result("Get User Info", success, message)
        return success
    except Exception as e:
        print_test_result("Get User Info", False, f"Error: {str(e)}")
        return False

def test_create_note():
    """Test 6: Crear una nota"""
    global test_note_id
    if not auth_token:
        print_test_result("Create Note", False, "No hay token de autenticación")
        return False
    
    try:
        note_data = {
            "title": "Nota de prueba Vercel",
            "content": "Este es el contenido de una nota de prueba para verificar la funcionalidad de la API en Vercel.",
            "tags": ["test", "vercel", "api"]
        }
        
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("POST", "/notes", note_data, auth_headers)
        success = response.status_code in [200, 201]
        
        if success:
            try:
                data = response.json()
                test_note_id = data.get("id")
                message = f"Nota creada con ID: {test_note_id}"
            except:
                message = "Nota creada pero respuesta inválida"
        else:
            try:
                error_data = response.json()
                message = f"Status: {response.status_code}, Error: {error_data}"
            except:
                message = f"Status: {response.status_code}, Response: {response.text}"
        
        print_test_result("Create Note", success, message)
        return success
    except Exception as e:
        print_test_result("Create Note", False, f"Error: {str(e)}")
        return False

def test_list_notes():
    """Test 7: Listar notas del usuario"""
    if not auth_token:
        print_test_result("List Notes", False, "No hay token de autenticación")
        return False
    
    try:
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("GET", "/notes", headers=auth_headers)
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                notes_count = len(data) if isinstance(data, list) else 0
                message = f"Se obtuvieron {notes_count} notas"
            except:
                message = "Respuesta inválida del servidor"
        else:
            message = f"Status: {response.status_code}"
        
        print_test_result("List Notes", success, message)
        return success
    except Exception as e:
        print_test_result("List Notes", False, f"Error: {str(e)}")
        return False

def test_get_note_by_id():
    """Test 8: Obtener nota por ID"""
    if not auth_token or not test_note_id:
        print_test_result("Get Note by ID", False, "No hay token o ID de nota")
        return False
    
    try:
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("GET", f"/notes/{test_note_id}", headers=auth_headers)
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                message = f"Nota obtenida: {data.get('title', 'Sin título')}"
            except:
                message = "Nota obtenida pero respuesta inválida"
        else:
            message = f"Status: {response.status_code}"
        
        print_test_result("Get Note by ID", success, message)
        return success
    except Exception as e:
        print_test_result("Get Note by ID", False, f"Error: {str(e)}")
        return False

def test_update_note():
    """Test 9: Actualizar nota"""
    if not auth_token or not test_note_id:
        print_test_result("Update Note", False, "No hay token o ID de nota")
        return False
    
    try:
        updated_data = {
            "title": "Nota actualizada Vercel",
            "content": "Contenido actualizado para verificar la funcionalidad de actualización en Vercel.",
            "tags": ["test", "vercel", "updated"]
        }
        
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("PUT", f"/notes/{test_note_id}", updated_data, auth_headers)
        success = response.status_code == 200
        
        message = f"Status: {response.status_code}"
        if success:
            try:
                data = response.json()
                message += f", Título actualizado: {data.get('title', 'N/A')}"
            except:
                message += ", Actualización exitosa"
        
        print_test_result("Update Note", success, message)
        return success
    except Exception as e:
        print_test_result("Update Note", False, f"Error: {str(e)}")
        return False

def test_get_note_tags():
    """Test 10: Obtener tags de notas"""
    if not auth_token:
        print_test_result("Get Note Tags", False, "No hay token de autenticación")
        return False
    
    try:
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("GET", "/notes/tags", headers=auth_headers)
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                tags_count = len(data) if isinstance(data, list) else 0
                message = f"Se obtuvieron {tags_count} tags únicos"
            except:
                message = "Respuesta inválida del servidor"
        else:
            message = f"Status: {response.status_code}"
        
        print_test_result("Get Note Tags", success, message)
        return success
    except Exception as e:
        print_test_result("Get Note Tags", False, f"Error: {str(e)}")
        return False

def test_ai_chat():
    """Test 11: Chat con IA"""
    if not auth_token:
        print_test_result("AI Chat", False, "No hay token de autenticación")
        return False
    
    try:
        chat_data = {
            "prompt": "Hola, ¿puedes ayudarme a generar ideas para un proyecto?"
        }
        
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("POST", "/ai/chat", chat_data, auth_headers)
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                response_text = data.get("response", "")
                message = f"IA respondió: {response_text[:50]}..." if len(response_text) > 50 else f"IA respondió: {response_text}"
            except:
                message = "Respuesta de IA recibida pero formato inválido"
        else:
            try:
                error_data = response.json()
                message = f"Status: {response.status_code}, Error: {error_data}"
            except:
                message = f"Status: {response.status_code}"
        
        print_test_result("AI Chat", success, message)
        return success
    except Exception as e:
        print_test_result("AI Chat", False, f"Error: {str(e)}")
        return False

def test_ai_summarize():
    """Test 12: Resumir texto con IA"""
    if not auth_token or not test_note_id:
        print_test_result("AI Summarize", False, "No hay token o ID de nota")
        return False
    
    try:
        summarize_data = {
            "note_id": test_note_id
        }
        
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("POST", "/ai/summarize", summarize_data, auth_headers)
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                summary = data.get("ai_summary", "")
                message = f"Resumen generado: {summary[:50]}..." if len(summary) > 50 else f"Resumen: {summary}"
            except:
                message = "Resumen generado pero formato inválido"
        else:
            message = f"Status: {response.status_code}"
        
        print_test_result("AI Summarize", success, message)
        return success
    except Exception as e:
        print_test_result("AI Summarize", False, f"Error: {str(e)}")
        return False

def test_ai_enhance():
    """Test 13: Mejorar texto con IA"""
    if not auth_token or not test_note_id:
        print_test_result("AI Enhance", False, "No hay token o ID de nota")
        return False
    
    try:
        enhance_data = {
            "note_id": test_note_id,
            "enhancement_type": "improve"
        }
        
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("POST", "/ai/enhance", enhance_data, auth_headers)
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                enhanced = data.get("ai_enhanced_content", "")
                message = f"Texto mejorado: {enhanced[:50]}..." if len(enhanced) > 50 else f"Texto mejorado: {enhanced}"
            except:
                message = "Texto mejorado pero formato inválido"
        else:
            message = f"Status: {response.status_code}"
        
        print_test_result("AI Enhance", success, message)
        return success
    except Exception as e:
        print_test_result("AI Enhance", False, f"Error: {str(e)}")
        return False

def test_ai_generate():
    """Test 14: Generar contenido con IA"""
    if not auth_token:
        print_test_result("AI Generate", False, "No hay token de autenticación")
        return False
    
    try:
        generate_data = {
            "prompt": "Genera una idea creativa para una aplicación móvil"
        }
        
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("POST", "/ai/generate", generate_data, auth_headers)
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                content = data.get("content", "")
                message = f"Contenido generado: {content[:50]}..." if len(content) > 50 else f"Contenido: {content}"
            except:
                message = "Contenido generado pero formato inválido"
        else:
            message = f"Status: {response.status_code}"
        
        print_test_result("AI Generate", success, message)
        return success
    except Exception as e:
        print_test_result("AI Generate", False, f"Error: {str(e)}")
        return False

def test_ai_analyze_notes():
    """Test 15: Analizar notas con IA"""
    if not auth_token:
        print_test_result("AI Analyze Notes", False, "No hay token de autenticación")
        return False
    
    try:
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("POST", "/ai/analyze-notes", {}, auth_headers)
        success = response.status_code == 200
        
        if success:
            try:
                data = response.json()
                analysis = data.get("insights", "")
                message = f"Análisis generado: {analysis[:50]}..." if len(analysis) > 50 else f"Análisis: {analysis}"
            except:
                message = "Análisis generado pero formato inválido"
        else:
            message = f"Status: {response.status_code}"
        
        print_test_result("AI Analyze Notes", success, message)
        return success
    except Exception as e:
        print_test_result("AI Analyze Notes", False, f"Error: {str(e)}")
        return False

def test_delete_note():
    """Test 16: Eliminar nota"""
    if not auth_token or not test_note_id:
        print_test_result("Delete Note", False, "No hay token o ID de nota")
        return False
    
    try:
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("DELETE", f"/notes/{test_note_id}", headers=auth_headers)
        success = response.status_code in [200, 204]
        
        message = f"Status: {response.status_code}"
        if success:
            message += ", Nota eliminada exitosamente"
        
        print_test_result("Delete Note", success, message)
        return success
    except Exception as e:
        print_test_result("Delete Note", False, f"Error: {str(e)}")
        return False

def test_logout():
    """Test 17: Logout de usuario"""
    if not auth_token:
        print_test_result("User Logout", False, "No hay token de autenticación")
        return False
    
    try:
        auth_headers = {"Authorization": f"Bearer {auth_token}"}
        response = make_request("POST", "/auth/logout", {}, auth_headers)
        success = response.status_code == 200
        
        message = f"Status: {response.status_code}"
        if success:
            message += ", Logout exitoso"
        
        print_test_result("User Logout", success, message)
        return success
    except Exception as e:
        print_test_result("User Logout", False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Ejecuta todos los tests y muestra un resumen"""
    print("🚀 INICIANDO TESTS DE LA API DE NOTESIA EN VERCEL")
    print(f"📍 URL Base: {BASE_URL}")
    print(f"👤 Usuario de prueba: {test_user_data['username']}")
    print("=" * 60)
    print()
    
    # Lista de todos los tests
    tests = [
        ("Tests Básicos", [
            test_health_check,
            test_docs_access
        ]),
        ("Tests de Autenticación", [
            test_user_registration,
            test_user_login,
            test_get_user_info
        ]),
        ("Tests de Notas", [
            test_create_note,
            test_list_notes,
            test_get_note_by_id,
            test_update_note,
            test_get_note_tags
        ]),
        ("Tests de Inteligencia Artificial", [
            test_ai_chat,
            test_ai_summarize,
            test_ai_enhance,
            test_ai_generate,
            test_ai_analyze_notes
        ]),
        ("Tests de Limpieza", [
            test_delete_note,
            test_logout
        ])
    ]
    
    total_tests = 0
    passed_tests = 0
    
    # Ejecutar tests por categoría
    for category, test_functions in tests:
        print(f"📋 {category}")
        print("-" * 40)
        
        category_passed = 0
        category_total = len(test_functions)
        
        for test_func in test_functions:
            total_tests += 1
            if test_func():
                passed_tests += 1
                category_passed += 1
        
        print(f"📊 {category}: {category_passed}/{category_total} tests pasados")
        print()
    
    # Resumen final
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print("=" * 60)
    print(f"📈 RESUMEN FINAL")
    print(f"✅ Tests pasados: {passed_tests}/{total_tests}")
    print(f"📊 Porcentaje de éxito: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 ¡Todos los tests pasaron! La API está funcionando correctamente en Vercel.")
    elif success_rate >= 80:
        print("✨ La mayoría de tests pasaron. La API está mayormente funcional.")
    elif success_rate >= 50:
        print("⚠️ Algunos tests fallaron. Revisar la funcionalidad de la API.")
    else:
        print("❌ Muchos tests fallaron. La API tiene problemas significativos.")
    
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()