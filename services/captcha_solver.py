"""
Servicio para resolver reCAPTCHA
"""
import time
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless

from config.settings import ANTICAPTCHA_KEY
from utils.console_utils import Color

class CaptchaSolver:
    """Manejador de resolución de reCAPTCHA"""
    
    def __init__(self):
        self.api_key = ANTICAPTCHA_KEY
        self.disponible = self._verificar_disponibilidad()
    
    def _verificar_disponibilidad(self) -> bool:
        """Verifica que la librería esté disponible"""
        try:
            from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
            return True
        except ImportError:
            print(f"{Color.FAIL}✗ Librería anticaptcha no disponible{Color.ENDC}")
            return False
    
    def verificar_api_key(self) -> bool:
        """Verifica que la API key sea válida y tenga saldo"""
        if not self.disponible:
            return False
            
        try:
            solver = recaptchaV2Proxyless()
            solver.set_verbose(0)
            solver.set_key(self.api_key)
            
            balance = solver.get_balance()
            
            if balance > 0:
                print(f"{Color.OKGREEN}✓ API Key válida - Balance: ${balance:.4f}{Color.ENDC}")
                if balance < 0.01:
                    print(f"{Color.WARNING}⚠ Saldo bajo. Recarga tu cuenta.{Color.ENDC}")
                return True
            else:
                print(f"{Color.FAIL}✗ API Key inválida o sin saldo{Color.ENDC}")
                return False
                
        except Exception as e:
            print(f"{Color.FAIL}✗ Error verificando API Key: {e}{Color.ENDC}")
            return False
    
    def resolver_recaptcha(self, url: str, sitekey: str) -> str:
        """
        Resuelve un reCAPTCHA v2
        
        Args:
            url: URL donde está el reCAPTCHA
            sitekey: Site key del reCAPTCHA
            
        Returns:
            str: Token de respuesta o None si hay error
        """
        if not self.disponible:
            return None
            
        try:
            print(f"{Color.OKCYAN}Resolviendo reCAPTCHA...{Color.ENDC}")
            print(f"{Color.WARNING}Esto puede tardar 20-40 segundos...{Color.ENDC}")
            
            solver = recaptchaV2Proxyless()
            solver.set_verbose(0)
            solver.set_key(self.api_key)
            solver.set_website_url(url)
            solver.set_website_key(sitekey)
            
            inicio = time.time()
            g_response = solver.solve_and_return_solution()
            tiempo = time.time() - inicio
            
            if g_response != 0:
                print(f"{Color.OKGREEN}✓ reCAPTCHA resuelto en {tiempo:.1f}s{Color.ENDC}")
                return g_response
            else:
                print(f"{Color.FAIL}✗ Error resolviendo reCAPTCHA: {solver.error_code}{Color.ENDC}")
                return None
                
        except Exception as e:
            print(f"{Color.FAIL}✗ Error en reCAPTCHA: {e}{Color.ENDC}")
            return None