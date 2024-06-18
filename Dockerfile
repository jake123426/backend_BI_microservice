# FROM python:3.11.9-slim
# FROM python:3-alpine
# FROM python:3-alpine
FROM python:3

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar las dependencias
COPY requirements.txt .
# COPY . .

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# ENV PORT=${PORT}
# ENV FLASK_APP=src.app.py

# Establecer el comando para ejecutar el contenedor
CMD ["python", "./src/app.py"]

# Comando para correr la aplicación usando Gunicorn

# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.app:create_app"]
# CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "src.app:app", "--timeout", "120"]
# CMD ["gunicorn", "-w", "2", "--host", "0.0.0.0:5000", "src.app:create_app()"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
