# Prueba Tecnica - Backend Trainee

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/ElAguilaPrograma/PruebaTecnica-BackendTrainee.git
```

```bash
cd PruebaTecnica-BackendTrainee
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno virtual:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Configuración

Esta prueba requiere una **API KEY** de ExchangeRate API.

## 1. Obtener API KEY

Ir al sitio:

https://www.exchangerate-api.com/

Crear una cuenta y generar una API KEY.

---

## 2. Configurar archivo .env

Renombrar el archivo:

```
.env_example
```

a:

```
.env
```

Editar el archivo y poner su API KEY:

```env
API_KEY=tu_api_key_aqui
```

---

# Ejecución

Ejecutar el servidor con:

```bash
fastapi dev app/main.py
```

Esperar a que el servidor inicie.

Por defecto se ejecutará en:

```
http://127.0.0.1:8000
```

---

# Uso

Abrir en el navegador:

```
http://127.0.0.1:8000/docs
```

Esto abrirá la documentación automática de Swagger.

---

# Endpoint principal

## Reconciliation

```
/reconciliation/{batch}
```

### Pasos:

1. Dar click en el endpoint y luego en **Try it out**

2. Ingresar un batch

Ejemplo recomendado:

```
TC-202403
```

3. Presionar **Execute**

4. Descargar el archivo generado dando click en:

```
Download file
```

---

# Ejemplo de batches

Recomiendo usar TC-202403 para probar el Endpoint, ya que contiene ejemplos con todos los estatus pero los otros batch tambien funcionan sin problemas.

