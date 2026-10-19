# ClothesLook

Red social sencilla para catalogar prendas, combinarlas en *looks* por temporada y comentarlas.
Es una **práctica universitaria en equipo** hecha con Django en enero de 2019.

> Proyecto académico, no mantenido y sin ningún despliegue conocido. Se conserva como muestra de trabajo en equipo con Django. Antes de reutilizarlo, lee [Seguridad y limitaciones](#seguridad-y-limitaciones).

[English summary below](#english-summary).

## Funcionalidades

- **Cuentas:**
  - Registro e inicio de sesión con un modelo de usuario propio: el identificador es `nickName` (`AbstractBaseUser` + `PermissionsMixin`, con `UserManager` propio).
  - Perfil editable y borrado de la propia cuenta.
- **Prendas:**
  - Alta con nombre, URL de la foto, talla, marca, enlace y categoría.
  - Listado general paginado, listado «mis prendas» y filtro por categoría.
  - Edición y borrado, solo por su propietario.
- **Looks:**
  - Combinan varias prendas con título, descripción y temporada (primavera, verano, otoño o invierno).
  - Listado general paginado, «mis looks», filtro por temporada y vista de detalle con comentarios.
- **Comentarios:** los usuarios registrados pueden comentar en los looks.
- **Administración:** se usa el *admin* de Django para categorías, prendas, looks, comentarios y usuarios. Las categorías se crean desde ahí.

## Stack

Python 3.7, Django 2.1 (vistas basadas en funciones, `ModelForm`, `Paginator`, autenticación de Django con modelo de usuario personalizado), SQLite, plantillas de Django y Bootstrap 4.2 (CDN).

```
ClothesLook/        configuración del proyecto (settings, urls, wsgi)
clothesLookApp/     la aplicación: models, views, forms, managers (UserManager), admin,
                    migrations y tests
templates/          plantillas (banner.html es el layout con el menú)
```

## Puesta en marcha

Django 2.1 solo admite oficialmente **Python 3.5 a 3.7**. Con versiones más recientes no hay garantía de que funcione.

```bash
python3.7 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export DJANGO_DEBUG=1                # solo desarrollo; ver .env.example
python manage.py migrate             # crea db.sqlite3 (no se versiona)
python manage.py createsuperuser     # pide nickName y contraseña
python manage.py runserver           # http://127.0.0.1:8000/
```

La configuración se lee de variables de entorno (ver [`.env.example`](.env.example)):

| Variable | Uso |
|---|---|
| `DJANGO_DEBUG` | `1` solo en desarrollo. Por defecto está desactivado |
| `DJANGO_SECRET_KEY` | Obligatoria si `DJANGO_DEBUG` no vale `1`. En desarrollo se usa una clave fija pública |
| `DJANGO_ALLOWED_HOSTS` | Hosts separados por comas. Es necesaria con `DJANGO_DEBUG=0` |

Antes de dar de alta prendas, crea alguna categoría en `/admin/`.

## Pruebas

```bash
DJANGO_DEBUG=1 python manage.py test
```

`clothesLookApp/tests.py` comprueba la autorización:
- Los visitantes anónimos van a `/login/`.
- Un usuario recibe un 403 si intenta editar o borrar la cuenta o las prendas de otro, y los datos no cambian.
- El propietario sí puede editar y borrar lo suyo.
- Los identificadores inexistentes devuelven 404.

## CI

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) usa GitHub Actions con permisos mínimos (`contents: read`) y acciones fijadas por SHA. En cada push a `master` y en cada pull request, dentro de un contenedor `python:3.7-slim`:

1. Instala `requirements.txt`.
2. Genera una `SECRET_KEY` efímera.
3. Ejecuta `manage.py check`, `makemigrations --check` y `manage.py test`.

## Seguridad y limitaciones

**Corregido en la rama `chore/portfolio-hardening`:**
- Cualquier visitante podía editar o borrar cualquier usuario o prenda conociendo su id. Ahora hace falta iniciar sesión y ser el propietario.
- Las vistas que necesitan un usuario redirigen al login en lugar de fallar.
- `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` salen de variables de entorno.
- `db.sqlite3`, los `.pyc` y los ficheros del IDE ya no se versionan.
- Se añade la migración que faltaba (`0002`).

**Pendiente o conocido:**
- **El historial de git conserva la `SECRET_KEY` antigua y una base SQLite con cuentas de prueba.** Esa clave ya no se usa y no debe reutilizarse: cualquier despliegue necesita una clave nueva. Purgar el historial es opcional y tendrían que acordarlo los coautores.
- **Django 2.1 está fuera de soporte desde diciembre de 2019** y tiene vulnerabilidades conocidas posteriores. Antes de cualquier despliegue habría que migrar a una versión LTS con soporte (por ejemplo, Django 5.2) y aplicar la configuración de `manage.py check --deploy` (HTTPS, cookies seguras, cabeceras).
- Los looks y los comentarios no se pueden editar ni borrar. Comentar en un look inexistente da error 500.
- Hay rutas `re_path` sin anclar y redirecciones relativas (`'../../../clothing/list'`).
- La foto de una prenda es una URL en texto libre: no hay subida de imágenes.
- El cierre de sesión se hace por GET (`LogoutView` de Django 2.1).

## Equipo y autoría

Es un trabajo en equipo. Según el historial de git y los mensajes de commit:

- **José Joaquín Rodríguez Pérez** ([@joaquinperez94](https://github.com/joaquinperez94)): creación del proyecto y del modelo, usuario personalizado, registro, login y perfil, edición y borrado de usuarios, vista de looks, paginación y limpieza final. También las mejoras de 2026 de esta rama (configuración, autorización, pruebas y CI).
- **María Jiménez Vega** (`marjimveg1`): módulo de prendas (listado, filtro por categoría, edición y borrado), comentarios y página de inicio.
- **Julia** (`julia`, `julgargal`): módulo de looks (creación, listado y detalle), comentarios y menú y layout con Bootstrap.
- Cuenta compartida del grupo (`grupo10dp2019`).

**Licencia:** el repositorio no tiene licencia. El código es de autoría compartida y no se añadirá una licencia sin el consentimiento de todos los coautores.

---

## English summary

**ClothesLook** is a university team project (January 2019) built with Django 2.1. It is a small social network to catalogue clothing items, combine them into seasonal *looks* and comment on them. It uses a custom user model (`nickName` as the username), function-based views, `ModelForm`, pagination and Bootstrap 4.

- **Run it:** Python 3.7, `pip install -r requirements.txt`, `DJANGO_DEBUG=1 python manage.py migrate`, then `runserver`. See `.env.example` for `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` and `DJANGO_ALLOWED_HOSTS`.
- **Tests:** `python manage.py test` covers the authorisation rules (owner-only edit/delete, login redirects, 404s). CI runs `check`, `makemigrations --check` and the tests on GitHub Actions.
- **Security:** the 2026 hardening branch fixed missing authorisation checks and moved secrets to environment variables. The old key and a test SQLite database remain in the git history. Django 2.1 is end-of-life.
- **Team:** José Joaquín Rodríguez Pérez (@joaquinperez94), María Jiménez Vega (`marjimveg1`), Julia (`julia`/`julgargal`) and the shared group account. No licence has been added because the code has several co-authors.
