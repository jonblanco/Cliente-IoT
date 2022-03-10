## CLIENTE IOT PARA SUBIR EL %RAM Y %CPU A THINGSPEAK

Cliente IoT capaz de subir a [ThingSpeak](https://thingspeak.com/) 
el %CPU y %RAM del sistema que lo ejecuta.

Existen dos versiones, la general y una extendida llamada "LUZAPENA".

### Versión original:

	1. Al ejecutarla, lo primero que hará será crear dos canales en 
		ThingSpeak colocando las etiquetas %CPU y %RAM en cada uno
		de ellos.
	
	2. Después de crear el canal, subirá los datos de CPU y RAM del
		sistema cada 15 segundos utilizando la librería **psutil**.

	3. Finalmente presionando CTRL+C se detendrá la subida y se vacia-
		rá el contenido del canal creado.

### Versión extendida:

	1. A parte de hacer todo lo que hace la versión original, en
		caso de tener 4 canales creados, borrará el más antiguo
		y creará uno nuevo para su posterior utilización.