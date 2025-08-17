import requests
import json
import time
from typing import Optional

# Configuración
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

class NotesiaAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.test_note_id: Optional[str] = None
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log de resultados de tests"""
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⏭️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   {details}")
        print()
    
    def make_request(self, method: str, endpoint: str, data: dict = None, auth: bool = True):
        """Realizar petición HTTP con manejo de errores"""
        url = f"{API_BASE}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if auth and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=headers, timeout=30)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, headers=headers, timeout=30)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers, timeout=30)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")
            
            return response
        except requests.exceptions.Timeout:
            print(f"Timeout al conectar con {url}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"Error de conexión con {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error de petición: {e}")
            return None
    
    def test_health_check(self):
        """Test del endpoint de health check"""
        response = requests.get(f"{BASE_URL}/health")
        if response and response.status_code == 200:
            self.log_test("Health Check", "PASS", f"Status: {response.json()}")
            return True
        else:
            self.log_test("Health Check", "FAIL", f"Status code: {response.status_code if response else 'No response'}")
            return False
    
    def test_docs_availability(self):
        """Test de disponibilidad de documentación"""
        docs_response = requests.get(f"{BASE_URL}/docs")
        openapi_response = requests.get(f"{BASE_URL}/openapi.json")
        
        docs_ok = docs_response and docs_response.status_code == 200
        openapi_ok = openapi_response and openapi_response.status_code == 200
        
        if docs_ok and openapi_ok:
            self.log_test("Documentación API", "PASS", "Swagger UI y OpenAPI JSON disponibles")
            return True
        else:
            self.log_test("Documentación API", "FAIL", f"Docs: {docs_response.status_code if docs_response else 'Error'}, OpenAPI: {openapi_response.status_code if openapi_response else 'Error'}")
            return False
    
    def test_user_registration(self):
        """Test de registro de usuario"""
        test_user = {
            "email": f"test_{int(time.time())}@notesiaaaa.com",
            "password": "TestPassword123!",
            "full_name": "Usuario de Prueba",
            "username": f"testuser_{int(time.time())}"
        }
        
        response = self.make_request("POST", "/auth/register", test_user, auth=False)
        
        if response is None:
            self.log_test("Registro de Usuario", "FAIL", "Error: Sin respuesta del servidor")
            return False, None
        elif response.status_code == 200 or response.status_code == 201:
            try:
                data = response.json()
                self.user_id = data.get("user_id")
                self.log_test("Registro de Usuario", "PASS", f"Usuario creado: {self.user_id}")
                return True, test_user
            except Exception as e:
                self.log_test("Registro de Usuario", "FAIL", f"Error al parsear respuesta: {e}")
                return False, None
        else:
            try:
                error_detail = response.json().get("detail", "Error desconocido")
            except:
                error_detail = f"HTTP {response.status_code}: {response.text[:100]}"
            print(f"   ❌ Status Code: {response.status_code}")
            print(f"   ❌ Response: {response.text}")
            self.log_test("Registro de Usuario", "FAIL", f"Error: {error_detail}")
            return False, None
    
    def test_user_login(self, user_credentials: dict):
        """Test de login de usuario"""
        login_data = {
            "email": user_credentials["email"],
            "password": user_credentials["password"]
        }
        
        response = self.make_request("POST", "/auth/login", login_data, auth=False)
        
        if response and response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access_token")
            self.log_test("Login de Usuario", "PASS", f"Token obtenido: {self.access_token[:20]}...")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Login de Usuario", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_get_current_user(self):
        """Test de obtener usuario actual"""
        response = self.make_request("GET", "/auth/me")
        
        if response and response.status_code == 200:
            user_data = response.json()
            self.log_test("Obtener Usuario Actual", "PASS", f"Usuario: {user_data.get('email')}")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Obtener Usuario Actual", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_create_note(self):
        """Test de creación de nota"""
        note_data = {
            "title": "Nota de Prueba",
            "content": "Este es el contenido de una nota de prueba para verificar la funcionalidad de la API.",
            "tags": ["test", "api", "notesia"],
            "status": "draft"
        }
        
        response = self.make_request("POST", "/notes", note_data)
        
        if response and response.status_code == 200:
            note = response.json()
            self.test_note_id = note.get("id")
            self.log_test("Crear Nota", "PASS", f"Nota creada: {self.test_note_id}")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Crear Nota", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_get_notes(self):
        """Test de obtener lista de notas"""
        response = self.make_request("GET", "/notes")
        
        if response and response.status_code == 200:
            notes = response.json()
            self.log_test("Listar Notas", "PASS", f"Notas encontradas: {len(notes)}")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Listar Notas", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_get_note_by_id(self):
        """Test de obtener nota por ID"""
        if not self.test_note_id:
            self.log_test("Obtener Nota por ID", "SKIP", "No hay nota de prueba disponible")
            return False
        
        response = self.make_request("GET", f"/notes/{self.test_note_id}")
        
        if response and response.status_code == 200:
            note = response.json()
            self.log_test("Obtener Nota por ID", "PASS", f"Nota: {note.get('title')}")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Obtener Nota por ID", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_update_note(self):
        """Test de actualización de nota"""
        if not self.test_note_id:
            self.log_test("Actualizar Nota", "SKIP", "No hay nota de prueba disponible")
            return False
        
        updated_data = {
            "title": "Nota de Prueba Actualizada",
            "content": "Contenido actualizado de la nota de prueba.",
            "tags": ["test", "api", "notesia", "updated"]
        }
        
        response = self.make_request("PUT", f"/notes/{self.test_note_id}", updated_data)
        
        if response and response.status_code == 200:
            note = response.json()
            self.log_test("Actualizar Nota", "PASS", f"Nota actualizada: {note.get('title')}")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Actualizar Nota", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_get_tags(self):
        """Test de obtener tags"""
        response = self.make_request("GET", "/notes/tags/list")
        
        if response and response.status_code == 200:
            tags = response.json()
            self.log_test("Obtener Tags", "PASS", f"Tags encontrados: {len(tags)}")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Obtener Tags", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_ai_chat(self):
        """Test de chat con IA"""
        chat_data = {
            "prompt": "Hola, ¿puedes ayudarme con mis notas?"
        }
        
        response = self.make_request("POST", "/ai/chat", chat_data)
        
        if response and response.status_code == 200:
            ai_response = response.json()
            self.log_test("Chat con IA", "PASS", f"Respuesta recibida: {len(ai_response.get('response', ''))} caracteres")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Chat con IA", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_ai_summarize(self):
        """Test de resumen con IA"""
        if not hasattr(self, 'test_note_id') or not self.test_note_id:
            self.log_test("Resumir con IA", "SKIP", "No hay nota de prueba disponible")
            return False
            
        summarize_data = {
            "note_id": self.test_note_id
        }
        
        response = self.make_request("POST", "/ai/summarize", summarize_data)
        
        if response and response.status_code == 200:
            summary = response.json()
            self.log_test("Resumir con IA", "PASS", f"Resumen generado: {len(summary.get('summary', ''))} caracteres")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Resumir con IA", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_ai_enhance(self):
        """Test de mejora de texto con IA"""
        if not hasattr(self, 'test_note_id') or not self.test_note_id:
            self.log_test("Mejorar Texto con IA", "SKIP", "No hay nota de prueba disponible")
            return False
            
        enhance_data = {
            "note_id": self.test_note_id,
            "enhancement_type": "improve"
        }
        
        response = self.make_request("POST", "/ai/enhance", enhance_data)
        
        if response and response.status_code == 200:
            enhanced = response.json()
            self.log_test("Mejorar Texto con IA", "PASS", f"Texto mejorado: {len(enhanced.get('enhanced_text', ''))} caracteres")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Mejorar Texto con IA", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_ai_generate(self):
        """Test de generación de contenido con IA"""
        generate_data = {
            "prompt": "Genera una nota sobre productividad personal"
        }
        
        response = self.make_request("POST", "/ai/generate", generate_data)
        
        if response and response.status_code == 200:
            generated = response.json()
            self.log_test("Generar Contenido con IA", "PASS", f"Contenido generado: {len(generated.get('generated_content', ''))} caracteres")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Generar Contenido con IA", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_ai_analyze_notes(self):
        """Test de análisis de notas con IA"""
        response = self.make_request("POST", "/ai/analyze-notes")
        
        if response and response.status_code == 200:
            analysis = response.json()
            self.log_test("Analizar Notas con IA", "PASS", f"Análisis completado: {len(analysis.get('analysis', ''))} caracteres")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Analizar Notas con IA", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_delete_note(self):
        """Test de eliminación de nota"""
        if not self.test_note_id:
            self.log_test("Eliminar Nota", "SKIP", "No hay nota de prueba disponible")
            return False
        
        response = self.make_request("DELETE", f"/notes/{self.test_note_id}")
        
        if response and response.status_code == 200:
            self.log_test("Eliminar Nota", "PASS", f"Nota eliminada: {self.test_note_id}")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Eliminar Nota", "FAIL", f"Error: {error_detail}")
            return False
    
    def test_logout(self):
        """Test de logout"""
        response = self.make_request("POST", "/auth/logout")
        
        if response and response.status_code == 200:
            self.access_token = None
            self.log_test("Logout", "PASS", "Sesión cerrada exitosamente")
            return True
        else:
            error_detail = response.json().get("detail", "Error desconocido") if response else "Sin respuesta"
            self.log_test("Logout", "FAIL", f"Error: {error_detail}")
            return False
    
    def run_all_tests(self):
        """Ejecutar todos los tests"""
        print("🚀 INICIANDO TESTS COMPLETOS DE LA API NOTESIA\n")
        print("=" * 60)
        
        results = []
        
        # Tests básicos
        print("📋 TESTS BÁSICOS")
        print("-" * 30)
        results.append(self.test_health_check())
        results.append(self.test_docs_availability())
        
        # Tests de autenticación
        print("🔐 TESTS DE AUTENTICACIÓN")
        print("-" * 30)
        registration_success, user_credentials = self.test_user_registration()
        results.append(registration_success)
        
        if registration_success and user_credentials:
            results.append(self.test_user_login(user_credentials))
            if self.access_token:
                results.append(self.test_get_current_user())
        
        # Tests de notas (solo si hay autenticación)
        if self.access_token:
            print("📝 TESTS DE NOTAS")
            print("-" * 30)
            results.append(self.test_create_note())
            results.append(self.test_get_notes())
            results.append(self.test_get_note_by_id())
            results.append(self.test_update_note())
            results.append(self.test_get_tags())
            
            # Tests de IA
            print("🤖 TESTS DE INTELIGENCIA ARTIFICIAL")
            print("-" * 30)
            results.append(self.test_ai_chat())
            results.append(self.test_ai_summarize())
            results.append(self.test_ai_enhance())
            results.append(self.test_ai_generate())
            results.append(self.test_ai_analyze_notes())
            
            # Cleanup
            print("🧹 LIMPIEZA")
            print("-" * 30)
            results.append(self.test_delete_note())
            results.append(self.test_logout())
        
        # Resumen final
        print("=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)
        
        passed = sum(1 for result in results if result)
        total = len(results)
        
        print(f"✅ Tests pasados: {passed}")
        print(f"❌ Tests fallidos: {total - passed}")
        print(f"📈 Porcentaje de éxito: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ¡TODOS LOS TESTS PASARON! La API está funcionando correctamente.")
        else:
            print(f"\n⚠️  {total - passed} tests fallaron. Revisa los errores arriba.")
        
        return passed == total

if __name__ == "__main__":
    tester = NotesiaAPITester()
    tester.run_all_tests()