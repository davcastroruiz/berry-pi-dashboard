
# berry-pi-dashboard - Configuración Local

## Requisitos

Para correr este proyecto localmente en macOS:

### 1. Instala Python 3 y pip:
```bash
brew install python3
```

### 2. Crea y activa un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instala las dependencias de Python:
```bash
pip install flask
```

### 4. Ejecuta la aplicación Flask localmente:
```bash
python app.py
```

## Notas

Este proyecto fue originalmente configurado para correr con Nginx y uWSGI en un Raspberry Pi, pero para propósitos de desarrollo local, puedes simplemente usar Flask sin esos componentes adicionales.

## Actualización Automática

Para mantener tu Raspberry Pi actualizado automáticamente con los últimos cambios en el repositorio, puedes configurar un **cron job** que haga un `git pull` y reinicie Nginx dos veces al día.

### Pasos para configurar el cron job:

1. Abre el crontab para editarlo:
   ```bash
   crontab -e
   ```

2. Agrega la siguiente línea para que el cron job se ejecute a las 8:00 AM y 8:00 PM todos los días:
   ```bash
   0 8,20 * * * cd /home/admin/dashboard && git pull origin main && sudo systemctl restart nginx
   ```

3. Guarda y cierra el archivo crontab.

Esto permitirá que el sistema actualice automáticamente los cambios desde el repositorio y reinicie Nginx dos veces al día.
