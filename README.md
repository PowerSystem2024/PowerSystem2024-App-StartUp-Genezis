
# Sistema Integral de Turnos Médicos | Grupo GENEZIS - COHORTE 2024



![Logo Genezis](./logo-genezis-new.png)



**Genezis** es una aplicación de escritorio desarrollada en **Python** con una interfaz gráfica intuitiva basada en **Tkinter**, que permite a diferentes actores del sistema de salud gestionar turnos médicos de forma eficiente. Está diseñada utilizando el patrón de arquitectura **MVC** (Modelo - Vista - Controlador), conectada a una base de datos **PostgreSQL** alojada en **Supabase**.

Este sistema fue desarrollado como proyecto académico por un equipo de estudiantes universitarios y está dividido en módulos independientes por tipo de usuario: administradores, médicos, pacientes e instituciones.

---

## 🎯 Objetivo del proyecto

El propósito principal de Genezis es ofrecer un entorno centralizado donde:

* Las instituciones puedan organizar a sus médicos y turnos disponibles.
* Los médicos gestionen su agenda, disponibilidad y pacientes.
* Los pacientes puedan solicitar, cancelar y consultar sus turnos.
* El administrador general del sistema tenga control y estadísticas sobre todo lo que ocurre.

Está pensado para ser escalable y adaptable a instituciones reales.

---

## 📌 Funcionalidades generales

* Registro y login de usuarios con rol asignado.
* Diferenciación de vistas y permisos por rol (admin, médico, paciente, institución).
* Gestión de horarios y agenda médica.
* Turnos con fechas y horarios específicos (no solo días de semana).
* Historial clínico por paciente.
* Alta, baja y edición de usuarios, médicos, instituciones y especialidades.
* Control visual desde paneles tipo dashboard.
* Validación de datos en tiempo real.
* Filtrado de turnos por fecha y estado.
* Prevención de superposición de horarios.

---

## 🛠️ Tecnologías utilizadas

| Herramienta       | Descripción                            |
| ----------------- | -------------------------------------- |
| **Python 3.12**   | Lenguaje principal del backend y la UI |
| **Tkinter**       | Biblioteca para interfaces gráficas    |
| **PostgreSQL**    | Base de datos relacional               |
| **Supabase**      | Backend as a Service (DB y API REST)   |
| **.env / dotenv** | Manejo seguro de credenciales          |
| **Git + GitHub**  | Control de versiones y colaboración    |

---

## 🧱 Arquitectura del Proyecto (MVC)

* **Modelo (Model):**

  * Tablas de base de datos diseñadas en Supabase.
  * Relaciones entre usuarios, médicos, pacientes, turnos, etc.

* **Vista (View):**

  * Interfaces diseñadas en Tkinter, separadas por tipo de usuario.
  * Todas ubicadas dentro de `/ui/`.

* **Controlador (Controller):**

  * Código Python que conecta la vista con Supabase.
  * Responsable de la lógica de negocio (alta, baja, validación, queries).

---

## 📁 Estructura del Proyecto

```bash
.
├── controllers/                  # Controladores del sistema (lógica de negocio)
│   ├── admin_controller.py
│   ├── auth_controller.py
│   ├── inst_controller.py
│   ├── med_controller.py
│   └── pac_controller.py
├── database/                     # Conexión y modelos DB
│   ├── db_manager.py
│   └── models.py
├── ui/                           # Interfaz gráfica (Tkinter)
│   ├── admin/
│   │   ├── dashboard.py
│   │   ├── reports.py
│   │   └── users.py
│   ├── common/
│   │   ├── assets/
│   │   ├── utils.py
│   │   └── widgets.py
│   ├── institucion/
│   │   ├── agenda.py
│   │   ├── config.py
│   │   ├── dashboard.py
│   │   ├── horarios.py
│   │   └── medicos.py
│   ├── medicos/
│   │   ├── agenda.py
│   │   ├── dashboard.py
│   │   ├── datosMedico.py
│   │   ├── horarios.py
│   │   └── pacientes.py
│   ├── pacientes/
│   │   ├── app.py
│   │   ├── login.py
│   │   ├── loginInterface.py
│   │   └── register.py
├── utils/
│   ├── config.py
│   └── env/
├── .env
├── main.py
├── README.md
├── logo-genezis-new.png
├── requirements.txt
└── test_connection.py
```

---

## 🗃️ Diseño de Base de Datos (Supabase / PostgreSQL)

### Tablas principales:

| Tabla                  | Descripción                                                |
| ---------------------- | ---------------------------------------------------------- |
| `usuarios`             | Datos base (nombre, mail, tipo\_usuario, etc.)             |
| `medicos`              | Datos personales, matrícula, especialidad, duración\_turno |
| `pacientes`            | Información médica, contacto y afiliación                  |
| `turnos`               | Fecha, hora, motivo de consulta, estado, notas             |
| `horarios_disponibles` | Fecha, hora\_inicio, hora\_fin, validación                 |
| `instituciones`        | Datos de instituciones y sus usuarios                      |
| `especialidades`       | Catálogo de especialidades médicas                         |

### Relaciones principales:

* `medicos.usuario_id` → `usuarios.id`
* `pacientes.usuario_id` → `usuarios.id`
* `medicos.institucion_id` → `instituciones.id`
* `turnos.medico_id` → `medicos.id`
* `turnos.paciente_id` → `pacientes.id`
* `horarios_disponibles.medico_id` → `medicos.id`
---

## 🎛️ Funcionalidades por panel

### 👤 Panel Médico

* Visualizar turnos del día actual
* Confirmar, cancelar y completar turnos
* Agregar y editar horarios de disponibilidad
* Evitar solapamiento de horarios duplicados
* Historial de turnos por paciente

### 🧑‍⚕️ Panel Paciente

* Buscar médicos por especialidad
* Reservar turnos con horarios disponibles
* Cancelar turnos próximos
* Visualizar historial de turnos
* Consultar estado (pendiente, completado, cancelado)

### 🏥 Panel Institución

* Crear, editar y eliminar instituciones
* Gestionar médicos asociados
* Visualizar agenda médica por especialidad
* Consultar estadísticas de turnos

### 👨‍💼 Panel Administrador

* Ver todos los usuarios y su rol
* Editar o eliminar instituciones
* Generar reportes globales
* Control general del sistema

---

## 📆 Sprints y metodología Scrum

El desarrollo se llevó a cabo en un Sprint extendido de 30 días, luego dividido formalmente en dos sprints de 15 días cada uno, aplicando la metodología Scrum para una entrega colaborativa, organizada y funcional.

### 🏁 Sprint 1 - Fundamentos (1 al 15 de junio)

* Autenticación de usuarios (registro y login)
* Estructura de base de datos y conexión con Supabase
* Implementación de controladores para usuarios, médicos, horarios
* Interfaz principal del médico (Dashboard, Agenda, Pacientes)

### 🧩 Sprint 2 - Funcionalidad extendida (16 al 30 de junio)

* Módulo de pacientes: reserva de turnos, historial, cancelación
* Panel institucional: CRUD de instituciones y gestión de médicos
* Panel administrador: usuarios, estadísticas, reportes
* Validaciones de superposición de horarios y duplicación
* Documentación técnica y README completo

---

## 🧪 ¿Cómo ejecutar el sistema localmente?

### 1. Clonar el repositorio

```bash
git clone https://github.com/PowerSystem2024/PowerSystem2024-App-StartUp-Genezis.git
cd PowerSystem2024-App-StartUp-Genezis
```

### 2. Crear un entorno virtual y activarlo

```bash
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar tu archivo `.env`

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-service-role-key
```

### 5. Ejecutar la aplicación

```bash
python main.py
```

---

## 👥 Equipo de desarrollo

| Integrante        | Rol                  |
|-------------------| -------------------- |
| Luciano Cortez    | Módulo Institución   |
| Gabriel Garino    | Módulo Institución   |
| Nicolás Fernandez | Módulo Médico        |
| Fernando Alma     | Módulo Médico        |
| Marcos Rodriguez  | Módulo Paciente      |
| Brisa Salvatierra | Módulo Paciente      |
| Javier Quiroga    | Panel Administrativo |

---

## 🚀 Mejoras futuras (Backlog)

* 🔔 Notificaciones de turnos por email o SMS
* 📅 Vista de calendario general por especialidad
* 📅 Integración de API de Google Calendar
* 🤖 Integración de agente virtual con IA
* 📊 Panel de estadísticas y reportes para admins
* 🌐 Exportación e importación de datos
* 🧑‍💼 Gestión de usuarios por parte de admins
* 🌍 Multi-idioma (ES, EN, etc.)
* 🖥️ Versión web en React o Flutter (Fase 3)

---

## 📆 Timeline del Proyecto


| Fase     | Fecha                       | Tareas principales                                                                                  |
| -------- |-----------------------------|-----------------------------------------------------------------------------------------------------|
| Sprint 1 | Primer Quincena Junio 2025  | Login, módulo médico, conexión Supabase                                                             |
| Sprint 2 | Segunda Quincena Junio 2025 | Módulo pacientes, edición de horarios, validaciones, panel administrador, pruebas, mejoras visuales |
---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Podés usarlo, modificarlo y compartirlo libremente.

---

## 🧩 Diagramas del Sistema

### 📊 Diagrama Entidad-Relación (DER)

![Diagrama ER](DER%20-%20App%20de%20Turnos%20Genezis.png)

### 🧱 Diagrama UML de Clases

![Diagrama UML](Diagrama%20UML%20-%20App%20de%20Turnos%20Genezis.png)

---

> Para cualquier consulta técnica o colaboración, contactanos a través del repositorio o vía mail.

---

Gracias por usar **Genezis** 💙

# Integrantes de Genezis: 

1. Brisa Salvatierra
2. Javier Quiroga
3. Fernando Alma
4. Gabriel Garino
5. Marcos Rodriguez
6. Luciano Cortez
7. Nicolas Fernandez

