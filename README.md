# Urban Routes Automation

## Descripción
Es un conjunto de pruebas automatizadas para verificar el funcionamiento de una aplicación de reserva de taxis, asegurando todas las funciones críticas, como establecer una ruta, seleccionar tarifas, agregar métodos de pago y solicitar servicios adicionales, operen correctamente.

## Tecnologías y Técnicas Utilizadas
- **Python**: Lenguaje principal para la escritura de pruebas.
- **Selenium**: Herramienta para la automatización de navegadores web.
- **ChromeDriver**: Controlador para ejecutar las pruebas en el navegador Google Chrome.
- **Page Object Model (POM)**: Patrón de diseño para mantener un código de pruebas organizado y reutilizable.

## Instrucciones para Ejecutar las Pruebas
1. **Instalar Dependencias**:
   - Python 3.8 o superior.
   - Selenium: `pip install selenium`.
   - Descarga el último [ChromeDriver](https://chromedriver.chromium.org/) compatible con tu versión de Chrome.

2. **Estructura del Proyecto**:
   - `data.py`: Contiene datos estáticos para las pruebas.
   - `main.py`: Contiene las clases `UrbanRoutesPage` y `TestUrbanRoutes` con las pruebas.

3. **Ejecución de las Pruebas**:
   - Navega al directorio del proyecto.
   - Ejecuta las pruebas con `pytest main.py`.

4. **Logs de Ejecución**:
   - Los logs de ejecución se generan automáticamente. Asegúrate de habilitar los permisos necesarios para las pruebas basadas en red.
