# Usa una imagen base de Python 3.9 (puedes elegir otra versión si lo deseas)
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos requeridos (requirements.txt y la aplicación) al contenedor
COPY requirements.txt requirements.txt
COPY .env .env
COPY . .

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Establecer las variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Exponer el puerto 5000 para que pueda ser accedido desde fuera del contenedor
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["flask", "run"]
