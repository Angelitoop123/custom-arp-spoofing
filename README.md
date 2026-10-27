# ARP Spoofing - Interfaz gráfica en Python

## Descripción

Proyecto desarrollado en Python que ofrece una interfaz gráfica para consultar dispositivos detectables en una red local mediante solicitudes ARP. También incluye funciones de demostración para enviar mensajes ARP y restaurar las asociaciones ARP de un equipo de prueba.

> **Uso autorizado:** utiliza esta herramienta únicamente en una red propia o en un laboratorio donde tengas autorización explícita. Las funciones de envenenamiento ARP pueden interrumpir la conectividad de otros dispositivos. No la ejecutes contra redes o equipos ajenos.

## Funcionalidades

- **Ingreso de dirección de red:** permite introducir una red IPv4, por ejemplo `192.168.1.0/24`.
- **Escaneo de red:** envía solicitudes ARP para identificar los equipos que responden en la red indicada.
- **Tabla de resultados:** muestra la dirección IP y la dirección MAC de cada respuesta recibida.
- **Barra de desplazamiento vertical:** permite recorrer la tabla cuando hay muchos resultados.
- **Ingreso de IP objetivo:** permite especificar una dirección IPv4 para las operaciones de prueba.
- **Consulta de la puerta de enlace:** obtiene la puerta de enlace IPv4 predeterminada del sistema.
- **Resolución de direcciones MAC:** intenta obtener las direcciones MAC de la puerta de enlace y del equipo indicado.
- **Controles de inicio y detención:** la interfaz incluye botones para iniciar y detener el proceso de envío de mensajes ARP.
- **Restauración ARP:** al detener el proceso, intenta enviar respuestas ARP para restablecer las asociaciones entre la puerta de enlace y el equipo objetivo.

## Tecnologías y librerías

- **Python 3**
- **CustomTkinter:** componentes de interfaz gráfica.
- **Tkinter / ttk:** ventana, tabla y barra de desplazamiento; normalmente incluidos con Python.
- **Scapy:** construcción y envío de paquetes ARP.
- **Netifaces:** consulta de la configuración de red y la puerta de enlace.
- **Multiprocessing:** ejecución del proceso de red separado de la interfaz.
- **ipaddress y time:** validación de direcciones IPv4 y pausas entre operaciones.

## Requisitos

- Python 3 instalado.
- Dependencias de Python instaladas desde `requirements.txt`.
- Permisos de sistema suficientes para las operaciones de red que realice Scapy.
- Una interfaz de red activa y un entorno de laboratorio autorizado.

## Instalación

1. Descarga o clona el proyecto y abre una terminal en la carpeta donde está el archivo Python.
2. (Opcional, recomendado) crea un entorno virtual:

   ```bash
   python -m venv .venv
   ```

3. Activa el entorno virtual.

   **Windows (PowerShell):**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux / macOS:**

   ```bash
   source .venv/bin/activate
   ```

4. Instala las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Ejecución

Inicia el archivo principal del proyecto, sustituyendo `main.py` por el nombre real de tu archivo:

```bash
python main.py
```

En la interfaz:

1. Introduce la dirección de red IPv4 en formato CIDR, por ejemplo `192.168.1.0/24`.
2. Pulsa **Scan Network** para mostrar los dispositivos que respondan.
3. Revisa las direcciones IP y MAC en la tabla.
4. Usa los controles de las operaciones ARP únicamente dentro de un laboratorio autorizado y con equipos de prueba.

## Consideraciones

- El escaneo ARP funciona en la red local de capa 2; no descubre directamente equipos situados detrás de un router.
- Que un equipo no aparezca en la tabla no demuestra que esté desconectado: puede no responder a las solicitudes ARP.
- La restauración ARP intenta corregir las asociaciones, pero no garantiza que todos los dispositivos actualicen su caché inmediatamente.
- Ejecuta las operaciones de red con los permisos adecuados para tu sistema operativo.
- Para una versión más robusta, conviene gestionar los errores de red y los procesos en segundo plano sin bloquear la interfaz gráfica.

## Estructura sugerida

```text
proyecto/
├── main.py
├── README.md
└── requirements.txt
```

`main.py` representa el nombre de ejemplo; conserva el nombre real de tu archivo Python.
