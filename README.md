# 🔍 Consulta de Jurados de Votación

Script automatizado para consultar si una cédula está registrada como jurado de votación en la Registraduría Nacional del Estado Civil de Colombia.

## ✨ Características
- Consulta automatizada en el portal oficial de la Registraduría
- Resolución automática de reCAPTCHA usando Anti-Captcha
- Navegación web automatizada con Selenium
- Interfaz de consola con colores y mensajes claros
- Manejo robusto de errores y tiempo de espera
- Múltiples intentos en caso de fallos

## 📋 Prerrequisitos
- Python 3.7 o superior
- Google Chrome instalado
- Conexión a internet
- API Key de [Anti-Captcha](https://anti-captcha.com/)

## 🚀 Instalación Rápida
```bash
# Clonar o descargar el proyecto
git clone <url-del-repositorio>
cd consulta-jurados

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate
# Activar entorno virtual (Mac/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
