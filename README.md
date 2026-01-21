# **Hotel La J Elegante - Sistema de Gestión Hotelera**
![Java](https://img.shields.io/badge/Java-EE7-red?logo=java)
![PHP](https://img.shields.io/badge/PHP-8.2-blue?logo=php)
![Laravel](https://img.shields.io/badge/Laravel-10.x-orange?logo=laravel)
![License](https://img.shields.io/badge/License-Academic-green)
![GitHub last commit](https://img.shields.io/github/last-commit/Xanderm0/LaJElegante)

## 🚀 Tabla de Contenidos
1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Stack Tecnológico](#-stack-tecnológico)
3. [Estado del Proyecto](#-estado-del-proyecto)
4. [Estructura del Repositorio](#-estructura-del-repositorio)
5. [Instalación y Configuración](#-instalación-y-configuración)
6. [Documentación Técnica](#-documentación-técnica)
7. [Equipo y Contribuciones](#-equipo-y-contribuciones)
8. [Rutas de Aprendizaje](#-rutas-de-aprendizaje)
9. [Licencia](#-licencia)

## 📋 Descripción del Proyecto
**Problema Académico que Resolvemos:** Como proyecto educativo, identificamos un escenario común en la hotelería: la gestión manual y dispersa de reservas que lleva a errores operativos, sobreocupación y mala experiencia del cliente. Decidimos crear "La J Elegante", un hotel ficticio, para desarrollar una solución tecnológica completa.

**Objetivo del Sistema:** Centralizar y optimizar la gestión de reservas, operaciones y administración del hotel, eliminando la dispersión de información causada por la gestión manual y mejorando la eficiencia operativa.

**Características Clave:**
- Gestión de reservas de habitaciones y restaurantes
- Administración de usuarios con roles y permisos diferenciados
- Configuración de tarifas y políticas dinámicas
- Dashboard administrativo con métricas (Chart.js)

**Metas de Eficiencia:** Reducir en un 80% los errores operativos mediante automatización.

**📝 Nota Académica:** Este es un proyecto educativo desarrollado por estudiantes de tecnología. La empresa "Hotel La J Elegante" es ficticia, creada para aplicar conocimientos de desarrollo web en un contexto realista. El problema a resolver fue planteado por el equipo como ejercicio de análisis de sistemas.

## 🛠 Stack Tecnológico
### **Tecnologías Comunes a Todas las Implementaciones**
- **Frontend:** Bootstrap 5 (estilos responsivos), Chart.js (gráficos y métricas)
- **Patrón de Diseño:** MVC (Model-View-Controller)
- **Base de Datos:** MySQL (principal), con posibilidad de adaptación
- **Control de Versiones:** Git + GitHub

### **Implementaciones Activas**
| Lenguaje | Framework | Versión | Estado | Dependencias Principales |
|----------|-----------|---------|--------|--------------------------|
| Java | Jakarta EE (JSF 2.1) | Java EE 7, GlassFish | 🔄 **En Desarrollo** | PrimeFaces, MySQL Connector, Ant |
| PHP | Laravel | 10.x (PHP 8.2) | 🔄 **En Desarrollo** | dompdf, Laravel Excel, Eloquent ORM |
| Python | Por definir | Por definir | ⏳ **Planificado** | - |
| C# | Por definir | Por definir | ⏳ **Planificado** | - |

## 📈 Estado del Proyecto
**Progreso General: < 20%** - Fase inicial de CRUDs básicos

### **✅ Historias de Usuario Completadas**

### **🔄 En Desarrollo (Sprint Actual)**

### **⏳ Pendientes (Backlog)**

## 📁 Estructura del Repositorio
**Estrategia de Ramas:**
```
main/                      # Proyecto ACTUAL del trimestre
│
├── laravel/               # Rama principal para PHP/Laravel
│   ├── laravel-jeremy/    # Rama personal de Jeremy
│   └── ... (otros desarrolladores)
│
├── java/                  # Rama principal para Java/JSF
│   ├── java-jeremy/       # Rama personal de Jeremy
│   ├── java-julian/       # Rama personal de Julián
│   └── java-javier/       # Rama personal de Javier
│   
├── python/                # (Futuro) Rama para Python
│   ├── python-jeremy/       # Rama personal de Jeremy
│   ├── python-julian/       # Rama personal de Julián
│   └── python-javier/       # Rama personal de Javier
│
└── csharp/                # (Futuro) Rama para C#
    ├── csharp-jeremy/       # Rama personal de Jeremy
    ├── csharp-julian/       # Rama personal de Julián
    └── csharp-javier/       # Rama personal de Javier
```

### **📌 Importante: Estrategia de Ramas**
Este proyecto utiliza **ramas especializadas por lenguaje**. No uses la rama `main` directamente ya que rota según el trimestre académico.

## ⚙️ Instalación y Configuración

### **🟠 PHP/Laravel (Rama: `laravel`)**

#### **Requisitos Previos:**
- PHP 8.2 o superior
- Composer 2.5+
- MySQL 8.0+
- Git

#### **Pasos de Instalación:**
```bash
# 1. Clonar el repositorio y acceder a la rama laravel
git clone https://github.com/Xanderm0/LaJElegante.git
cd LaJElegante
git checkout laravel

# 2. Instalar dependencias de PHP
composer install

# 3. Configurar variables de entorno
cp .env.example .env
# ⚠️ EDITAR el archivo .env con tus credenciales:
# DB_DATABASE=hotellje
# DB_USERNAME=tu_usuario
# DB_PASSWORD=tu_contraseña

# 4. Generar clave de aplicación
php artisan key:generate

# 5. Crear la base de datos (ejecutar en MySQL)
CREATE DATABASE hotel_la_j_elegante CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 6. Ejecutar migraciones y seeders
php artisan migrate --seed

# 7. (Opcional) Instalar dependencias frontend
npm install && npm run build

# 8. Iniciar servidor de desarrollo
php artisan serve

# 9. Acceder en el navegador:
# 🌐 http://localhost:8000
```

#### **Credenciales de Prueba (creadas por seeders):**
- **Administrador:** admin@lajelegante.com / password123
- **Recepcionista:** recepcion@lajelegante.com / password123

---

### **🔵 Java/JSF (Rama: `java`)**

#### **Requisitos Previos:**
- Java JDK 11 o superior
- Apache NetBeans 13+ (recomendado)
- GlassFish Server 6.2+
- MySQL 8.0+
- Git

#### **Opción A: Con NetBeans (Recomendada)**
```bash
# 1. Clonar y cambiar a rama java
git clone https://github.com/Xanderm0/LaJElegante.git
cd LaJElegante
git checkout java

# 2. Abrir NetBeans y seleccionar:
#    File → Open Project → Seleccionar carpeta "java"

# 3. Configurar GlassFish Server:
#    - Services → Servers → Add Server
#    - Seleccionar GlassFish 6.2+
#    - Descargar si no está instalado

# 4. Configurar Base de Datos MySQL:
#    - Services → Databases → New Connection
#    - MySQL (Connector/J driver)
#    - Host: localhost, Port: 3306
#    - Database: hotellje -> puedes encontrar esta base de datos en el drive
#    - User: root (o tu usuario)

# 5. Ejecutar script SQL inicial:
#    Ubicación: /java/docs/database/init.sql
#    Ejecutar en MySQL Workbench o línea de comandos

# 6. Ejecutar proyecto:
#    Click derecho en proyecto → Run
#    🌐 http://localhost:8080/HotelLaJElegante/
```

#### **Opción B: Línea de Comandos**
```bash
# 1. Clonar repositorio
git clone -b java https://github.com/Xanderm0/LaJElegante.git
cd LaJElegante

# 2. Instalar Base de Datos MySQL:
#  hotellje -> puedes encontrar esta base de datos en el drive

# 3. Compilar con Ant (desde carpeta /java)
cd java
ant compile

# 4. Crear archivo WAR
ant war
# Se generará: dist/HotelLaJElegante.war

# 5. Desplegar en GlassFish manualmente:
# Copiar el .war a: [glassfish-install]/domains/domain1/autodeploy/

# 6. Iniciar GlassFish:
# [glassfish-install]/bin/asadmin start-domain

# 7. Acceder vía navegador:
# 🌐 http://localhost:8080/HotelLaJElegante/
```
## 📚 Documentación Técnica
### **Enlaces a Documentación Completa**
- **[Documentación General en Drive](https://drive.google.com/drive/folders/14hGh5fvlVhJBpGYN0-jRrzCacsubTl8S?usp=sharing)** - Requisitos, diagramas, planificación, reglas de negocio
- **Diagramas PlantUML:** Disponibles en `/java/docs/diagrams/` y `/laravel/docs/diagrams/`
- **Modelo de Datos:** Diagramas en cada carpeta `/docs/`

### **Decisiones de Arquitectura**
1. **Patrón MVC Estricto:** Separación clara entre lógica, datos y presentación
2. **Base de Datos Unificada:** Mismo esquema para todas las implementaciones, pequeñas variaciones entre lenguajes para implementar auditoria
3. **Bootstrap como Framework UI:** Consistencia visual entre implementaciones
4. **Chart.js para Analytics:** Gráficos unificados en dashboard administrativo

### **Diagramas Disponibles**
- Diagrama de Casos de Uso
- Diagrama de Clases (por lenguaje)
- Diagrama de Despliegue (por lenguaje)
- Diagrama de Base de Datos (ER) (por lenguaje y base inicial)
- Modelo Relacional
- Historias de Usuario

## 👥 Equipo y Contribuciones
### **Roles del Equipo Scrum**
| Nombre | Rol | Especialización | Ramas Principales |
|--------|-----|----------------|-------------------|
| **Jeremy Duarte** | SCRUM Master | Arquitectura, Coordinación | `laravel-jeremy`, `java-jeremy`, `python-jeremy`, , `csharp-jeremy` |
| **Julián Suárez** | Development Team | Backend, Lógica de Negocio | `java-julian`, `python-julian`, `csharp-julian` |
| **Javier Peñata** | Product Owner | Requisitos, Testing | `java-javier` , `python-javier`, `csharp-javier` |

### **Política de Contribución**
1. **Flujo de Trabajo:**
   - Cada desarrollador trabaja en su rama personal (`program-languaje-dev`)
   - Pull desde la rama principal del lenguaje trabajado (`program-languaje-dev` ← `program-languaje`)
   - Merge a la rama principal del lenguaje (`program-languaje-dev` → `program-languaje`)
   - Revisión por pares antes de merge a main

2. **Commits Semánticos:**
   ```bash
   feat: add reservation validation (HU-004)
   fix: correct date calculation in booking
   docs: update installation guide for Java
   refactor: optimize room availability query
   ```

3. **Visualización de Contribuciones:**
   - GitHub Insights: [https://github.com/Xanderm0/LaJElegante/graphs/contributors](https://github.com/Xanderm0/LaJElegante/graphs/contributors)
   - Cada rama personal muestra el trabajo individual

## 🎯 Rutas de Aprendizaje
**Como Estudiantes de Tecnología, Buscamos:**

### **Objetivos de Aprendizaje Técnico:**
- ✅ **Comparar Implementaciones:** MVC en Java EE vs Laravel
- 🔄 **Patrones de Diseño:** Aplicar Factory, Singleton, Strategy en contexto real
- 🔄 **ORM vs SQL Directo:** Experiencia con Eloquent (Laravel) y JDBC (Java)
- ⏳ **Despliegue Multi-Entorno:** Local, desarrollo, producción
- ⏳ **Integración Continua:** GitHub Actions para testing automático

### **Objetivos de Gestión de Proyectos:**
- ✅ **Metodología Scrum:** Roles, sprints, historias de usuario
- 🔄 **Control de Versiones:** Git avanzado (ramas, merges, conflictos)
- 🔄 **Documentación Profesional:** READMEs, wikis, diagramas técnicos
- ⏳ **Trabajo Colaborativo:** Code reviews, pair programming

### **Lecciones Aprendidas (Espacio para Reflexión)**
*"En esta fase inicial, descubrimos que la planeación de la base de datos es crítica antes de cualquier implementación. Un modelo de datos bien diseñado ahorra horas de refactorización."*

## 📄 Licencia
Este es un proyecto **académico educativo** sin licencia comercial. El código puede ser usado como referencia para fines de aprendizaje. 

**Restricciones:**
- No puede ser usado con fines comerciales
- Atribución a los autores requerida
- Sin garantías de ningún tipo

**Uso Académico Libre:** Profesores y estudiantes pueden usar, modificar y distribuir este código con propósitos educativos.

---

## ❓ Preguntas Frecuentes
**Q: ¿Por qué múltiples implementaciones del mismo sistema?**  
R: Como ejercicio académico, nos permite comparar enfoques, frameworks y mejores prácticas en diferentes ecosistemas tecnológicos.

**Q: ¿Cómo selecciono qué versión usar?**  
R: Depende de tu stack tecnológico familiar:
- Si conoces PHP → Usa la versión Laravel
- Si trabajas con Java EE → Usa la versión JSF
- Para aprendizaje → Recomendamos comparar ambas

**Q: ¿Dónde reporto bugs o sugiero mejoras?**  
 R: En la sección [Issues](https://github.com/Xanderm0/LaJElegante/issues) del repositorio.

---

**¿Necesitas ayuda?** Contacta al SCRUM Master: Jeremy Duarte o abre un issue en GitHub.

---
