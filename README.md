# 🧱 Minecraft Image to Blocks Generator

Convierte cualquier imagen a pixel art de Minecraft con colores precisos y algoritmos avanzados de mapeo de color.

![Minecraft Blocks](https://img.shields.io/badge/Minecraft-Blocks-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

## ✨ Características

- **🎯 Mapeo de colores preciso**: Usa algoritmo Delta E CIE76 para comparación perceptual de colores
- **🎨 Paleta adaptativa**: Genera automáticamente una paleta de bloques basada en tu imagen
- **⚡ Dithering Floyd-Steinberg**: Mejora los gradientes y transiciones de color
- **📦 Datapack completo**: Genera archivos listos para usar en Minecraft
- **🔧 60+ bloques disponibles**: Amplia gama de bloques de construcción, lana, concreto y más

## 🚀 Instalación Rápida

### Opción 1: Clonar repositorio
```bash
git clone https://github.com/tu-usuario/minecraft-image-blocks.git
cd minecraft-image-blocks
pip install -r requirements.txt
streamlit run minecraft_datapack_generator.py
```

### Opción 2: Instalación directa
```bash
pip install streamlit numpy pillow scikit-learn
# Descargar minecraft_datapack_generator.py
streamlit run minecraft_datapack_generator.py
```

## 📋 Requisitos

- Python 3.8 o superior
- Las dependencias listadas en `requirements.txt`

## 🎮 Cómo usar

### 1. Generar el datapack
1. Ejecuta la aplicación con `streamlit run minecraft_datapack_generator.py`
2. Sube tu imagen (PNG, JPG, JPEG, BMP, GIF)
3. Ajusta el **factor de escala** (2-16x):
   - `2x`: Máximo detalle, más bloques
   - `8x`: Balance entre detalle y tamaño
   - `16x`: Imagen pequeña, menos bloques
4. Activa/desactiva **dithering** según tu preferencia:
   - ✅ **ON**: Mejor para fotos y imágenes complejas
   - ❌ **OFF**: Mejor para logos y arte simple
5. Descarga el archivo `.zip`

### 2. Instalar en Minecraft
1. Copia el archivo `.zip` a la carpeta `datapacks` de tu mundo:
   ```
   .minecraft/saves/[NombreDeTuMundo]/datapacks/
   ```
2. En el juego, ejecuta: `/reload`
3. Verifica que se cargó: debería aparecer un mensaje verde

### 3. Construir la imagen
1. Ve al lugar donde quieres construir la imagen
2. Ejecuta: `/function imageblocks:build`
3. La imagen se construirá hacia arriba y a la derecha desde tu posición

### 4. Comandos adicionales
- `/function imageblocks:clear` - Limpia la construcción
- `/reload` - Recarga todos los datapacks

## 🔧 Configuración Avanzada

### Factor de Escala
- **2x-4x**: Para imágenes detalladas (máximo 100x100 bloques recomendado)
- **6x-8x**: Balance ideal para la mayoría de casos
- **10x-16x**: Para imágenes grandes o vista desde lejos

### Dithering
- **Activado**: Mejor gradaciones, más realista
- **Desactivado**: Colores más sólidos, estilo pixelado clásico

## 🎨 Bloques Soportados

El generador incluye más de 60 bloques diferentes:

### Construcción Básica
- Piedra, Adoquín, Pizarra profunda
- Obsidiana, Cuarzo
- Concreto (16 colores)

### Decorativos
- Lana (16 colores)
- Terracota (10 colores)
- Madera (8 tipos)

### Metálicos y Minerales
- Oro, Hierro, Cobre
- Esmeralda, Lapislázuli
- Amatista, Redstone

### Naturales
- Césped, Tierra, Arena
- Calabaza, Sandía
- Musgo, Slime

## 📊 Rendimiento

| Tamaño Imagen | Factor Escala | Bloques Minecraft | Tiempo Construcción |
|---------------|---------------|-------------------|-------------------|
| 200x200 px    | 4x           | 50x50 (2,500)    | ~3 minutos       |
| 400x300 px    | 8x           | 50x38 (1,900)    | ~2 minutos       |
| 800x600 px    | 16x          | 50x38 (1,900)    | ~2 minutos       |

## 🛠️ Desarrollo

### Estructura del proyecto
```
minecraft-image-blocks/
├── minecraft_datapack_generator.py  # Aplicación principal
├── requirements.txt                 # Dependencias
├── README.md                       # Este archivo
└── examples/                       # Imágenes de ejemplo
```

### Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature: `git checkout -b nueva-caracteristica`
3. Commit tus cambios: `git commit -am 'Añadir nueva característica'`
4. Push a la rama: `git push origin nueva-caracteristica` 
5. Crea un Pull Request

## 🐛 Solución de Problemas

### Error: "No se puede cargar la imagen"
- Verifica que el formato sea PNG, JPG, JPEG, BMP o GIF
- Asegúrate de que el archivo no esté corrupto

### Error: "Datapack no se carga en Minecraft"
- Verifica que esté en la carpeta correcta: `saves/[mundo]/datapacks/`
- Ejecuta `/reload` después de añadir el datapack
- Verifica que sea una versión compatible de Minecraft (1.19+)

### La imagen se ve muy pixelada
- Reduce el factor de escala (usar 2x o 4x)
- Activa el dithering para mejores gradientes

### La construcción es muy lenta
- Usa un factor de escala mayor (8x o 16x)
- Considera usar imágenes más pequeñas

## 📝 Changelog

### v2.0.0
- ✨ Nuevo algoritmo Delta E para mapeo de colores
- 🎨 Paleta adaptativa automática
- ⚡ Dithering Floyd-Steinberg
- 🧹 Código completamente reescrito y optimizado
- 📦 Solo genera datapacks (formato más útil)

### v1.0.0
- 🎉 Lanzamiento inicial
- 🔧 Generación de archivos .mcfunction y .nbt

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- Algoritmo Delta E basado en estándares CIE
- Inspirado en herramientas de pixel art clásicas
- Comunidad de Minecraft por feedback y testing

---

**¿Problemas o sugerencias?** Abre un [issue](https://github.com/tu-usuario/minecraft-image-blocks/issues) o contribuye al proyecto.

**¿Te gustó el proyecto?** Dale una ⭐ en GitHub!