
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from config.settings import SELENIUM_TIMEOUT, WAIT_TIME
from utils.console_utils import Color

class SeleniumService:
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = None
        self.wait = None
    
    def iniciar_navegador(self) -> bool:
 
        try:
            print(f"{Color.OKCYAN}Iniciando navegador...{Color.ENDC}")
            
            chrome_options = Options()
            
            # Configuración para evitar detección
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, SELENIUM_TIMEOUT)
            
            print(f"{Color.OKGREEN}✓ Navegador iniciado{Color.ENDC}")
            return True
            
        except Exception as e:
            print(f"{Color.FAIL}✗ Error iniciando navegador: {e}{Color.ENDC}")
            return False
    
    def cargar_pagina(self, url: str) -> bool:
       
        try:
            print(f"{Color.OKCYAN}Cargando página...{Color.ENDC}")
            self.driver.get(url)
            time.sleep(WAIT_TIME)
            print(f"{Color.OKGREEN}✓ Página cargada{Color.ENDC}")
            return True
        except Exception as e:
            print(f"{Color.FAIL}✗ Error cargando página: {e}{Color.ENDC}")
            return False
    
    def ingresar_cedula(self, cedula: str) -> bool:

        try:
            campo_cedula = self.wait.until(
                EC.presence_of_element_located((By.NAME, "cedula"))
            )
            campo_cedula.clear()
            campo_cedula.send_keys(cedula)
            print(f"{Color.OKGREEN}✓ Cédula ingresada{Color.ENDC}")
            return True
        except Exception as e:
            print(f"{Color.FAIL}✗ Error ingresando cédula: {e}{Color.ENDC}")
            return False
    
    def inyectar_solucion_captcha(self, token: str) -> bool:
    
        try:
            # Intentar múltiples métodos para inyectar el token
            scripts = [
                # Método 1: Elemento por ID
                "var elem = document.getElementById('g-recaptcha-response'); if (elem) elem.innerHTML = arguments[0];",
                # Método 2: Textarea por nombre
                "var elem = document.querySelector('textarea[name=\"g-recaptcha-response\"]'); if (elem) elem.value = arguments[0];",
                # Método 3: Cualquier textarea con la clase
                "var elem = document.querySelector('textarea.g-recaptcha-response'); if (elem) elem.value = arguments[0];"
            ]
            
            for script in scripts:
                self.driver.execute_script(script, token)
            
            print(f"{Color.OKGREEN}✓ Solución de captcha inyectada{Color.ENDC}")
            return True
        except Exception as e:
            print(f"{Color.FAIL}✗ Error inyectando captcha: {e}{Color.ENDC}")
            return False
    
    def enviar_formulario(self) -> bool:
    
        try:
            boton_consultar = self.wait.until(
                EC.element_to_be_clickable((By.NAME, "b_consulta"))
            )
            boton_consultar.click()
            
            # Esperar a que procese
            time.sleep(WAIT_TIME + 2)
            print(f"{Color.OKGREEN}✓ Formulario enviado{Color.ENDC}")
            return True
        except Exception as e:
            print(f"{Color.FAIL}✗ Error enviando formulario: {e}{Color.ENDC}")
            return False
    
    def obtener_resultado(self) -> str:

        try:
            # Intentar encontrar el div específico de resultados
            resultado_div = self.wait.until(
                EC.presence_of_element_located((By.ID, "consulta_resp"))
            )
            return resultado_div.text.strip()
        except TimeoutException:
            # Si no encuentra el div, buscar en toda la página
            try:
                return self.driver.find_element(By.TAG_NAME, "body").text
            except:
                return ""
    
    def tomar_screenshot(self, nombre_archivo: str = "screenshot.png"):

        try:
            self.driver.save_screenshot(nombre_archivo)
            print(f"{Color.WARNING}Screenshot guardado: {nombre_archivo}{Color.ENDC}")
        except Exception as e:
            print(f"{Color.FAIL}Error tomando screenshot: {e}{Color.ENDC}")
    
    def cerrar_navegador(self):
    
        if self.driver:
            self.driver.quit()
            print(f"{Color.OKCYAN}Navegador cerrado{Color.ENDC}")