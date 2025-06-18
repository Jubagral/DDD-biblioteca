import os
import json
import re
import copy
import logging
import time
import hashlib
import argparse
from tqdm import tqdm
from colorama import init, Fore, Style

# Inicializar colorama para colores en la consola
init(autoreset=True)

# Configuración de carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
TEMPLATE_DIR = os.path.join(BASE_DIR, "template")
OUTPUT_DIR = os.path.join(BASE_DIR, "outh")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
TEMPLATE_MAP_FILE = os.path.join(CONFIG_DIR, "template_map.json")
TYPE_TO_FOLDER_FILE = os.path.join(CONFIG_DIR, "type_to_folder.json")
REQUIRED_FIELDS_FILE = os.path.join(CONFIG_DIR, "required_fields.json")
COVER_SETTINGS_FILE = os.path.join(CONFIG_DIR, "cover_settings.json")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")

# Configuración de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
    ]
)

def confirm_overwrite(file_path, batch_mode=None):
    """Pregunta al usuario si desea sobreescribir un archivo existente, salvo en modo batch."""
    if batch_mode == "overwrite":
        logging.info(f"Sobreescribiendo automáticamente {file_path} en modo batch")
        return True
    if os.path.exists(file_path):
        while True:
            respuesta = input(f"¿Sobreescribir {file_path}? (s/n): ").strip().lower()
            if respuesta in ['s', 'n']:
                return respuesta == 's'
            logging.warning(f"Respuesta inválida para {file_path}. Usa 's' o 'n'.")
    return True

def write_file(file_path, content, batch_mode=None):
    """Escribe un archivo solo si se permite la sobreescritura."""
    if confirm_overwrite(file_path, batch_mode):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Archivo escrito: {file_path}")
    else:
        logging.info(f"Archivo omitido: {file_path}")

def write_json_file(file_path, data, batch_mode=None):
    """Escribe un archivo JSON solo si se permite la sobreescritura."""
    if confirm_overwrite(file_path, batch_mode):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=True, indent=2)
        logging.info(f"Archivo JSON escrito: {file_path}")
    else:
        logging.info(f"Archivo JSON omitido: {file_path}")

def format_array(arr):
    return ", ".join(arr) if arr else "-"

def capitalize(text):
    return str.capitalize(str(text)) if text else ""

def escape(text):
    return str(text).replace('#', r'\#') if text else ""

def get_nested_value(d, key, default='-'):
    """Obtiene un valor anidado de un diccionario usando claves separadas por puntos."""
    keys = key.split('.')
    current = d
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    return current if current is not None else default

def flatten_dict(d, parent_key='', sep='.'):
    """Aplana un diccionario anidado para usar en str.format."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        elif isinstance(v, list):
            # Convertir listas de valores complejos a cadenas JSON para evitar errores
            converted = []
            for elem in v:
                if isinstance(elem, (str, int, float, bool)):
                    converted.append(str(elem))
                else:
                    converted.append(json.dumps(elem, ensure_ascii=False))
            items.append((new_key, format_array(converted)))
        else:
            items.append((new_key, v if v is not None else '-'))
    return dict(items)

def hash_dict(d):
    """Calcula un hash MD5 de un diccionario para comparación de contenido."""
    return hashlib.md5(json.dumps(d, sort_keys=True).encode()).hexdigest()

def load_config(file_path, default):
    """Carga un archivo de configuración JSON o retorna un valor por defecto si falla."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Archivo {file_path} no encontrado.")
        return default
    except json.JSONDecodeError:
        logging.error(f"No se pudo parsear {file_path}.")
        return default

def load_template_map():
    """Carga el mapeo de plantillas desde template_map.json."""
    return load_config(TEMPLATE_MAP_FILE, {})

def load_type_to_folder():
    """Carga el mapeo de tipos a carpetas desde type_to_folder.json."""
    default = {
        "item": "items",
        "monster": "monsters",
        "pnj": "pnj",
        "pj": "pj",
        "spell": "spells",
        "trap": "traps",
        "encounter": "encounters",
        "event": "events",
        "plane": "planes",
        "scene": "scenes",
        "environment": "environments",
        "class": "classes",
        "location": "locations",
        "adventure": "adventures",
        "hook": "hooks",
        "objective": "objectives",
        "familiar": "familiars",
        "mount": "mounts",
        "item_pack": "item_packs"
    }
    return load_config(TYPE_TO_FOLDER_FILE, default)

def load_required_fields():
    """Carga los campos obligatorios por tipo desde required_fields.json."""
    default = {
        "item": ["type", "subtype", "id", "name", "rarity", "description", "mechanics.cost"],
        "monster": [],  # Validación manejada por template/monster/monster.json
        "pnj": ["type", "id", "name", "description", "alignment"],
        "pj": ["type", "id", "name", "description", "class", "level"],
        "spell": ["type", "id", "name", "level", "school", "description"]
    }
    return load_config(REQUIRED_FIELDS_FILE, default)

def load_cover_settings():
    """Carga la configuración de portada y contraportada desde cover_settings.json."""
    default = {
        "cover": {
            "template": "# {title}\n<div class='phb#first-page'>\n## {subtitle}\n**Módulo para {juego}**\n*Autor*: {author}\n*Entorno*: {entorno_de_campanya}\n*Tipo*: {modul_tipe}\n</div>\n",
            "defaults": {
                "title": "{modul_tipe} de {entorno_de_campanya}",
                "subtitle": "Un módulo épico para D&D 5e 2025",
                "author": "Anónimo",
                "juego": "D&D 5e 2025"
            }
        },
        "back_cover": {
            "template": "<div class='phb#page-cover'>\n# Contraportada\n**{title}**\n*Descripción*: {description}\n*Créditos*: {credits}\n</div>\n",
            "defaults": {
                "title": "{modul_tipe} de {entorno_de_campanya}",
                "description": "Un módulo diseñado para aventuras inolvidables.",
                "credits": "Creado con el Generador de Contenido D&D 5e"
            }
        }
    }
    return load_config(COVER_SETTINGS_FILE, default)

def list_templates():
    templates = []
    for root, _, files in os.walk(TEMPLATE_DIR):
        for f in files:
            if f.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, f), TEMPLATE_DIR)
                templates.append(rel_path.replace(os.sep, '/'))
    if not templates:
        logging.error("No hay plantillas en la carpeta template ni en sus subcarpetas.")
        return []
    logging.debug(f"Plantillas encontradas: {', '.join(templates)}")
    return templates 
    
def select_template(templates):
    """Permite seleccionar una plantilla por número (usado si falta mapeo)."""
    logging.info("Plantillas disponibles:")
    for idx, fname in enumerate(templates, 1):
        logging.info(f"{idx}. {fname}")
    while True:
        seleccion = input("Selecciona la plantilla por número (deja vacío para omitir): ").strip()
        if not seleccion:
            return None
        if seleccion.isdigit() and 0 < int(seleccion) <= len(templates):
            return templates[int(seleccion) - 1]
        logging.warning("Selección de plantilla inválida.")

def render_template(template_content, data):
    """Renderiza una plantilla con los datos proporcionados usando str.format."""
    try:
        flat_data = flatten_dict(data)
        flat_data.update({
            'format_array': format_array,
            'capitalize': capitalize,
            'escape': escape
        })

        def format_with_defaults(match):
            key = match.group(1)
            return str(flat_data.get(key, '-'))

        output = re.sub(r'\{([^}]+)\}', format_with_defaults, template_content)
        return output
    except Exception as e:
        logging.error(f"Error al renderizar plantilla: {e}")
        return ""

def render_entity(entity, template_name):
    """Renderiza una entidad con la plantilla correspondiente."""
    try:
        template_path = os.path.join(TEMPLATE_DIR, template_name)
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        return render_template(template_content, entity)
    except Exception as e:
        logging.error(f"Error al renderizar {entity.get('id', 'unknown')} con {template_name}: {e}")
        raise

def get_template_name(entity, templates, template_map):
    """Obtiene el nombre de la plantilla según tipo, subtipo y mapeo."""
    tipo = entity.get("type")
    subtipo = entity.get("subtype")
    if tipo in template_map:
        if isinstance(template_map[tipo], dict):
            template = template_map[tipo].get(subtipo, template_map[tipo].get("default"))
        else:
            template = template_map[tipo]
        if template and os.path.exists(os.path.join(TEMPLATE_DIR, template)):
            return template
    logging.error(f"No se encontró plantilla para tipo {tipo}/{subtipo}.")
    return select_template(templates) or None

def get_cover_template(modul_tipe, template_map, template_type, templates):
    """Obtiene la plantilla de portada o contraportada según el tipo de módulo."""
    covers = template_map.get("covers", {})
    if modul_tipe in covers and template_type in covers[modul_tipe]:
        template = covers[modul_tipe][template_type]
        if os.path.exists(os.path.join(TEMPLATE_DIR, template)):
            return template
    return None

def validate_entity(entity, entity_type, required_fields):
    """Valida los campos obligatorios de una entidad."""
    errors = []
    for field in required_fields.get(entity_type, []):
        keys = field.split(".")
        current = entity
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                errors.append(f"Campo obligatorio faltante: {field}")
                break
    if errors:
        logging.error(f"Errores en la entidad {entity.get('id', 'unknown')}: {'; '.join(errors)}")
    return errors

def load_entities(json_files, template_map):
    """Carga todas las entidades de los JSON, filtrando por plantillas."""
    entities = []
    for json_file in json_files:
        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or "entidades" not in data:
                logging.error(f"Formato inválido en {json_file}: falta 'entidades'")
                continue
            metadata = {
                "juego": data.get("juego", "Unknown"),
                "entorno_de_campanya": data.get("entorno_de_campanya", "Unknown"),
                "modul_tipe": data.get("modul_tipe", "Unknown"),
                "cover": data.get("cover", {})
            }
            for entity_type, entity_list in data["entidades"].items():
                for item in entity_list:
                    if isinstance(item, dict):
                        # Agregar el campo "type" basado en el nombre del array
                        item_with_type = item.copy()

                        # Mapear nombres de arrays a tipos de plantilla
                        type_mapping = {
                            "monsters": "monster",
                            "items": "item", 
                            "spells": "spell",
                            "characters": "pj",  # Asumo que characters son PJs
                            "pnjs": "pnj",
                            "pjs": "pj",
                            "traps": "trap",
                            "encounters": "encounter",
                            "events": "event",
                            "planes": "plane",
                            "scenes": "scene",
                            "environments": "environment",
                            "classes": "class",
                            "locations": "location",
                            "adventures": "adventure",
                            "hooks": "hook",
                            "objectives": "objective",
                            "familiars": "familiar",
                            "mounts": "mount",
                            "item_packs": "item_pack"
                        }

                        # Usar el mapeo o el nombre del array directamente
                        entity_type_mapped = type_mapping.get(entity_type, entity_type)
                        item_with_type["type"] = entity_type_mapped

                        # Verificar si existe plantilla para este tipo (considerando subtipos)
                        has_template = False
                        if entity_type_mapped in template_map:
                            template_config = template_map[entity_type_mapped]
                            if isinstance(template_config, dict):
                                # Tiene subtipos, verificar si tiene default o el subtipo específico
                                subtipo = item_with_type.get("subtype")
                                if subtipo and subtipo in template_config:
                                    has_template = True
                                elif "default" in template_config:
                                    has_template = True
                            else:
                                # Es una plantilla simple (string)
                                has_template = True

                        if has_template:
                            entities.append((json_file, item_with_type, metadata))
                            subtipo_info = f" (subtipo: {item_with_type.get('subtype', 'ninguno')})" if item_with_type.get('subtype') else ""
                            logging.debug(f"Entidad cargada: {item_with_type.get('id', 'unknown')} como tipo '{entity_type_mapped}'{subtipo_info}")
                        else:
                            subtipo = item_with_type.get('subtype', 'ninguno')
                            logging.warning(f"No hay plantilla para tipo '{entity_type_mapped}' subtipo '{subtipo}' (entidad {item.get('id', 'unknown')})")

            logging.info(f"Entidades cargadas desde {json_file}: {len([e for e in entities if e[0] == json_file])}")
        except Exception as e:
            logging.error(f"Error al cargar {json_file}: {e}")
    return entities
    

def sanitize_filename(name):
    """Convierte un nombre en un formato seguro para nombres de carpetas."""
    return "".join(c if c.isalnum() or c in " _-" else "_" for c in name)

def check_json_output_exists(json_file, entities, type_to_folder, template_map, templates, cover_settings):
    """Verifica si todos los archivos de salida existen y su contenido no ha cambiado."""
    try:
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "entidades" not in data:
            logging.error(f"Formato inválido en {json_file} al verificar salida.")
            return False

        metadata = {
            "juego": data.get("juego", "Unknown"),
            "entorno_de_campanya": data.get("entorno_de_campanya", "Unknown"),
            "modul_tipe": data.get("modul_tipe", "Unknown"),
            "cover": data.get("cover", {})
        }
        safe_juego = sanitize_filename(metadata["juego"])
        safe_entorno = sanitize_filename(metadata["entorno_de_campanya"])
        safe_modul = sanitize_filename(metadata["modul_tipe"])

        # Verificar Markdown principal
        main_md_path = os.path.join(OUTPUT_DIR, safe_juego, safe_entorno, safe_modul, f"{safe_modul}.md")
        if not os.path.exists(main_md_path):
            logging.debug(f"Falta Markdown principal: {main_md_path}")
            return False

        # Comparar contenido del Markdown principal (incluye portada/contraportada)
        expected_md = generate_main_markdown(metadata, data, template_map, templates, cover_settings)
        with open(main_md_path, 'r', encoding='utf-8') as f:
            existing_md = f.read()
        if hashlib.md5(expected_md.encode()).hexdigest() != hashlib.md5(existing_md.encode()).hexdigest():
            logging.debug(f"Markdown principal modificado: {main_md_path}")
            return False

        # Verificar JSON de referencias
        ref_json_path = os.path.join(OUTPUT_DIR, safe_juego, safe_entorno, safe_modul, f"{os.path.basename(json_file).replace('.json', '_referencias.json')}")
        if not os.path.exists(ref_json_path):
            logging.debug(f"Falta JSON de referencias: {ref_json_path}")
            return False

        # Verificar archivos de entidades y su contenido
        entities_for_json = [e for e in entities if e[0] == json_file]
        for _, entity, _ in entities_for_json:
            tipo = entity.get("type")
            plantilla = get_template_name(entity, templates, template_map)
            if not plantilla or not os.path.exists(os.path.join(TEMPLATE_DIR, plantilla)):
                logging.debug(f"Plantilla no encontrada para {entity.get('id', 'unknown')} ({tipo}).")
                return False

            name = entity.get("name") or entity.get("id", "unknown")
            safe_name = sanitize_filename(name)
            folder_name = type_to_folder.get(tipo, tipo)
            md_path = os.path.join(OUTPUT_DIR, safe_juego, safe_entorno, safe_modul, folder_name, f"{safe_name}.md")
            json_path = os.path.join(OUTPUT_DIR, safe_juego, safe_entorno, safe_modul, folder_name, f"{safe_name}.json")

            if not os.path.exists(md_path):
                logging.debug(f"Falta archivo Markdown: {md_path}")
                return False
            if not os.path.exists(json_path):
                logging.debug(f"Falta archivo JSON: {json_path}")
                return False

            # Comparar contenido del JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                existing_entity = json.load(f)
            if hash_dict(entity) != hash_dict(existing_entity):
                logging.debug(f"Entidad {entity.get('id', 'unknown')} modificada en {json_file}")
                return False

        logging.info(f"Todos los archivos de salida para {json_file} existen y no han cambiado.")
        return True
    except Exception as e:
        logging.error(f"Error al verificar salida para {json_file}: {e}")
        return False

def update_json_with_references(original_data, extracted_entities, output_paths):
    """Actualiza el JSON original con referencias a las entidades extraídas."""
    updated_data = copy.deepcopy(original_data)
    updated_data.setdefault("referencias", [])

    for entity, output_path in zip(extracted_entities, output_paths):
        entity_id = entity.get("id")
        entity_type = entity.get("type")
        if entity_type in updated_data["entidades"]:
            updated_data["entidades"][entity_type] = [
                e for e in updated_data["entidades"][entity_type] if e.get("id") != entity_id
            ]
        updated_data["referencias"].append({
            "id": entity_id,
            "type": entity_type,
            "path": output_path
        })

    return updated_data

def generate_cover(metadata, cover_settings, template_map, templates):
    """Genera la portada usando plantilla o configuración dinámica."""
    modul_tipe = metadata.get("modul_tipe", "unknown").lower()
    cover_data = metadata.get("cover", {})

    # Combinar metadatos con valores por defecto
    cover_config = cover_settings.get("cover", {})
    defaults = cover_config.get("defaults", {})
    cover_data = {
        "title": cover_data.get("title", defaults.get("title", "").format(**metadata)),
        "subtitle": cover_data.get("subtitle", defaults.get("subtitle", "")),
        "author": cover_data.get("author", defaults.get("author", "")),
        "juego": metadata.get("juego", defaults.get("juego", "")),
        "entorno_de_campanya": metadata.get("entorno_de_campanya", ""),
        "modul_tipe": capitalize(metadata.get("modul_tipe", ""))
    }

    # Buscar plantilla específica
    cover_template = get_cover_template(modul_tipe, template_map, "cover", templates)
    if cover_template:
        try:
            with open(os.path.join(TEMPLATE_DIR, cover_template), 'r', encoding='utf-8') as f:
                template_content = f.read()
            output = render_template(template_content, cover_data)
            logging.debug(f"Portada generada con plantilla {cover_template}")
            return output
        except Exception as e:
            logging.error(f"Error al usar plantilla {cover_template}: {e}")

    # Usar plantilla dinámica
    template = cover_config.get("template", "")
    output = render_template(template, cover_data)
    logging.debug("Portada generada con plantilla dinámica")
    return output

def generate_back_cover(metadata, cover_settings, template_map, templates):
    """Genera la contraportada usando plantilla o configuración dinámica."""
    modul_tipe = metadata.get("modul_tipe", "unknown").lower()
    cover_data = metadata.get("cover", {})

    # Combinar metadatos con valores por defecto
    back_cover_config = cover_settings.get("back_cover", {})
    defaults = back_cover_config.get("defaults", {})
    back_cover_data = {
        "title": cover_data.get("title", defaults.get("title", "").format(**metadata)),
        "description": cover_data.get("description", defaults.get("description", "")),
        "credits": cover_data.get("credits", defaults.get("credits", "")),
        "entorno_de_campanya": metadata.get("entorno_de_campanya", ""),
        "modul_tipe": capitalize(metadata.get("modul_tipe", ""))
    }

    # Buscar plantilla específica
    back_cover_template = get_cover_template(modul_tipe, template_map, "back_cover", templates)
    if back_cover_template:
        try:
            with open(os.path.join(TEMPLATE_DIR, back_cover_template), 'r', encoding='utf-8') as f:
                template_content = f.read()
            output = render_template(template_content, back_cover_data)
            logging.debug(f"Contraportada generada con plantilla {back_cover_template}")
            return output
        except Exception as e:
            logging.error(f"Error al usar plantilla {back_cover_template}: {e}")

    # Usar plantilla dinámica
    template = back_cover_config.get("template", "")
    output = render_template(template, back_cover_data)
    logging.debug("Contraportada generada con plantilla dinámica")
    return output

def generate_main_markdown(metadata, original_data, template_map, templates, cover_settings):
    """Genera el Markdown principal con portada, contenido y contraportada."""
    # Generar portada
    cover_content = generate_cover(metadata, cover_settings, template_map, templates)

    # Generar contenido principal
    main_content = f"# {capitalize(metadata['modul_tipe'])}: {capitalize(metadata['entorno_de_campanya'])}\n\n"
    main_content += "## Entidades Incluidas\n\n"

    for entity_type, entity_list in original_data["entidades"].items():
        if not entity_list:
            continue
        capitalized_type = capitalize(entity_type)
        main_content += f"### {capitalized_type}\n\n"
        for entity in entity_list:
            tipo = entity.get("type")
            if tipo in template_map:
                plantilla = get_template_name(entity, templates, template_map)
                if plantilla:
                    entity_content = render_entity(entity, plantilla)
                    main_content += entity_content + "\n\n"

    # Generar contraportada
    back_cover_content = generate_back_cover(metadata, cover_settings, template_map, templates)

    # Combinar todo
    md_content = f"{cover_content}\n{main_content}\n{back_cover_content}"
    logging.debug(f"Markdown principal generado para {metadata['modul_tipe']}: {metadata['entorno_de_campanya']}")
    return md_content

def print_summary(json_status):
    """Imprime un resumen visual con colores y arte ASCII."""
    print("\n" + Fore.CYAN + "╔══════════════════════════════╗")
    print(Fore.CYAN + "║       Resumen de Proceso     ║")
    print(Fore.CYAN + "╚══════════════════════════════╝")
    for json_file, status in json_status.items():
        status_color = {
            "Procesado": Fore.GREEN,
            "Omitido": Fore.YELLOW,
            "Error": Fore.RED
        }.get(status, Fore.WHITE)
        print(f"{status_color}- {os.path.basename(json_file)}: {status}{Style.RESET_ALL}")
    print(Fore.CYAN + "╚══════════════════════════════╝\n")

def main():
    # Parsear argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Generador de contenido D&D 5e")
    parser.add_argument('--batch', choices=['overwrite'], help="Modo batch para sobreescritura automática")
    args = parser.parse_args()

    # Crear carpeta config si no existe
    os.makedirs(CONFIG_DIR, exist_ok=True)
    logging.info("Inicio del procesamiento.")

    # Cargar configuraciones
    template_map = load_template_map()
    if not template_map:
        logging.error("No se pudo cargar template_map.json. Terminando.")
        return

    type_to_folder = load_type_to_folder()
    required_fields = load_required_fields()
    cover_settings = load_cover_settings()

    # Verificar plantillas
    templates = list_templates()
    if not templates:
        logging.error("Crea al menos una plantilla en template/. Terminando.")
        return

    # Cargar todos los archivos JSON de input/
    json_files = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    if not json_files:
        logging.error("No hay archivos JSON en la carpeta input. Terminando.")
        return

    # Cargar todas las entidades
    all_entities = load_entities(json_files, template_map)
    if not all_entities:
        logging.error("No se encontraron entidades válidas con plantillas asociadas. Terminando.")
        return

    # Procesar en modo single con barra de progreso
    mode = "single"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_status = {}

    # Barra de progreso para JSON
    for json_file in tqdm(json_files, desc="Processing JSON files", mininterval=0.1):
        start_time = time.time()
        json_status[json_file] = "Procesado"

        try:
            # Verificar si todos los archivos de salida existen y no han cambiado
            if check_json_output_exists(json_file, all_entities, type_to_folder, template_map, templates, cover_settings):
                json_status[json_file] = "Omitido"
                logging.info(f"JSON {json_file} ya procesado completamente. Omitido.")
                elapsed_time = time.time() - start_time
                if elapsed_time < 15:
                    delay = 15 - elapsed_time
                    logging.debug(f"Añadiendo retraso de {delay:.2f} segundos para {json_file}")
                    time.sleep(delay)
                continue

            with open(json_file, encoding="utf-8") as f:
                original_data = json.load(f)

            extracted_entities = []
            output_paths = []

            # Filtrar entidades para el JSON actual
            entities_for_json = [e for e in all_entities if e[0] == json_file]

            # Barra de progreso para entidades
            for _, entity, metadata in tqdm(entities_for_json, desc="Processing entities", leave=False):
                tipo = entity.get("type")
                plantilla = get_template_name(entity, templates, template_map)
                if not plantilla or not os.path.exists(os.path.join(TEMPLATE_DIR, plantilla)):
                    logging.error(f"Plantilla no encontrada para {entity.get('id', 'unknown')} ({tipo}).")
                    continue

                if validate_entity(entity, tipo, required_fields):
                    continue

                md = render_entity(entity, plantilla)
                name = entity.get("name") or entity.get("id", "unknown")
                safe_name = sanitize_filename(name)
                safe_juego = sanitize_filename(metadata["juego"])
                safe_entorno = sanitize_filename(metadata["entorno_de_campanya"])
                safe_modul = sanitize_filename(metadata["modul_tipe"])
                folder_name = type_to_folder.get(tipo, tipo)
                out_folder = os.path.join(OUTPUT_DIR, safe_juego, safe_entorno, safe_modul, folder_name)
                os.makedirs(out_folder, exist_ok=True)

                md_path = os.path.join(out_folder, f"{safe_name}.md")
                write_file(md_path, md, batch_mode=args.batch)

                json_path = os.path.join(out_folder, f"{safe_name}.json")
                write_json_file(json_path, entity, batch_mode=args.batch)

                extracted_entities.append(entity)
                output_paths.append(os.path.join(safe_juego, safe_entorno, safe_modul, folder_name, f"{safe_name}.md"))

            # Actualizar JSON con referencias
            if extracted_entities:
                updated_data = update_json_with_references(original_data, extracted_entities, output_paths)
                safe_modul = sanitize_filename(original_data.get("modul_tipe", "unknown"))
                safe_juego = sanitize_filename(original_data.get("juego", "Unknown"))
                safe_entorno = sanitize_filename(original_data.get("entorno_de_campanya", "Unknown"))
                ref_folder = os.path.join(OUTPUT_DIR, safe_juego, safe_entorno, safe_modul)
                os.makedirs(ref_folder, exist_ok=True)
                ref_json_path = os.path.join(ref_folder, f"{os.path.basename(json_file).replace('.json', '_referencias.json')}")
                write_json_file(ref_json_path, updated_data, batch_mode=args.batch)

                # Generar Markdown principal con portada y contraportada
                main_md = generate_main_markdown(metadata, original_data, template_map, templates, cover_settings)
                main_md_path = os.path.join(ref_folder, f"{safe_modul}.md")
                write_file(main_md_path, main_md, batch_mode=args.batch)

        except Exception as e:
            json_status[json_file] = "Error"
            logging.error(f"Error procesando {json_file}: {e}")

        # Añadir retraso si el procesamiento fue menor a 15 segundos
        elapsed_time = time.time() - start_time
        if elapsed_time < 15:
            delay = 15 - elapsed_time
            logging.debug(f"Añadiendo retraso de {delay:.2f} segundos para {json_file}")
            time.sleep(delay)

    # Imprimir resumen visual
    print_summary(json_status)
    logging.info("Resumen de procesamiento:")
    for json_file, status in json_status.items():
        logging.info(f"{os.path.basename(json_file)}: {status}")

    logging.info("Procesamiento completado.")

if __name__ == "__main__":
    main()