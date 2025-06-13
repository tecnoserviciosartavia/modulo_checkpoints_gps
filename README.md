# Módulo de Checkpoints de Seguridad con GPS

Este módulo permite gestionar puntos de control de seguridad utilizando códigos QR. Los oficiales de seguridad pueden registrar visitas al escanear un código QR en cada checkpoint, lo que incluye la ubicación GPS y la fecha y hora de la visita.

## Estructura del Proyecto

El proyecto está organizado en los siguientes archivos y directorios:

- **controllers/checkpoint_controller.py**: Maneja las rutas HTTP relacionadas con los checkpoints y registra visitas al escanear códigos QR.
- **data/qr_sequence.xml**: Define la secuencia para generar códigos QR únicos para los checkpoints.
- **models/__init__.py**: Importa los modelos `checkpoint` y `visita`.
- **models/checkpoint.py**: Define la clase `Checkpoint`, que representa un punto de control de seguridad con propiedades como nombre, descripción, ubicación, código QR, imagen QR y visitas asociadas.
- **models/visita.py**: Define la clase `VisitaSeguridad`, que representa un registro de visita con propiedades como oficial, checkpoint, fecha de visita y observaciones.
- **report/reporte_visita_excel.py**: Genera un reporte en formato Excel de las visitas registradas en un rango de fechas.
- **security/ir.model.access.csv**: Define los permisos de acceso a los modelos del módulo.
- **security/security.xml**: Define los grupos de seguridad y su categorización.
- **views/checkpoint_views.xml**: Define las vistas para los checkpoints, incluyendo formularios y listas.
- **views/visita_views.xml**: Define las vistas para las visitas, incluyendo formularios y listas.
- **wizard/reporte_visita_wizard.py**: Permite a los usuarios seleccionar un rango de fechas para generar un reporte de visitas.
- **__init__.py**: Inicializa el módulo importando controladores, modelos y wizard.
- **__manifest__.py**: Contiene la configuración del módulo, incluyendo su nombre, versión, dependencias y archivos de datos.

## Instalación

Para instalar el módulo, colóquelo en la carpeta de addons de Odoo y actualice la lista de módulos. Luego, instale el módulo desde la interfaz de Odoo.

## Uso

Los oficiales de seguridad pueden escanear códigos QR en los checkpoints para registrar sus visitas. El módulo también permite generar reportes de visitas en formato Excel, facilitando el seguimiento y la gestión de la seguridad.

## Contribuciones

Las contribuciones son bienvenidas. Si desea mejorar este módulo, por favor envíe un pull request o abra un issue en el repositorio.