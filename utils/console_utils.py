class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def imprimir_banner():
    print(f"\n{Color.HEADER}{'='*70}")
    print("    CONSULTA DE JURADO DE VOTACIÓN")
    print("    Registraduría Nacional del Estado Civil")
    print("    Elecciones Atípicas - Villeta, Cundinamarca")
    print(f"{'='*70}{Color.ENDC}\n")

def solicitar_entrada(mensaje: str, obligatorio: bool = True) -> str:
    
    while True:
        try:
            entrada = input(f"{Color.BOLD}{mensaje}{Color.ENDC}").strip()
            
            if obligatorio and not entrada:
                print(f"{Color.FAIL}Este campo es obligatorio.{Color.ENDC}")
                continue
                
            return entrada
            
        except KeyboardInterrupt:
            print(f"\n{Color.WARNING}Operación cancelada por el usuario.{Color.ENDC}")
            return ""
        except EOFError:
            print(f"\n{Color.FAIL}Error de entrada.{Color.ENDC}")
            return ""

def confirmar_accion(mensaje: str) -> bool:
    
    respuesta = solicitar_entrada(f"{mensaje} (S/N): ").upper()
    return respuesta in ['S', 'SI', 'Y', 'YES']