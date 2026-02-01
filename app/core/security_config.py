import os

# En producción, esto se lee de variables de entorno
# Por ahora, usamos valores por defecto para tu desarrollo en Termux
SECRET_KEY = os.getenv("SECRET_KEY", "70678c3c7e743a3d5f9922e967a5f6a9c1489e53697e68")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

