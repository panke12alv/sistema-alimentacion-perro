# Documentación de Tests - Dog Feeder

## Descripción
Los tests del proyecto Dog Feeder verifican que los modelos y la lógica de la aplicación funcionen correctamente. Se usan **tests unitarios** con `pytest`. Cada test corre sobre la base de datos de prueba (`mysql_test_db`) y no requiere datos previos, ya que se crean y validan dentro del test.

---

## Tests disponibles

### 1. `tests/test_usuario.py`
- **Propósito:** Validar la creación y búsqueda de usuarios.
- **Funciones testeadas:**  
  - `Usuario.crear(nombre)` → crea un usuario con rol `DUENO`.  
  - `Usuario.buscar_por_id(id)` → busca un usuario por su ID.
- **Flujo del test:**  
  1. Crear un usuario de prueba.  
  2. Verificar que se asigna un ID.  
  3. Buscar al usuario por ID.  
  4. Verificar que los datos coinciden.

---

### 2. `tests/test_perro.py`
- **Propósito:** Validar la creación y consulta de perros.
- **Funciones testeadas:**  
  - `Perro.crear(nombre, raza, edad, peso, propietario_nombre)` → crea un perro.  
  - `Perro.buscar_por_id(id)` → busca un perro por ID.
- **Flujo del test:**  
  1. Crear un perro de prueba.  
  2. Verificar que se asigna un ID.  
  3. Buscar el perro por ID.  
  4. Validar que los atributos coinciden con los ingresados.

---

### 3. `tests/test_rutina.py`
- **Propósito:** Validar la creación y actualización de rutinas de alimentación.
- **Funciones testeadas:**  
  - `RutinaAlimentacion.crear_o_actualizar(perro_id, alimentos_ids, horarios, cantidad_total)`  
- **Flujo del test:**  
  1. Crear un perro de prueba.  
  2. Crear una rutina para el perro.  
  3. Verificar que la rutina se guardó correctamente y los datos coinciden.

---

### 4. `tests/test_alimento.py`
- **Propósito:** Validar el registro de alimentos.
- **Funciones testeadas:**  
  - `Alimento.crear(tipo, marca, calorias_por_100g)`  
- **Flujo del test:**  
  1. Crear un alimento de prueba.  
  2. Verificar que se asigna un ID.  
  3. Consultar todos los alimentos y validar que el nuevo está incluido.

---

### 5. `tests/test_historial.py`
- **Propósito:** Validar el registro y consulta de comidas realizadas.
- **Funciones testeadas:**  
  - `Comida.crear(perro_id, alimento_id, cantidad)`  
- **Flujo del test:**  
  1. Crear perro y alimento de prueba.  
  2. Registrar una comida para el perro.  
  3. Consultar las comidas y verificar que los datos coinciden.

---

## Cómo correr los tests

1. Asegurarse de tener la base de datos de prueba vacía o recreada (`schema.sql`).  
2. Activar el entorno virtual si existe.  
3. Ejecutar:

```bash
pytest

