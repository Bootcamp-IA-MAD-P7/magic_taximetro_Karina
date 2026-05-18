# ✨ Magic Taxi Meter ✨

> Un taxímetro digital moderno, estético y seguro desarrollado en Python utilizando la librería **CustomTkinter**. Diseñado con una interfaz intuitiva con temática *Lavender Blush* para facilitar la gestión de viajes, tarifas en tiempo real y facturación automática.

---

## 📸 Capturas de Pantalla

Para ver la interfaz en acción, despliega las secciones a continuación:

<details>
<summary><b>🚕 Ver Interfaz Principal del Taxímetro (Dentro de la App)</b></summary>
<br>
<p align="center">
  <!-- Reemplaza la ruta de abajo cuando tengas tu captura, por ejemplo: docs/main.png -->
  <img <img width="295" height="450" alt="captura2" src="https://github.com/user-attachments/assets/4609f922-9129-493f-8a5b-1fadd21a621d" />
  <br>
  <i>Panel principal de control de tarifas, estados del vehículo y contador en tiempo real.</i>
</p>
</details>

---

## 🚀 Características Principales

*   **Seguridad por PIN:** Pantalla de acceso obligatorio que bloquea la aplicación si no se introduce la clave correcta (`1234`).
*   **Tarifas Dinámicas Automatizadas:** El sistema calcula el precio final segundo a segundo dependiendo de si el taxi está detenido o avanzando.
*   **Estructura Organizativa de Archivos:** Crea directorios automáticos para mantener el proyecto limpio:
    *   `invoices/`: Almacena las facturas detalladas en formato `.txt`.
    *   `logs/`: Guarda el registro de auditoría del sistema (`taxi_system.log`).
*   **Interfaz Ultra Moderna:** Diseñada con **CustomTkinter** con colores pasteles, bordes suavizados y fuentes legibles de alta calidad.

---

## 📊 Tabla de Tarifas

El coste se computa de manera automática cada **1 segundo** según el estado seleccionado mediante el botón *Change Gear*:

| Estado del Taxi | Tarifa Aplicada | Color de Estado en App |
| :--- | :--- | :--- |
| **🚗 En Movimiento (Moving)** | `€ 0.05 / seg` | Verde (`#51CF66`) |
| **🛑 Parado (Car Stopped)** | `€ 0.02 / seg` | Amarillo (`#FAB005`) |

---

## 🛠️ Instalación y Dependencias

Antes de arrancar la aplicación, asegúrate de clonar el proyecto e instalar los requisitos indispensables.

1. **Clonar el repositorio:**
2. **Instalar dependencias:**
Esta aplicación requiere la librería customtkinter. Puedes instalarla ejecutando:
```
pip install requirement.txt
```
---

## ⚡ Comando para Arrancar la Aplicación

Una vez completada la instalación, abre tu terminal en la ruta raíz del proyecto y ejecuta el comando correspondiente a tu sistema operativo:

### 🪟 En Windows
```bash
python base.py
```

## 📁 Estructura del Proyecto
Una vez que la aplicación comience a usarse, generará automáticamente carpetas para organizar los datos de la siguiente manera:
```
magic-taximetro/
├── base.py              # Código fuente principal de la app
├── README.md            # Documentación del proyecto
├── invoices/            # Carpeta autogenerada con las facturas individuales
│   ├── invoice_001.txt
│   └── invoice_002.txt
└── logs/                # Carpeta autogenerada para el control del sistema
    └── taxi_system.log  # Historial detallado de logins, resets y viajes
```
## 📝 Ejemplo de Factura Generada (.txt)
Al presionar el botón FINISH, la app exporta un informe limpio estructurado así:
```
--- MAGIC TAXI INVOICE #001 ---
Date: 2026-05-17 22:15
Total: €14.50
Stopped Fare: €2.10
Moving Fare: €12.40
--- Thank you! ---
```
## 🔒 Control de Logs (Auditoría)
El archivo logs/taxi_system.log registra marcas de tiempo e información sobre el comportamiento del usuario para evitar fraudes en el uso del taxímetro, por ejemplo:
```
[INFO] Inicio de sesión correcto.

[WARNING] Intento de acceso fallido con el PIN: 9999

[INFO] Viaje #1 iniciado.

[WARNING] Viaje #1 cancelado/reiniciado por el usuario.
```
