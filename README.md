# 🎓 School Management System - Odoo 8

Un sistema integral de gestión escolar desarrollado para Odoo 8 que permite administrar estudiantes, profesores, cursos, aulas, horarios y exámenes con diferentes niveles de acceso según el rol del usuario.

## 📋 Tabla de Contenidos

- [🎯 Características Principales](#-características-principales)
- [👥 Roles y Permisos](#-roles-y-permisos)
- [🏗️ Estructura del Proyecto](#️-estructura-del-proyecto)
- [🔧 Funcionalidades por Módulo](#-funcionalidades-por-módulo)
- [🚀 Instalación en Oracle Cloud](#-instalación-en-oracle-cloud)
- [📦 Instalación del Módulo](#-instalación-del-módulo)
- [🔍 Solución de Problemas](#-solución-de-problemas)
- [📝 Notas Importantes](#-notas-importantes)

## 🎯 Características Principales

### ✨ Sistema de Roles Multi-nivel
- **Super Admin**: Control total del sistema
- **Teacher (Profesor)**: Gestión de clases y estudiantes asignados
- **Student (Estudiante)**: Vista de solo lectura de información personal

### 🔐 Seguridad Avanzada
- Autenticación basada en grupos de seguridad
- Filtrado de datos por nivel de usuario
- Vistas específicas sin botones de acción para estudiantes
- Control de acceso a menus por rol

### 📊 Gestión Completa
- Administración de estudiantes y profesores
- Control de aulas y capacidades
- Programación de horarios
- Sistema de exámenes y calificaciones
- Reportes detallados por módulo

## 👥 Roles y Permisos

### 🔴 Super Admin
**Acceso:** Control total del sistema
```
✅ Crear, editar, eliminar todos los registros
✅ Gestionar usuarios y perfiles de acceso
✅ Asignar roles a usuarios
✅ Acceso a todos los reportes
✅ Configuración del sistema
✅ Wizards de gestión avanzada
```

### 🟡 Teacher (Profesor)
**Acceso:** Gestión de clases asignadas
```
✅ Ver y gestionar estudiantes de sus cursos
✅ Crear perfiles de estudiantes
✅ Gestionar exámenes y calificaciones
✅ Ver horarios de sus clases
✅ Reportes de sus cursos
❌ No puede gestionar otros profesores
❌ No puede modificar configuración del sistema
```

### 🟢 Student (Estudiante)
**Acceso:** Vista de solo lectura
```
✅ Ver sus cursos asignados
✅ Ver horarios de sus clases
✅ Ver información de aulas
✅ Ver sus exámenes y calificaciones
❌ Sin botones de crear/editar/eliminar
❌ Solo ve información relacionada a él
❌ No puede acceder a datos de otros estudiantes
```

## 🏗️ Estructura del Proyecto

```
school_management/
├── 📄 __init__.py                       # Inicialización del módulo
├── 📄 __openerp__.py                    # Manifiesto del módulo
├── 📁 data/                             # Datos de demostración
│   ├── 📄 alumnos_demo.xml             # Datos demo de estudiantes
│   ├── 📄 aulas_demo.xml               # Datos demo de aulas
│   ├── 📄 cursos_demo.xml              # Datos demo de cursos
│   ├── 📄 examenes_demo.xml            # Datos demo de exámenes
│   ├── 📄 horarios_demo.xml            # Datos demo de horarios
│   └── 📄 post_install.xml             # Configuración post-instalación
├── 📁 models/                           # Modelos de datos
│   ├── 📄 __init__.py                  # Inicialización de modelos
│   ├── 📄 alumnos.py                   # 👨‍🎓 Gestión de estudiantes
│   ├── 📄 aulas.py                     # 🏫 Gestión de aulas
│   ├── 📄 cursos.py                    # 📚 Gestión de cursos
│   ├── 📄 examenes.py                  # 📝 Sistema de exámenes
│   ├── 📄 horarios.py                  # ⏰ Programación de horarios
│   └── 📄 school_users_simple.py      # 👤 Gestión de usuarios y roles
├── 📁 security/                         # Configuración de seguridad
│   ├── 📄 groups.xml                   # Definición de grupos de usuarios
│   ├── 📄 ir.model.access.csv        # Permisos de acceso a modelos
│   └── 📄 record_rules.xml            # Reglas de filtrado de datos
├── 📁 views/                           # Interfaces de usuario
│   ├── 📄 alumnos_view.xml            # Vistas principales de estudiantes
│   ├── 📄 alumno_creation_wizard_view.xml  # Vista wizard creación estudiantes
│   ├── 📄 alumno_wizard_view.xml      # Vista wizard gestión estudiantes
│   ├── 📄 aulas_view.xml              # Vistas de aulas
│   ├── 📄 aula_wizard_view.xml        # Vista wizard gestión aulas
│   ├── 📄 calificaciones_view.xml     # Vistas de calificaciones
│   ├── 📄 cursos_view.xml             # Vistas de cursos
│   ├── 📄 curso_wizard_view.xml       # Vista wizard gestión cursos
│   ├── 📄 examenes_view.xml           # Vistas de exámenes
│   ├── 📄 examen_wizard_view.xml      # Vista wizard gestión exámenes
│   ├── 📄 horarios_view.xml           # Vistas de horarios
│   ├── 📄 horario_wizard_view.xml     # Vista wizard gestión horarios
│   ├── 📄 school_menu.xml             # 🏠 Menú principal del sistema
│   ├── 📄 school_users_view.xml       # Vista de gestión de usuarios
│   └── 📄 student_readonly_views.xml  # 👁️ Vistas de solo lectura para estudiantes
├── 📁 wizard/                          # Asistentes de configuración
│   ├── 📄 __init__.py                 # Inicialización de wizards
│   ├── 📄 alumno_creation_wizard.py   # 🧙‍♂️ Wizard creación de estudiantes
│   ├── 📄 alumno_wizard.py            # Wizard gestión de estudiantes
│   ├── 📄 aula_wizard.py              # Wizard gestión de aulas
│   ├── 📄 curso_wizard.py             # Wizard gestión de cursos
│   ├── 📄 examen_wizard.py            # Wizard gestión de exámenes
│   └── 📄 horario_wizard.py           # Wizard gestión de horarios
├── 📁 reports/                         # Sistema de reportes
│   ├── 📄 __init__.py                 # Inicialización de reportes
│   ├── 📄 school_reports.py           # Lógica de generación de reportes
│   ├── 📄 reporte_alumnos.xml         # Reporte de estudiantes
│   ├── 📄 reporte_aulas.xml           # Reporte de aulas
│   ├── 📄 reporte_cursos.xml          # Reporte de cursos
│   ├── 📄 reporte_examenes.xml        # Reporte de exámenes
│   └── 📄 reporte_horarios.xml        # Reporte de horarios
└── 📄 README.md                        # 📖 Este archivo de documentación
```

## 🔧 Funcionalidades por Módulo

### 👨‍🎓 Gestión de Estudiantes (`alumnos.py`)
- **Registro completo**: Datos personales, contacto, información académica
- **Número de estudiante**: Generación automática basada en el año
- **Asignación de aulas**: Control de capacidad y ocupación
- **Validaciones**: Email único, capacidad de aulas, eliminación segura
- **Campos computados**: Estado académico, promedio general

### 🏫 Gestión de Aulas (`aulas.py`)
- **Control de capacidad**: Límites máximos y disponibilidad
- **Estadísticas en tiempo real**: Ocupación, estudiantes actuales
- **Validaciones de seguridad**: Previene eliminación con estudiantes asignados
- **Porcentaje de ocupación**: Cálculo automático

### 📚 Gestión de Cursos (`cursos.py`)
- **Información académica**: Código, créditos, descripción
- **Asignación de profesores**: Relación con usuarios del sistema
- **Estadísticas**: Total de estudiantes, exámenes, promedio general
- **Validaciones**: Código único, eliminación segura

### ⏰ Programación de Horarios (`horarios.py`)
- **Horarios detallados**: Día, hora inicio/fin, duración
- **Prevención de conflictos**: Validación de solapamiento
- **Formato de tiempo**: Conversión automática a formato legible
- **Turnos**: Matutino y vespertino

### 📝 Sistema de Exámenes (`examenes.py`)
- **Tipos de evaluación**: Parcial, final, quiz, proyecto, tarea
- **Gestión de calificaciones**: Sistema completo de puntuación
- **Estadísticas**: Promedios, aprobados, reprobados
- **Generación automática**: Calificaciones para todos los estudiantes

### 👤 Gestión de Usuarios (`school_users_simple.py`)
- **Sistema de roles**: Super Admin, Teacher, Student
- **Creación de perfiles**: Wizard intuitivo con validaciones
- **Asignación automática**: Relación usuario-estudiante
- **Numeración inteligente**: IDs únicos por año académico

## 🚀 Instalación en Oracle Cloud

### 📋 Prerrequisitos
- Cuenta en Oracle Cloud con instancia Ubuntu 22.04
- Acceso SSH al servidor
- Llave SSH configurada localmente

### 🔑 Configuración de Llave SSH

#### 1. Generar llave SSH (en tu computadora local)
```cmd
# Generar nueva llave SSH (en Windows CMD o PowerShell)
ssh-keygen -t rsa -b 4096 -C "tu-email@ejemplo.com" -f %USERPROFILE%\.ssh\odoo8_oracle

# Ver la llave pública para configurar en Oracle Cloud
type %USERPROFILE%\.ssh\odoo8_oracle.pub
```

#### 2. Configurar llave en Oracle Cloud
1. Ir al portal de Oracle Cloud
2. Navegar a "Compute" > "Instances"
3. En la instancia, ir a "Console Connection" > "SSH Keys"
4. Pegar el contenido de la llave pública (`odoo8_oracle.pub`)

#### 3. Conectarse al servidor
```bash
ssh -i %USERPROFILE%\.ssh\odoo8_oracle ubuntu@TU_IP_SERVIDOR
```

### 🔧 Configuración Inicial del Servidor

#### 1. Actualizar sistema e instalar dependencias
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release
```

#### 2. Instalar Docker
```bash
# Agregar repositorio oficial de Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) stable" \
| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Configurar Docker para usar sin sudo
sudo usermod -aG docker $USER
newgrp docker
```

#### 3. Crear estructura de directorios
```bash
sudo mkdir -p /opt/odoo/{addons,nginx,postgresql,odoo_data}
sudo chown -R $USER:$USER /opt/odoo
cd /opt/odoo
```

#### 4. Configurar archivos de configuración

**Archivo de configuración de Odoo (`odoo.conf`):**
```bash
cat > /opt/odoo/odoo.conf <<'EOF'
[options]
admin_passwd = admin123**
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = /usr/lib/python2.7/dist-packages/openerp/addons,/mnt/extra-addons
logfile = /var/log/odoo/odoo.log
logrotate = True
xmlrpc_port = 8069
longpolling_port = 8072
workers = 0
limit_memory_soft = 268435456
limit_memory_hard = 402653184
limit_time_cpu = 60
limit_time_real = 120
EOF
```

**Configuración de NGINX (`nginx/odoo.conf`):**
```bash
cat > /opt/odoo/nginx/odoo.conf <<'EOF'
upstream odoo {
    server odoo:8069;
}
upstream odoo_longpolling {
    server odoo:8072;
}

server {
    listen 80;
    server_name _;

    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;

    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-For  $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP        $remote_addr;

    client_max_body_size 128m;

    location /longpolling/ {
        proxy_pass http://odoo_longpolling;
    }

    location / {
        proxy_redirect off;
        proxy_pass http://odoo;
    }

    access_log /var/log/nginx/odoo_access.log;
    error_log  /var/log/nginx/odoo_error.log;
}
EOF
```

**Archivo Docker Compose (`docker-compose.yml`):**
```bash
cat > /opt/odoo/docker-compose.yml <<'EOF'
version: "3.8"

services:
  db:
    image: postgres:9.6
    restart: unless-stopped
    environment:
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
      POSTGRES_DB: postgres
    volumes:
      - ./postgresql:/var/lib/postgresql/data

  odoo:
    image: odoo:8
    depends_on:
      - db
    restart: unless-stopped
    ports:
      - "8069:8069"
      - "8072:8072"
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
    volumes:
      - ./odoo_data:/var/lib/odoo
      - ./addons:/mnt/extra-addons
      - ./odoo.conf:/etc/odoo/odoo.conf
    command: ["--config=/etc/odoo/odoo.conf"]

  nginx:
    image: nginx:stable
    depends_on:
      - odoo
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx/odoo.conf:/etc/nginx/conf.d/odoo.conf:ro
EOF
```

### 🏃‍♂️ Despliegue de la Aplicación

#### 5. Iniciar los servicios
```bash
cd /opt/odoo
docker compose pull
docker compose up -d
docker compose ps
```

#### 6. Configurar permisos de Odoo
```bash
docker compose down odoo

docker compose run --rm --user root odoo bash

mkdir -p /var/lib/odoo/sessions
mkdir -p /var/lib/odoo/addons/8.0
chown -R odoo:odoo /var/lib/odoo
chmod -R 700 /var/lib/odoo
exit

docker compose down
docker compose up -d
```

#### 7. Verificar instalación
Acceder a: `http://TU_IP_SERVIDOR:8069`

## 📦 Instalación del Módulo

### Para instalar el módulo School Management:

#### 1. Transferir módulo desde tu computadora al servidor
```cmd
# Desde CMD o PowerShell en Windows
cd RUTA_DONDE_TIENES_TU_MODULO
scp -i %USERPROFILE%\.ssh\odoo8_oracle -r school_management ubuntu@TU_IP_SERVIDOR:/tmp/
```

#### 2. Mover y configurar permisos en el servidor
```bash
# Conectarse al servidor
ssh -i %USERPROFILE%\.ssh\odoo8_oracle ubuntu@TU_IP_SERVIDOR

# Mover el módulo a la carpeta de addons
sudo mv /tmp/school_management /opt/odoo/addons/

# Eliminar carpeta .git si existe
sudo rm -rf /opt/odoo/addons/school_management/.git

# Configurar permisos correctos
cd /opt/odoo/addons
sudo chown -R 1000:1000 school_management/
sudo chmod -R 755 school_management/
```

#### 3. Verificar desde el contenedor
```bash
# Verificar que Odoo puede acceder a los archivos
sudo docker compose exec odoo ls -la /mnt/extra-addons/school_management/

# Reiniciar Odoo para detectar el nuevo módulo
sudo docker compose restart odoo

# Ver logs de instalación
sudo docker compose logs odoo | grep -i school
```

#### 4. Instalar en Odoo
1. Acceder a Odoo: `http://TU_IP_SERVIDOR`
2. Ir a **Apps** → **Actualizar lista de aplicaciones**
3. Buscar "**school_management**"
4. **Instalar** el módulo

### 🎯 Acceso al Sistema

Una vez instalado el módulo:

1. **Menú principal**: Ir a "School Management"
2. **Crear perfiles**: Solo Super Admin puede crear perfiles de acceso
3. **Gestión de roles**: 
   - Super Admin: Acceso total
   - Teachers: Pueden crear estudiantes
   - Students: Solo lectura de su información

## 🔍 Solución de Problemas

### Verificar servicios
```bash
# Estado de los contenedores
docker compose ps

# Logs de Odoo
docker compose logs odoo

# Logs de NGINX
docker compose logs nginx
```

### Verificar permisos de módulos
```bash
# Desde el host
ls -la /opt/odoo/addons/school_management/

# Desde el contenedor
docker compose exec odoo ls -la /mnt/extra-addons/school_management/
```

### Comandos útiles de administración
```bash
# Reiniciar servicios específicos
sudo docker compose restart odoo nginx

# Detener todos los servicios
sudo docker compose down

# Iniciar servicios
sudo docker compose up -d

# Ver uso de recursos
sudo docker stats
```

### Problemas comunes

#### ❌ Error de permisos
**Síntoma:** El módulo no aparece en la lista de aplicaciones
**Solución:**
```bash
sudo chown -R 1000:1000 /opt/odoo/addons/school_management/
sudo chmod -R 755 /opt/odoo/addons/school_management/
sudo docker compose restart odoo
```

#### ❌ Error de sintaxis Python 2.7
**Síntoma:** Errores de instalación relacionados con sintaxis
**Solución:** Este módulo está optimizado para Python 2.7/Odoo 8

#### ❌ Menús no visibles
**Síntoma:** Los usuarios no ven los menús correspondientes
**Solución:** Verificar que el usuario tenga el grupo correcto asignado

## 📝 Notas Importantes

### 🔒 Seguridad
- **Contraseña por defecto**: Cambiar `admin123**` en producción
- **Grupos de usuarios**: El sistema automáticamente asigna grupos según el rol
- **Filtrado de datos**: Los estudiantes solo ven su información personal

### 💾 Datos
- **Ruta de módulos**: `/opt/odoo/addons/` se mapea a `/mnt/extra-addons/` dentro del contenedor
- **Base de datos**: Se almacena en `/opt/odoo/postgresql/`
- **Logs**: Disponibles mediante `docker compose logs`

### ⚙️ Configuración
- **Permisos**: Usar UID 1000 y permisos 755 para módulos
- **Reinicios**: Siempre reiniciar Odoo después de agregar nuevos módulos
- **Recursos**: Configurado para instancias con 1GB RAM

### 📊 Rendimiento
- **Workers**: Configurado en 0 para instancias pequeñas
- **Límites de memoria**: Optimizado para Oracle Cloud Free Tier
- **Proxy**: NGINX como proxy inverso para mejor rendimiento

## 🎯 Resumen de lo Implementado

### ✅ Infraestructura Completa
- **Odoo 8** en contenedores Docker
- **PostgreSQL 9.6** como base de datos
- **NGINX** como proxy reverso
- **Configuración optimizada** para recursos limitados (1GB RAM)
- **Estructura organizada** para módulos personalizados
- **Permisos y seguridad** adecuados
- **Acceso vía web** en el puerto 80

### ✅ Sistema de Gestión Escolar
- **3 niveles de usuario** con permisos específicos
- **Gestión completa** de estudiantes, profesores y cursos
- **Sistema de horarios** con prevención de conflictos
- **Exámenes y calificaciones** con estadísticas automáticas
- **Reportes detallados** por módulo
- **Vistas específicas** para cada tipo de usuario

### 🔄 Flujo para agregar módulos personalizados:
1. Transferir módulo al servidor vía SCP
2. Mover a `/opt/odoo/addons/`
3. Configurar permisos (1000:1000 y 755)
4. Reiniciar Odoo
5. Instalar desde la interfaz web

### 📁 Estructura final de directorios:
```
/opt/odoo/
├── addons/          # Módulos personalizados (school_management aquí)
├── nginx/           # Configuración de NGINX
├── postgresql/      # Base de datos
├── odoo_data/       # Datos de Odoo
├── odoo.conf        # Configuración de Odoo
└── docker-compose.yml
```

---

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades:
1. Revisar la sección de "Solución de Problemas"
2. Verificar logs de Odoo: `docker compose logs odoo`
3. Contactar al administrador del sistema

---

**Desarrollado para Odoo 8 | Compatible con Python 2.7 | Oracle Cloud Free Tier Optimized**