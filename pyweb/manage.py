#!/usr/bin/env python
import os
import sys
import logging
import argparse

# Configuración del logger para registrar acciones y errores
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Función principal para ejecutar las operaciones de administración de Django."""
    
    # Configura el entorno de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

    try:
        # Importa Django y configura la aplicación
        import django
        django.setup()
    except Exception as e:
        logger.error(f'Error al configurar Django: {e}')
        sys.exit(1)

    # Análisis de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Django Management Script')
    parser.add_argument('command', nargs='?', default='runserver', 
                        help='El comando a ejecutar (runserver, migrate, createsuperuser, etc.)')
    parser.add_argument('--settings', help='Especifica un módulo de configuración diferente')
    parser.add_argument('--verbosity', type=int, choices=[0, 1, 2], default=1,
                        help='Nivel de verbosidad de la salida')

    args = parser.parse_args()

    # Establecer configuraciones adicionales si se proporcionan
    if args.settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = args.settings

    # Log de información sobre el comando a ejecutar
    logger.info(f'Ejecutando comando: {args.command} con verbosidad: {args.verbosity}')

    # Manejo de comandos específicos
    if args.command == 'runserver':
        runserver(args.verbosity)
    elif args.command == 'migrate':
        migrate(args.verbosity)
    elif args.command == 'createsuperuser':
        create_superuser()
    elif args.command == 'startapp':
        start_app(args.verbosity)
    elif args.command == 'makemigrations':
        make_migrations(args.verbosity)
    elif args.command == 'shell':
        open_shell()
    else:
        logger.error(f'Comando no reconocido: {args.command}')
        sys.exit(1)

def runserver(verbosity):
    """Inicia el servidor de desarrollo de Django."""
    logger.info('Iniciando el servidor de desarrollo...')
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'runserver'])

def migrate(verbosity):
    """Aplica las migraciones a la base de datos."""
    logger.info('Aplicando migraciones...')
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'migrate'])

def create_superuser():
    """Crea un superusuario para el panel de administración."""
    logger.info('Creando superusuario...')
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'createsuperuser'])

def start_app(verbosity):
    """Crea una nueva aplicación dentro del proyecto Django."""
    app_name = input('Ingrese el nombre de la nueva aplicación: ')
    logger.info(f'Creando nueva aplicación: {app_name}')
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'startapp', app_name])

def make_migrations(verbosity):
    """Crea nuevas migraciones basadas en los cambios en los modelos."""
    logger.info('Creando migraciones...')
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'makemigrations'])

def open_shell():
    """Abre una shell interactiva de Django."""
    logger.info('Abriendo shell interactiva de Django...')
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'shell'])

if __name__ == '__main__':
    main()
