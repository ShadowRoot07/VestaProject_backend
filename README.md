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

## DOCUMENTATION IN ENGLISH.

Welcome to the crown jewel of **ShadowRoot07**. **VestaProject** is a scalable, secure, and highly modular REST API built with **fastapi** and **sqlmodel**, designed to handle a community of affiliated products, social reputation and armor against common attacks. 

--- 

## Main Features ### Social Identity System 

* **rich profile:** Includes biography, profile photos, external links, and activity statistics. 

* **Dynamic Reputation:** Built-in algorithm that calculates the user's prestige based on the global *likes* accumulated in their publications. 

* **Data security:** Strict filtering using `userpublic` schemes to prevent leaks of sensitive information (such as password hashes). 

* **Smart Update:** Endpoint `put /me` with partial update logic (`exclude_unset`), allowing the profile to be modified in granular form. ### Search engine and filters.

* **Advanced search:** Dedicated module (`Search.py`) with filters by text, price ranges and categories. 

* **Trend Ranking:** Logic to identify and display products with more interactions (*Most Likes*). 

* **Sql optimization:** Using `SelectinLoad` from SQLALCHEMY to avoid the problem of n+1 queries when loading complex relationships. 

### Management of Feedback and Affiliates 

* **Complete CRUD:** Robust operations of creation, reading and deletion with strict validation of authorship. 
* **Feedback system:** Comments and "likes" system with toggle logic (*toggle*). 

* **Affiliate module:** Click tracking and analytics by platform (Amazon, eBay, etc.) for product owners. 

---

## Security and Shielding (layered defense) 

| layer | technology | Purpose | 
| :--- | :--- | :--- | 
| **Authentication** | jwt (hs256) | Secure sessions with strict expiration of 30 min. | 
| **HASHING** | Passlib / bcrypt | Protection against brute force and rainbow boards. | 
| **Sanitization** | bleach | Active prevention of cross-site scripting (XSS) attacks. | 
| **Authorization** | RBAC | Role-based access control (Admin vs User). | 
| **Validation** | pydantic v2 | Total integrity of data types and formats. | 

--- 

## Installation and configuration **Prerequisites:** 

* Python 3.12+ 
* Termux (if running on mobile) or any Linux environment. 
* PostgreSQL (recommended: Neon.Tech). 

**Steps:** 
1. **Clone the repository.** 
2. **Install dependencies:** 
```Bash
pip install -r requirements.txt 
``` 
3. **Configure environment variables:** Create a .env file with Secret_Key, Algorithm and Database_url. 
4. **Apply Migrations:** 
```Bash 
Alembic Upgrade Head 
``` 
5. **Start Server:** 
```Bash
uvicorn main:app --reload 
``` 

## Guide Usage (httpie commands) **authentication** 
* log: 
```bash
http post :8000/auth/register username="shadow" email="shadow@example.com" password="tu_password" ``` * login: ```bash export token=$(http --form post :8000/auth/login username="shadow" password="tu_password" | jq -r .access_token) 
```

**Products and categories** 

* List products: 
```Bash
http get :8000/products limit==10 Offset=0 
``` 
* Create product: 
```Bash 
HTTP post :8000/products Authorization:"Bearer $token" title="laptop" description="powerful" price:=1200 Category_id:=1 
``` 
* Create Category (Admin only): 
```Bash
HTTP POST :8000/Categories Authorization:"Bearer $token" name="laptops" slug="laptops" 
``` 

**Analytics and Search** 
* View Analytics: 

```Bash
HTTP get :8000/affiliates/analytics/1 Authorization:"Bearer $token" 
``` 

* Filtered search: 
```bash
http get :8000/search q=="laptop" min_price==500 sort_by=="lowest_price" 
``` 

## Architecture of the project. 

```Text 
. ├── app/ 
│ ├── core/ # security, auth and config utilities 
│ ├── models/ # SQLModel models (Tables of db) 
│ ├── routers/ # endpoints divided by logical modules 
│ ├── schemas/ # pydantic schemes (validation and Sanitization) 
│ └── Database.py# DB Session Configuration and Engine ├── Migrations/ # Database Version Control (Alembic) 
├── main.py # FastAPI application entry point 
└──requirements.txt 
``` 

**Note for Termux users:** Install test tools with PKG Install Httpy jq.


### Desarrollado con ❤️ por ShadowRoot07 - 2026.
### >> Developed with ❤️ by ShadowRoot07 - 2026.
