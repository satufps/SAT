# Instalaciones

SAT (Sistema alertas tempranas)\
Frontend -> Angular 2+\
Backend -> Python + Flask\
Base de datos -> MongoDB

## Paso 1

Instalar Docker

## Paso 2

Clonar repositorio\
**git clone https://github.com/ingalexander94/SAT.git**

## Paso 3

Construir proyecto con Docker\
**docker-compose build**

## Paso 4

Ejecutar proyecto\
**docker-compose up**

**La aplicación corre en el puerto 4200**

# Instrucciones para realizar pruebas

## Rutas para iniciar sesión

- Enlace iniciar sesión estudiantes -> http://localhost:4200/estudiante/iniciar-sesion
- Enlace iniciar sesión (docentes y jefes de plan) -> http://localhost:4200/docente/iniciar-sesion
- Enlace iniciar sesión administrativos (Vicerrector y Psicologo) -> http://localhost:4200/administrativo/iniciar-sesion

## Datos para iniciar sesión

Estudiante -> Datos cargados por defecto en el formulario\
Jefe de plan -> Datos cargados por defecto en el formulario\
Psicologo -> Datos cargados por defecto en el formulario\
Docente -> codigo: 1049485, documento: 525933018, clave:9226\
Vicerrector -> documento: 1740427369, clave:5535
