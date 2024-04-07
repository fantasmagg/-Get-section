# Descripcion
 Este programa lo que hace es obtener las secciones de los navegadores, 
 el programa esta hecho para cuando necesitemos mover las secciones
 de nuestros navegadores

## Pasos de ejecución

### Primero

1. **Reemplazar la ruta**, en la cual desea que lleguen los datos
    - `destination_path = "C:/ffas"`
2. **Ejecutar el archivo** `ser.py`
3. **Levantar el server** ngrok ([https://dashboard.ngrok.com/](https://dashboard.ngrok.com/))
4. Ir al archivo `cl.py`
5. Con los valores que le ha dado el server ngrok, **reemplazar estos valores**:
    - `server_ip = '6.tcp.ngrok.io'`
    - `port = 00000`
6. Una vez se hayan reemplazado los datos necesarios en `cl.py`, ahora se puede ejecutar el programa `cl.py`

    > NOTA: recordar que para todo esto ya debieron tener el `ser.py` ejecutándose, y el server de ngrok activo.

7. Ahora, para generar el `.exe` de `cl.py`:
    - Instalar: `pip install pyinstaller`
    - Ubicarse en la carpeta que se encuentre el `cl.py`
    - Y ahora ejecutar: `pyinstaller --onefile --noconsole app.py`
