# VestaProject API (backend).

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
