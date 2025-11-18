import sys, os
sys.path.append(os.path.dirname(__file__))
from utils.console_utils import imprimir_banner, solicitar_entrada, confirmar_accion, Color
from utils.validators import validar_cedula
from services.captcha_solver import CaptchaSolver
from services.selenium_service import SeleniumService
from models.results import ConsultaResult
from config.settings import URL_CONSULTA, RECAPTCHA_SITEKEY

class ConsultaJuradosApp:
    
    def __init__(self):
        self.captcha_solver = CaptchaSolver()
        self.selenium_service = None
    
    def ejecutar(self):

        try:
            imprimir_banner()
            
            # Verificar dependencias
            if not self._verificar_dependencias():
                sys.exit(1)
            
            # Bucle principal
            while True:
                cedula = self._solicitar_cedula()
                if not cedula:
                    break
                
                resultado = self._realizar_consulta(cedula)
                self._mostrar_resultado(resultado)
                
                if not self._preguntar_continuar():
                    break
            
            print(f"\n{Color.OKGREEN}¡Gracias por usar el sistema!{Color.ENDC}")
            
        except KeyboardInterrupt:
            print(f"\n{Color.WARNING}Programa interrumpido por el usuario.{Color.ENDC}")
        except Exception as e:
            print(f"\n{Color.FAIL}Error inesperado: {e}{Color.ENDC}")
        finally:
            if self.selenium_service:
                self.selenium_service.cerrar_navegador()
    
    def _verificar_dependencias(self) -> bool:

        print(f"{Color.OKCYAN}Verificando dependencias...{Color.ENDC}")
        
        # Verificar API key de Anti-Captcha
        if not self.captcha_solver.verificar_api_key():
            return False
        
        # Verificar que Selenium puede iniciarse
        self.selenium_service = SeleniumService(headless=False)
        if not self.selenium_service.iniciar_navegador():
            return False
        
        print(f"{Color.OKGREEN}✓ Todas las dependencias verificadas{Color.ENDC}\n")
        return True
    
    def _solicitar_cedula(self) -> str:

        intentos = 0
        max_intentos = 3
        
        while intentos < max_intentos:
            cedula = solicitar_entrada("Ingrese el número de cédula a consultar: ")
            
            if not cedula:  # Usuario canceló
                return None
            
            # Validar formato
            es_valida, mensaje = validar_cedula(cedula)
            if not es_valida:
                print(f"{Color.FAIL}✗ {mensaje}{Color.ENDC}")
                intentos += 1
                continue
            
            # Confirmar
            if confirmar_accion(f"¿Consultar la cédula {cedula}?"):
                return cedula
            else:
                print(f"{Color.WARNING}Consulta cancelada.{Color.ENDC}")
                intentos += 1
        
        print(f"{Color.FAIL}Máximo de intentos alcanzado.{Color.ENDC}")
        return None
    
    def _realizar_consulta(self, cedula: str) -> ConsultaResult:

        print(f"\n{Color.HEADER}{'='*70}")
        print(f"INICIANDO CONSULTA PARA: {cedula}")
        print(f"{'='*70}{Color.ENDC}\n")
        
        try:
            # Paso 1: Cargar página
            if not self.selenium_service.cargar_pagina(URL_CONSULTA):
                return ConsultaResult(
                    exito=False,
                    mensaje="Error cargando la página de consulta"
                )
            
            # Paso 2: Ingresar cédula
            if not self.selenium_service.ingresar_cedula(cedula):
                return ConsultaResult(
                    exito=False,
                    mensaje="Error ingresando la cédula"
                )
            
            # Paso 3: Resolver reCAPTCHA
            captcha_token = self.captcha_solver.resolver_recaptcha(
                URL_CONSULTA, 
                RECAPTCHA_SITEKEY
            )
            if not captcha_token:
                return ConsultaResult(
                    exito=False,
                    mensaje="Error resolviendo el reCAPTCHA"
                )
            
            # Paso 4: Inyectar solución del captcha
            if not self.selenium_service.inyectar_solucion_captcha(captcha_token):
                return ConsultaResult(
                    exito=False,
                    mensaje="Error aplicando la solución del captcha"
                )
            
            # Paso 5: Enviar formulario
            if not self.selenium_service.enviar_formulario():
                return ConsultaResult(
                    exito=False,
                    mensaje="Error enviando el formulario"
                )
            
            # Paso 6: Obtener y analizar resultado
            resultado_texto = self.selenium_service.obtener_resultado()
            
            return self._analizar_resultado(cedula, resultado_texto)
            
        except Exception as e:
            self.selenium_service.tomar_screenshot("error_consulta.png")
            return ConsultaResult(
                exito=False,
                mensaje=f"Error durante la consulta: {str(e)}"
            )
    
    def _analizar_resultado(self, cedula: str, texto: str) -> ConsultaResult:
      
        if not texto:
            return ConsultaResult(
                exito=False,
                mensaje="No se recibió respuesta del servidor"
            )
        
        texto_lower = texto.lower()
        
        if "no ha sido designado" in texto_lower or "no figura" in texto_lower:
            return ConsultaResult(
                exito=True,
                es_jurado=False,
                mensaje=f"La cédula {cedula} NO ha sido designada como jurado",
                detalle=texto,
                cedula=cedula
            )
        elif "ha sido designado" in texto_lower:
            return ConsultaResult(
                exito=True,
                es_jurado=True,
                mensaje=f"¡ATENCIÓN! La cédula {cedula} SÍ es jurado de votación",
                detalle=texto,
                cedula=cedula
            )
        elif "por favor digite" in texto_lower:
            return ConsultaResult(
                exito=False,
                mensaje="El formulario no se procesó correctamente",
                detalle="Posible problema con el captcha o la sesión"
            )
        else:
            return ConsultaResult(
                exito=True,
                mensaje="Respuesta recibida del servidor",
                detalle=texto,
                cedula=cedula
            )
    
    def _mostrar_resultado(self, resultado: ConsultaResult):

        print(f"\n{Color.HEADER}{'='*70}")
        print("RESULTADO DE LA CONSULTA")
        print(f"{'='*70}{Color.ENDC}\n")
        
        if resultado.exito:
            if resultado.es_jurado is not None:
                if resultado.es_jurado:
                    print(f"{Color.OKGREEN}✓ {resultado.mensaje}{Color.ENDC}\n")
                    print(f"{Color.WARNING}INFORMACIÓN IMPORTANTE:{Color.ENDC}")
                    print(f"  • Presentarse a las 7:30 AM")
                    print(f"  • Llevar cédula original")
                    print(f"  • Ubicarse en la mesa asignada")
                else:
                    print(f"{Color.OKCYAN}ℹ {resultado.mensaje}{Color.ENDC}")
            else:
                print(f"{Color.OKGREEN}✓ {resultado.mensaje}{Color.ENDC}")
            
            if resultado.detalle:
                print(f"\n{Color.BOLD}Detalles:{Color.ENDC}")
                print(f"{Color.WARNING}{'-'*70}")
                print(resultado.detalle)
                print(f"{'-'*70}{Color.ENDC}")
        else:
            print(f"{Color.FAIL}✗ {resultado.mensaje}{Color.ENDC}")
        
        print(f"\n{Color.HEADER}{'='*70}{Color.ENDC}\n")
    
    def _preguntar_continuar(self) -> bool:

        while True:
            respuesta = solicitar_entrada(
                "¿Desea realizar otra consulta? (S/N): "
            ).upper()
            
            if respuesta in ['S', 'SI', 'Y', 'YES']:
                return True
            elif respuesta in ['N', 'NO']:
                return False
            else:
                print(f"{Color.WARNING}Por favor responda SÍ o NO{Color.ENDC}")

def main():

    app = ConsultaJuradosApp()
    app.ejecutar()

if __name__ == "__main__":
    main()