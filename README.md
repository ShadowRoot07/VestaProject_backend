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

1. Authentication & Profile (The Basics)

Primero creamos identidad para obtener el acceso.
 
    * Register a user:

```bash
http POST :8000/auth/register username="GhostShell_07" email="ghost@vesta.project" password="password123"
```

    * Login (Get Token):

```bash
http --form POST :8000/auth/token username="GhostShell_07" password="password123"
```

    * Set Token Variable:

```bash
export TOKEN="tu_token_aqui"
```

    * Update My Profile:

```bash
http PUT :8000/users/me bio="Backend Developer & Neovim Enthusiast" website="https://github.com/ShadowRoot07" "Authorization: Bearer $TOKEN"
```

    * View Public Profile:
```bash
http GET :8000/users/GhostShell_07
```

2. Catalog Setup (Categories)


Sin categorías no hay productos en tu nueva estructura relacional.

    * Create a Category:
```bash
http POST :8000/categories name="Technology" slug="tech" description="Gadgets and peripherals"
```

    * List All Categories:

```bash
http GET :8000/categories
```

3. Inventory Management (Products)

Ahora que tenemos category_id=1, podemos crear productos.

    * Create a Product:
    (Nota: Ya no enviamos "category" como texto, enviamos category_id)

```bash
http POST :8000/products title="Logitech G502" description="Best selling gaming mouse" price:=49.99 category_id=1 "Authorization: Bearer $TOKEN"
```

    * Update a Product:

```bash
http PUT :8000/products/1 title="Updated Product" price:=59.99 category_id=1 "Authorization: Bearer $TOKEN"
````

    * Delete a Product:

```bash
http DELETE :8000/products/1 "Authorization: Bearer $TOKEN"
```

4. Search & Discovery

Consultas para los compradores.

    * List Products (with pagination):

```bash
http GET :8000/products?limit=5&offset=0
```


    * Advanced Search (Filters):

```bash
http GET ":8000/search?q=Logitech&min_price=10&max_price=100&sort_by=lowest_price"
```
    
    * Get Trending (Most Liked):
    (Nota: Este endpoint debe estar implementado en tu router de productos)
```bash
http GET :8000/products/trending
```

5. Affiliate System (The Core Business)

Aquí es donde rastreamos el dinero.
    
    * Create Affiliate Link:

```bash
http POST :8000/affiliates platform_name="Amazon" url="https://amazon.com/mouse-ref" product_id=1 "Authorization: Bearer $TOKEN"
```

    * Redirect & Track Click (Public):

```bash
http GET :8000/affiliates/go/1
```

    * Get Links for a Specific Product:
```bahs
http GET :8000/affiliates/product/1
```

    * Analyze Link Clicks (Owner Only):
```bash
http GET :8000/affiliates/analytics/1 "Authorization: Bearer $TOKEN"
```

    * Deactivate Link (Soft Delete):
```bash
http DELETE :8000/affiliates/1 "Authorization: Bearer $TOKEN"
```

6. Social (Comments & Interactions)

    * Post a Comment:

```bash
http POST :8000/products/1/comments content="Highly recommended!" "Authorization: Bearer $TOKEN"
```

    * Edit a Comment:

```bash
http PUT :8000/products/comments/1 content="Corrected comment content." "Authorization: Bearer $TOKEN"
```

🛠️ Mantenimiento de Emergencia

    * Reset Database (The Red Button):
```bash
python reset_db.py
```

### Notas de ShadowRoot07:
    * URL Corta: En local puedes usar :8000 en lugar de http://127.0.0.1:8000, HTTPie lo entiende perfectamente.

    * Price format: Usa price:=49.99 (con los dos puntos) para asegurar que HTTPie lo envíe como un número (float) y no como un string.
    * Consistency: Ahora que todo está en inglés, tu Swagger (/docs) se verá mil veces más profesional.


