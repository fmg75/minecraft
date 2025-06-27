import streamlit as st
import numpy as np
from PIL import Image
import io
import json
import zipfile
from sklearn.cluster import KMeans

# Paleta completa de bloques de Minecraft con colores RGB precisos
MINECRAFT_BLOCKS = {
    # Bloques básicos de construcción
    (128, 128, 128): "minecraft:stone",
    (139, 90, 43): "minecraft:cobblestone",
    (105, 105, 105): "minecraft:deepslate",
    (64, 64, 64): "minecraft:blackstone",
    (50, 50, 50): "minecraft:obsidian",
    (255, 255, 255): "minecraft:white_concrete",
    (192, 192, 192): "minecraft:light_gray_concrete",
    (128, 128, 128): "minecraft:gray_concrete",
    (64, 64, 64): "minecraft:black_concrete",
    
    # Bloques de madera
    (160, 82, 45): "minecraft:oak_planks",
    (139, 90, 43): "minecraft:spruce_planks",
    (205, 133, 63): "minecraft:birch_planks",
    (115, 85, 45): "minecraft:dark_oak_planks",
    (218, 165, 32): "minecraft:acacia_planks",
    (144, 108, 63): "minecraft:jungle_planks",
    (184, 115, 51): "minecraft:mangrove_planks",
    (139, 69, 19): "minecraft:cherry_planks",
    
    # Lana - Colores básicos
    (255, 255, 255): "minecraft:white_wool",
    (220, 220, 220): "minecraft:light_gray_wool",
    (128, 128, 128): "minecraft:gray_wool",
    (64, 64, 64): "minecraft:black_wool",
    (139, 69, 19): "minecraft:brown_wool",
    
    # Lana - Colores vibrantes
    (220, 20, 60): "minecraft:red_wool",
    (255, 165, 0): "minecraft:orange_wool",
    (255, 255, 0): "minecraft:yellow_wool",
    (50, 205, 50): "minecraft:lime_wool",
    (0, 128, 0): "minecraft:green_wool",
    (0, 255, 255): "minecraft:cyan_wool",
    (135, 206, 235): "minecraft:light_blue_wool",
    (25, 25, 112): "minecraft:blue_wool",
    (128, 0, 128): "minecraft:purple_wool",
    (255, 20, 147): "minecraft:magenta_wool",
    (255, 192, 203): "minecraft:pink_wool",
    
    # Concreto - Colores más saturados
    (209, 178, 161): "minecraft:white_concrete",
    (169, 48, 159): "minecraft:magenta_concrete",
    (176, 46, 38): "minecraft:red_concrete",
    (249, 128, 29): "minecraft:orange_concrete",
    (254, 216, 61): "minecraft:yellow_concrete",
    (128, 199, 31): "minecraft:lime_concrete",
    (94, 124, 22): "minecraft:green_concrete",
    (22, 156, 156): "minecraft:cyan_concrete",
    (58, 175, 217): "minecraft:light_blue_concrete",
    (35, 137, 198): "minecraft:blue_concrete",
    (100, 32, 156): "minecraft:purple_concrete",
    (243, 139, 170): "minecraft:pink_concrete",
    (162, 78, 78): "minecraft:brown_concrete",
    (142, 142, 134): "minecraft:light_gray_concrete",
    (71, 79, 82): "minecraft:gray_concrete",
    (25, 22, 22): "minecraft:black_concrete",
    
    # Bloques metálicos y minerales
    (255, 215, 0): "minecraft:gold_block",
    (192, 192, 192): "minecraft:iron_block",
    (255, 140, 0): "minecraft:copper_block",
    (139, 69, 19): "minecraft:oxidized_copper",
    (46, 125, 50): "minecraft:emerald_block",
    (31, 58, 147): "minecraft:lapis_block",
    (106, 13, 173): "minecraft:amethyst_block",
    (255, 0, 0): "minecraft:redstone_block",
    (85, 255, 85): "minecraft:lime_concrete_powder",
    
    # Bloques de terracota
    (152, 89, 36): "minecraft:terracotta",
    (161, 83, 37): "minecraft:orange_terracotta",
    (142, 60, 46): "minecraft:red_terracotta",
    (107, 53, 51): "minecraft:brown_terracotta",
    (76, 62, 92): "minecraft:purple_terracotta",
    (76, 83, 42): "minecraft:green_terracotta",
    (86, 91, 91): "minecraft:gray_terracotta",
    (209, 177, 161): "minecraft:white_terracotta",
    (135, 107, 98): "minecraft:light_gray_terracotta",
    (37, 22, 16): "minecraft:black_terracotta",
    
    # Bloques naturales
    (34, 139, 34): "minecraft:grass_block",
    (139, 69, 19): "minecraft:dirt",
    (255, 228, 181): "minecraft:sand",
    (194, 178, 128): "minecraft:sandstone",
    (255, 140, 0): "minecraft:pumpkin",
    (34, 139, 34): "minecraft:melon",
    (85, 107, 47): "minecraft:moss_block",
    (107, 142, 35): "minecraft:slime_block",
    (85, 107, 47): "minecraft:oak_leaves",
    (50, 50, 50): "minecraft:coal_block",
}

def calculate_delta_e(color1, color2):
    """Calcula la diferencia perceptual entre dos colores usando Delta E CIE76"""
    def rgb_to_lab(rgb):
        # Normalizar RGB
        r, g, b = [x/255.0 for x in rgb]
        
        # Convertir a XYZ
        def f(t):
            return t**(1/3) if t > 0.008856 else (7.787 * t) + (16/116)
        
        # Conversión simplificada RGB -> LAB
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        
        fx = f(x / 0.95047)
        fy = f(y / 1.00000)
        fz = f(z / 1.08883)
        
        l = (116 * fy) - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)
        
        return (l, a, b)
    
    lab1 = rgb_to_lab(color1)
    lab2 = rgb_to_lab(color2)
    
    delta_l = lab1[0] - lab2[0]
    delta_a = lab1[1] - lab2[1]
    delta_b = lab1[2] - lab2[2]
    
    return (delta_l**2 + delta_a**2 + delta_b**2)**0.5

def find_closest_minecraft_block(color):
    """Encuentra el bloque de Minecraft más cercano usando Delta E"""
    min_distance = float('inf')
    closest_block = "minecraft:stone"
    
    for mc_color, block in MINECRAFT_BLOCKS.items():
        distance = calculate_delta_e(color, mc_color)
        if distance < min_distance:
            min_distance = distance
            closest_block = block
    
    return closest_block

def create_adaptive_palette(image, max_colors=32):
    """Crea una paleta adaptativa basada en los colores dominantes de la imagen"""
    # Redimensionar para análisis más rápido
    analysis_img = image.resize((100, 100))
    pixels = np.array(analysis_img).reshape(-1, 3)
    
    # Usar K-means para encontrar colores dominantes
    n_colors = min(max_colors, len(np.unique(pixels.view(np.dtype((np.void, pixels.dtype.itemsize*pixels.shape[1]))))))
    
    if n_colors < 2:
        return [(128, 128, 128)]
    
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    dominant_colors = kmeans.cluster_centers_.astype(int)
    
    # Mapear cada color dominante al bloque más cercano
    minecraft_palette = []
    used_blocks = set()
    
    for color in dominant_colors:
        closest_block = find_closest_minecraft_block(tuple(color))
        
        if closest_block not in used_blocks:
            # Obtener el color RGB del bloque
            for rgb, block in MINECRAFT_BLOCKS.items():
                if block == closest_block:
                    minecraft_palette.append(rgb)
                    used_blocks.add(closest_block)
                    break
    
    # Asegurar que tenemos suficientes colores básicos
    essential_colors = [
        (255, 255, 255), (128, 128, 128), (64, 64, 64),  # Grises
        (220, 20, 60), (0, 128, 0), (25, 25, 112),       # RGB básicos
        (139, 69, 19), (255, 215, 0)                     # Tierra y oro
    ]
    
    for color in essential_colors:
        if len(minecraft_palette) >= max_colors:
            break
        if color not in minecraft_palette:
            minecraft_palette.append(color)
    
    return minecraft_palette

def quantize_to_palette(image, palette):
    """Cuantiza la imagen a la paleta de colores especificada"""
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    
    quantized = np.zeros_like(img_array)
    
    for y in range(height):
        for x in range(width):
            original_color = tuple(img_array[y, x])
            
            # Encontrar el color más cercano en la paleta
            min_distance = float('inf')
            closest_color = palette[0]
            
            for palette_color in palette:
                distance = calculate_delta_e(original_color, palette_color)
                if distance < min_distance:
                    min_distance = distance
                    closest_color = palette_color
            
            quantized[y, x] = closest_color
    
    return Image.fromarray(quantized)

def apply_floyd_steinberg(image, palette):
    """Aplica dithering Floyd-Steinberg para mejor gradación"""
    img_array = np.array(image, dtype=np.float32)
    height, width = img_array.shape[:2]
    
    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x]
            
            # Encontrar color más cercano
            min_distance = float('inf')
            new_pixel = palette[0]
            
            for palette_color in palette:
                distance = calculate_delta_e(tuple(old_pixel.astype(int)), palette_color)
                if distance < min_distance:
                    min_distance = distance
                    new_pixel = palette_color
            
            img_array[y, x] = new_pixel
            
            # Calcular y propagar error
            error = old_pixel - np.array(new_pixel)
            
            # Distribución Floyd-Steinberg
            if x + 1 < width:
                img_array[y, x + 1] += error * 7/16
            if y + 1 < height:
                if x > 0:
                    img_array[y + 1, x - 1] += error * 3/16
                img_array[y + 1, x] += error * 5/16
                if x + 1 < width:
                    img_array[y + 1, x + 1] += error * 1/16
    
    return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

def generate_minecraft_datapack(image, scale_factor=4, use_dithering=True):
    """Genera un datapack completo para Minecraft"""
    
    # Calcular nuevo tamaño
    original_width, original_height = image.size
    new_width = max(1, original_width // scale_factor)
    new_height = max(1, original_height // scale_factor)
    
    # Redimensionar imagen
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Crear paleta adaptativa
    palette = create_adaptive_palette(resized_image)
    
    # Aplicar cuantización y dithering
    if use_dithering:
        processed_image = apply_floyd_steinberg(resized_image, palette)
    else:
        processed_image = quantize_to_palette(resized_image, palette)
    
    # Generar comandos
    img_array = np.array(processed_image)
    commands = []
    
    # Header
    commands.append("# Minecraft Image to Blocks Generator")
    commands.append(f"# Original size: {original_width}x{original_height}")
    commands.append(f"# Minecraft size: {new_width}x{new_height}")
    commands.append(f"# Scale factor: {scale_factor}")
    commands.append(f"# Colors in palette: {len(palette)}")
    commands.append("")
    
    # Limpiar área
    commands.append("# Limpiar área")
    commands.append(f"fill ~-1 ~-1 ~-1 ~{new_width} ~{new_height} ~1 minecraft:air")
    commands.append("")
    
    # Colocar bloques
    commands.append("# Colocar imagen")
    for y in range(new_height):
        for x in range(new_width):
            pixel_color = tuple(img_array[y, x])
            block = find_closest_minecraft_block(pixel_color)
            
            # Coordenadas: x horizontal, y vertical (invertida), z profundidad
            commands.append(f"setblock ~{x} ~{new_height - 1 - y} ~0 {block}")
    
    # Crear datapack
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # pack.mcmeta
        pack_mcmeta = {
            "pack": {
                "pack_format": 48,
                "description": f"Image to Blocks: {new_width}x{new_height}"
            }
        }
        zip_file.writestr("pack.mcmeta", json.dumps(pack_mcmeta, indent=2))
        
        # Función principal
        zip_file.writestr(
            "data/imageblocks/function/build.mcfunction", 
            "\n".join(commands)
        )
        
        # Función de limpieza
        clear_commands = [
            "# Limpiar imagen",
            f"fill ~-2 ~-2 ~-2 ~{new_width+1} ~{new_height+1} ~2 minecraft:air",
            'tellraw @a {"text":"Área limpiada","color":"green"}'
        ]
        zip_file.writestr(
            "data/imageblocks/function/clear.mcfunction", 
            "\n".join(clear_commands)
        )
        
        # Función de carga
        load_commands = [
            "# Image to Blocks Generator",
            'tellraw @a {"text":"Image to Blocks cargado! Usa /function imageblocks:build","color":"yellow"}',
            'tellraw @a {"text":"Para limpiar: /function imageblocks:clear","color":"gray"}'
        ]
        zip_file.writestr(
            "data/imageblocks/function/load.mcfunction", 
            "\n".join(load_commands)
        )
        
        # Tag de carga
        zip_file.writestr(
            "data/minecraft/tags/function/load.json",
            json.dumps({"values": ["imageblocks:load"]}, indent=2)
        )
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue(), processed_image, palette

def show_palette_preview(palette):
    """Muestra una preview de la paleta de colores"""
    if not palette:
        return
    
    # Crear imagen con muestras de colores
    sample_width = 40
    sample_height = 40
    cols = min(8, len(palette))
    rows = (len(palette) + cols - 1) // cols
    
    palette_img = Image.new('RGB', (cols * sample_width, rows * sample_height))
    
    for i, color in enumerate(palette):
        row = i // cols
        col = i % cols
        
        # Crear muestra de color
        sample = Image.new('RGB', (sample_width, sample_height), color)
        palette_img.paste(sample, (col * sample_width, row * sample_height))
    
    return palette_img

# Configuración de Streamlit
st.set_page_config(
    page_title="Minecraft Image to Blocks",
    page_icon="🧱",
    layout="wide"
)

st.title("🧱 Minecraft Image to Blocks Generator")
st.markdown("Convierte imágenes a pixel art de Minecraft con colores precisos")

# Sidebar
st.sidebar.header("⚙️ Configuración")

uploaded_file = st.sidebar.file_uploader(
    "Sube tu imagen",
    type=['png', 'jpg', 'jpeg', 'bmp', 'gif'],
    help="Formatos soportados: PNG, JPG, JPEG, BMP, GIF"
)

if uploaded_file is not None:
    scale_factor = st.sidebar.slider(
        "Factor de escala",
        min_value=2,
        max_value=16,
        value=4,
        help="Mayor valor = imagen más pequeña en Minecraft"
    )
    
    use_dithering = st.sidebar.checkbox(
        "Usar dithering (Floyd-Steinberg)",
        value=True,
        help="Mejora los gradientes de color"
    )
    
    # Procesar imagen
    try:
        image = Image.open(uploaded_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Layout principal
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📸 Imagen Original")
            st.image(image, caption=f"Tamaño: {image.size[0]}x{image.size[1]}")
        
        with col2:
            st.subheader("🧱 Preview Minecraft")
            
            # Generar preview
            with st.spinner("Generando preview..."):
                datapack_data, processed_image, palette = generate_minecraft_datapack(
                    image, scale_factor, use_dithering
                )
            
            st.image(
                processed_image, 
                caption=f"Minecraft: {processed_image.size[0]}x{processed_image.size[1]} bloques"
            )
        
        # Mostrar paleta de colores
        st.subheader("🎨 Paleta de Colores")
        palette_preview = show_palette_preview(palette)
        if palette_preview:
            st.image(palette_preview, caption=f"Paleta generada: {len(palette)} colores")
        
        # Información y descarga
        col3, col4 = st.columns([1, 1])
        
        with col3:
            st.subheader("📊 Información")
            st.info(f"""
            **Tamaño original:** {image.size[0]} x {image.size[1]} píxeles
            **Tamaño Minecraft:** {processed_image.size[0]} x {processed_image.size[1]} bloques
            **Factor de escala:** {scale_factor}x
            **Colores en paleta:** {len(palette)}
            **Total de bloques:** {processed_image.size[0] * processed_image.size[1]}
            **Dithering:** {'Activado' if use_dithering else 'Desactivado'}
            """)
        
        with col4:
            st.subheader("📥 Descargar Datapack")
            
            filename = f"minecraft_image_{processed_image.size[0]}x{processed_image.size[1]}.zip"
            
            st.download_button(
                label="🎮 Descargar Datapack",
                data=datapack_data,
                file_name=filename,
                mime="application/zip",
                help="Datapack listo para usar en Minecraft"
            )
            
            st.success("✅ Datapack generado exitosamente!")
        
        # Instrucciones
        st.subheader("📋 Instrucciones de Uso")
        st.markdown("""
        1. **Descargar** el datapack (.zip)
        2. **Colocar** en la carpeta `datapacks` de tu mundo
        3. **Ejecutar** `/reload` en el juego
        4. **Posicionarte** donde quieres construir la imagen
        5. **Ejecutar** `/function imageblocks:build`
        
        **Comandos adicionales:**
        - `/function imageblocks:clear` - Limpia la construcción
        - La imagen se construye hacia arriba y a la derecha desde tu posición
        """)
        
    except Exception as e:
        st.error(f"Error al procesar la imagen: {str(e)}")
        st.exception(e)

else:
    st.info("👆 Sube una imagen para comenzar")
    
    # Información adicional
    st.markdown("---")
    st.subheader("✨ Características")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Mapeo de colores preciso:**
        - Algoritmo Delta E para comparación de colores
        - Paleta adaptativa basada en la imagen
        - 60+ bloques de Minecraft disponibles
        """)
    
    with col2:
        st.markdown("""
        **⚡ Funciones avanzadas:**
        - Dithering Floyd-Steinberg opcional
        - Escalado inteligente
        - Datapack completo y funcional
        """)
    
    st.markdown("---")
    st.markdown("💡 **Tip:** Para mejores resultados, usa imágenes con colores claros y bien definidos.")