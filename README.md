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
 


## comandos:

```bash
http --form POST http://127.0.0.1:8000/auth/token \
    username=ShadowRoot07 \
    password=tupassword123
```

```bash
export TOKEN="pega_aquí_tu_access_token"
```

* **PUT:**

```bash
http PUT http://127.0.0.1:8000/products/1 \
    title="Producto Actualizado" \
    description="Nueva descripción con mejoras" \
    price:=99.99 \
    image_url="http://link.com/foto.jpg" \
    affiliate_link="http://amazon.com/ref" \
    category="Ofertas" \
    "Authorization: Bearer $TOKEN"
```

* **DELETE:**

```bash
http DELETE http://127.0.0.1:8000/products/1 \
    "Authorization: Bearer $TOKEN"
```

```bash
# Buscar solo productos de tecnología
http GET "http://127.0.0.1:8000/products?category=Tecnología"

# Buscar productos que tengan la palabra 'Gamer'
http GET "http://127.0.0.1:8000/products?search=Gamer"

# Pedir solo los primeros 5 productos
http GET "http://127.0.0.1:8000/products?limit=5"
```


```bash
http PUT http://127.0.0.1:8000/products/comments/1 \
    content="Este es mi comentario editado y corregido." \
    "Authorization: Bearer $TOKEN"
```

* comando para ver los mejores productos (con mas likes):

```bash
# Obtener el top 10 de productos más populares
http GET http://127.0.0.1:8000/products/trending
```

* comando para crear comentarios:

```bash
http POST http://127.0.0.1:8000/products/1/comments \
    content="¡Este producto me encantó! Muy recomendado." \
    "Authorization: Bearer $TOKEN"
```

```bash
# Buscar Laptops entre 500 y 1500 dólares, ordenadas por la más barata
http GET "http://127.0.0.1:8000/search?q=Laptop&min_price=500&max_price=1500&sort_by=lowest_price"

# Solo ver productos que cuesten menos de 100 dólares
http GET "http://127.0.0.1:8000/search?max_price=100"
```

* comando para actualizar perfil creado.

```bash
http PUT http://127.0.0.1:8000/users/me \
    bio="ShadowRoot07 | Backend Developer & Neovim Enthusiast" \
    website="https://github.com/ShadowRoot07" \
    "Authorization: Bearer $TOKEN"
```

* Comando GET para ver perfil:

```bash
http GET http://127.0.0.1:8000/users/ShadowRoot07
```

```bash
http POST http://127.0.0.1:8000/affiliates/ \
    platform_name="Amazon" \
    url="https://www.amazon.com/ejemplo-producto-afiliado" \
    product_id=1 \
    "Authorization: Bearer $TOKEN"
```

```bash
http GET http://127.0.0.1:8000/affiliates/go/1
```

```bash
http GET http://127.0.0.1:8000/affiliates/go/1 "Authorization: Bearer $TOKEN"
```

```bash
http GET http://127.0.0.1:8000/affiliates/product/1
```

```bash
http GET http://127.0.0.1:8000/affiliates/analytics/1 "Authorization: Bearer $TOKEN"
```

```bash
http POST http://127.0.0.1:8000/auth/register \
    username="GhostShell_07" \
    email="ghost@vesta.project" \
    password="password123"
```

```bash
http GET :8000/users/profile "Authorization: Bearer $TOKEN"
```


```bash
http POST http://127.0.0.1:8000/products/ \
    title="Teclado Ghost" \
    description="Teclado especial para GhostShell_07" \
    price=50.0 \
    category="Tech" \
    image_url="https://via.placeholder.com/150" \
    affiliate_link="https://amazon.com/placeholder" \
    "Authorization: Bearer $TOKEN"
```

```bash
http PATCH :8000/affiliates/1 \
    platform_name="Amazon Pro" \
    url="https://amazon.com/nueva-url" \
    "Authorization: Bearer $TOKEN"
```

```bash
http DELETE :8000/affiliates/1 "Authorization: Bearer $TOKEN"
```

```bash
http POST http://127.0.0.1:8000/categories/ \
    name="Tecnología" \
    slug="tech" \
    description="Gadgets y periféricos para entusiastas"
```

```bash
http GET http://127.0.0.1:8000/categories/
```

```bash
http POST http://127.0.0.1:8000/products \
    name="Mouse Logitech G502" \
    description="El mouse más vendido" \
    price=49.99 \
    category_id=1 \
    "Authorization: Bearer $TOKEN"
```

* **Comando especial para limpiar la base de datos:** solo usarlo en casos especoales o de emergencia.

```bash
python reset_db.python
```

Esto ehecuta el Script especial encargado de eso, **USAR CON CUIDADO!!**.
