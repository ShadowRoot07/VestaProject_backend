# VestaProject API - Backend Professional

Bienvenido a la joya de la corona de **ShadowRoot07**. **VestaProject** es una API REST escalable, segura y altamente modular construida con **FastAPI** y **SQLModel**, diseñada para manejar una comunidad de productos con sistema de afiliados, reputación social y blindaje contra ataques comunes.

---

## Características Principales

### Sistema de Identidad Social
* **Perfil Enriquecido:** Incluye biografía, fotos de perfil, enlaces externos y estadísticas de actividad.

* **Reputación Dinámica:** Algoritmo integrado que calcula el prestigio del usuario basado en los *likes* globales acumulados en sus publicaciones.

* **Seguridad de Datos:** Filtrado estricto mediante esquemas `UserPublic` para evitar fugas de información sensible (como hashes de contraseñas).

* **Actualización Inteligente:** Endpoint `PUT /me` con lógica de actualización parcial (`exclude_unset`), permitiendo modificar el perfil de forma granular.

### Motor de Búsqueda y Filtros
* **Búsqueda Avanzada:** Módulo dedicado (`search.py`) con filtros por texto, rangos de precio y categorías.

* **Ranking de Tendencias:** Lógica para identificar y mostrar los productos con más interacciones (*most likes*).

* **Optimización SQL:** Uso de `selectinload` de SQLAlchemy para evitar el problema de N+1 consultas al cargar relaciones complejas.

### Gestión de Feedback y Afiliados
* **CRUD Completo:** Operaciones robustas de creación, lectura y borrado con validación estricta de autoría.

* **Sistema de Feedback:** Comentarios y sistema de "Likes" con lógica de alternancia (*toggle*).

* **Módulo de Afiliados:** Seguimiento de clics y analíticas por plataforma (Amazon, eBay, etc.) para dueños de productos.

---

## Seguridad y Blindaje (Layered Defense)

| Capa | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Autenticación** | JWT (HS256) | Sesiones seguras con expiración estricta de 30 min. |
| **Hashing** | Passlib / Bcrypt | Protección contra fuerza bruta y tablas arcoíris. |
| **Sanitización** | Bleach | Prevención activa de ataques Cross-Site Scripting (XSS). |
| **Autorización** | RBAC | Control de acceso basado en roles (Admin vs User). |
| **Validación** | Pydantic V2 | Integridad total de tipos y formatos de datos. |

---

## Instalación y Configuración

**Requisitos Previos:**
* Python 3.12+

* Termux (si se ejecuta en móvil) o cualquier entorno Linux.

* PostgreSQL (Recomendado: Neon.tech).

**Pasos:**
1. **Clonar el repositorio.**

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:** Crea un archivo .env con SECRET_KEY, ALGORITHM y DATABASE_URL.

4. **Aplicar migraciones:**

    ```bash
    alembic upgrade head
    ```

5. **Iniciar Servidor:**

    ```bash
    uvicorn main:app --reload
    ```

## Guía de Uso (Comandos HTTPie)

**Autenticación**

* Registro:

    ```bash
    http POST :8000/auth/register username="shadow" email="shadow@example.com" password="tu_password"
    ```

* Login (Obtener Token):

    ```bash
    export TOKEN=$(http --form POST :8000/auth/login username="shadow" password="tu_password" | jq -r .access_token)
    ```

**Productos y Categorías**

* Listar Productos:

    ```bash
    http GET :8000/products limit==10 offset==0
    ```

* Crear Producto:

    ```bash
    http POST :8000/products Authorization:"Bearer $TOKEN" title="Laptop" description="Potente" price:=1200 category_id:=1
    ```

* Crear Categoría (Solo Admin):

    ```bash
    http POST :8000/categories Authorization:"Bearer $TOKEN" name="Laptops" slug="laptops"
    ```

**Analíticas y Búsqueda**

* Ver Analytics:

    ```bash
    http GET :8000/affiliates/analytics/1 Authorization:"Bearer $TOKEN"
    ```

* Búsqueda Filtrada:

    ```bash
    http GET :8000/search q=="laptop" min_price==500 sort_by=="lowest_price"
    ```

## Arquitectura del Proyecto.

```text 
.
├── app/
│   ├── core/      # Seguridad, utilidades de auth y config
│   ├── models/    # Modelos SQLModel (Tablas de DB)
│   ├── routers/   # Endpoints divididos por módulos lógicos
│   ├── schemas/   # Esquemas Pydantic (Validación y Sanitización)
│   └── database.py# Configuración de la sesión y motor de DB
├── migrations/    # Control de versiones de base de datos (Alembic)
├── main.py        # Punto de entrada de la aplicación FastAPI
└── requirements.txt
```

**Nota para usuarios de Termux:** Instala las herramientas de prueba con pkg install httpie jq.

### Desarrollado con ❤️ por ShadowRoot07 - 2026.
