# VestaProject API (backend).

## Notas en tener en cuenta:

## Sistema de Identidad Social (Módulo de Usuarios)

 * Perfil Enriquecido: Se extendió el modelo de usuario para incluir bio, profile_pic, website y estadísticas de actividad.

 * Reputación Dinámica: Implementación de un algoritmo para calcular la "reputación" del usuario basada en el total de likes acumulados en todas sus publicaciones.

 * Seguridad de Datos: Integración de esquemas UserPublic para filtrar información sensible (como contraseñas) en los endpoints públicos.

 * Actualización Inteligente: Endpoint PUT /me con lógica de actualización parcial (exclude_unset), permitiendo modificar el perfil sin afectar datos no enviados.

### Motor de Búsqueda y Filtros

 * Búsqueda Avanzada: Creación de un módulo de búsqueda (search.py) con filtros por texto, rangos de precio y categorías.

 * Ranking de Tendencias: Lógica para identificar y mostrar los productos con más interacciones (most likes).

 * Optimización de Consultas: Uso de selectinload de SQLAlchemy para evitar el problema de N+1 consultas al cargar productos y sus relaciones.

### Gestión de Productos y Feedback

 * CRUD Completo: Finalización de las operaciones de creación, lectura, actualización y borrado de productos con validación de autoría.

 * Sistema de Feedback: Implementación de un sistema de comentarios con soporte para edición (PUT) y eliminación, junto con un sistema de "Likes" con lógica de alternancia (toggle).

### Arquitectura y Estabilidad

 * Modularización: Desacoplamiento total de rutas en módulos independientes (auth, products, users, search).

 * Resolución de Dependencias: Solución técnica a importaciones circulares complejas entre modelos de Pydantic/SQLModel mediante reconstrucción de modelos en el punto de entrada (main.py).

 * Corrección de Errores: Depuración de inconsistencias en la base de datos (migraciones manuales de columnas en Neon) y refinamiento del orden de rutas dinámicas.
 
## Seguridad y Blindaje de la API

Este proyecto implementa una arquitectura de seguridad por capas para garantizar la integridad de los datos y la protección de los usuarios:

* **Autenticación Robusta (JWT Hardening):** Implementación de tokens de acceso (JWT) con algoritmos de firma `HS256`. Se ha configurado una expiración estricta de 30 minutos para minimizar riesgos de secuestro de sesión (Session Hijacking).

* **Protección de Credenciales (Passlib/Bcrypt):** Las contraseñas nunca se almacenan en texto plano. Se utiliza `Passlib` con el esquema `Bcrypt` para el hashing de contraseñas, asegurando una defensa sólida contra ataques de fuerza bruta y tablas de arcoíris.

* **Sanitización de Entradas (Anti-XSS):** Uso de la librería `Bleach` integrada en los esquemas de Pydantic. Todas las entradas de texto (descripciones de productos, bios de usuarios, títulos) son filtradas para eliminar etiquetas HTML y scripts maliciosos, previniendo ataques de Cross-Site Scripting (XSS).

* **Control de Acceso Basado en Roles (RBAC):** Sistema de permisos jerárquicos donde solo los usuarios con privilegios de Administrador (`is_admin: true`) pueden gestionar categorías y realizar tareas críticas de mantenimiento.

* **Validación de Integridad de Datos:** Uso de validadores de Pydantic para asegurar que la información (precios, slugs, emails) cumpla con los formatos técnicos requeridos antes de procesar cualquier transacción en la base de datos.


## comandos:

### Autenticación (Auth).

* Registro de Usuario:

```
http POST :8000/auth/register username="shadow" email="shadow@example.com" password="tu_password"
```

* Login (Obtener Token):

```
# Guarda el token en una variable para los siguientes comandos
export TOKEN=$(http --form POST :8000/auth/login username="shadow" password="tu_password" | jq -r .access_token)
```

### Productos (Products)
* Listar Productos (Paginados):

```
http GET :8000/products limit==10 offset==0

Crear Producto (Requiere Token):
http POST :8000/products Authorization:"Bearer $TOKEN" title="Laptop Gaming" description="Potente laptop" price:=1200 category_id:=1
```

### Eliminar Producto:

```
http DELETE :8000/products/1 Authorization:"Bearer $TOKEN"
```

###  Categorías (Categories)
* Listar Categorías:

```
http GET :8000/categories
```

* Crear Categoría (Solo Admin):

```
http POST :8000/categories Authorization:"Bearer $TOKEN" name="Laptops" description="Equipos portátiles" slug="laptops"
```

### Afiliados y Analytics (Affiliates)

* Crear Enlace de Afiliado:

```
http POST :8000/affiliates Authorization:"Bearer $TOKEN" platform_name="Amazon" url="https://amazon.com/item" product_id:=1
```


* Simular un Click (Redirección):

```
http GET :8000/affiliates/go/1

Ver Analíticas del Producto:
http GET :8000/affiliates/analytics/1 Authorization:"Bearer $TOKEN"
```

### Búsqueda y Perfil (Search & Users)

* Búsqueda con Filtros:

```
http GET :8000/search q=="laptop" min_price==500 sort_by=="lowest_price"
```

* Ver mi Perfil:

```
http GET :8000/users/me Authorization:"Bearer $TOKEN"
```

* Actualizar mi Perfil:

```
http PUT :8000/users/me Authorization:"Bearer $TOKEN" bio="Nuevo bio para Vesta" website="https://shadowroot.dev"
```

### Nota
> Para ejecutar estos comandos en Termux, asegúrate de tener instalados httpie y jq (pkg install httpie jq). El uso de :8000 es un atajo de HTTPie para http://localhost:8000.
