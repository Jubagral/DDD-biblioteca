
#!/usr/bin/env python3

import os
import json
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directorio base
BASE_DIR = "/home/runner/workspace"

# Definir estructura de carpetas
DIRECTORIES = [
    "config",
    "input",
    "template/monster",
    "template/item",
    "template/pnj",
    "template/pj",
    "template/spell",
    "template/cover/adventure",
    "template/cover/item_pack",
    "outh"
]

# Archivos y sus contenidos
FILES = {
    "config/template_map.json": {
        "monster": "monster/monster.md",
        "item": {
            "default": "item/item.md",
            "weapon": "item/weapon.md",
            "potion": "item/potion.md"
        },
        "pnj": "pnj/pnj.md",
        "pj": "pj/pj.md",
        "spell": {
            "default": "spell/spell.md"
        },
        "trap": "trap/trap.md",
        "encounter": "encounter/encounter.md",
        "event": "event/event.md",
        "plane": "plane/plane.md",
        "scene": "scene/scene.md",
        "environment": "environment/environment.md",
        "class": "class/class.md",
        "location": "location/location.md",
        "adventure": "adventure/adventure.md",
        "hook": "hook/hook.md",
        "objective": "objective/objective.md",
        "familiar": "familiar/familiar.md",
        "mount": "mount/mount.md",
        "item_pack": "item_pack/item_pack.md",
        "covers": {
            "adventure": {
                "cover": "cover/adventure/portada.md",
                "back_cover": "cover/adventure/contraportada.md"
            },
            "item_pack": {
                "cover": "cover/item_pack/portada.md",
                "back_cover": "cover/item_pack/contraportada.md"
            }
        }
    },
    "config/required_fields.json": {
        "item": ["type", "subtype", "id", "name", "rarity", "description", "mechanics.cost"],
        "monster": [],
        "pnj": ["type", "id", "name", "description", "alignment"],
        "pj": ["type", "id", "name", "description", "class", "level"]
    },
    "config/type_to_folder.json": {
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
    },
    "config/cover_settings.json": {
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
    },
    "template/monster/monster.md": """# {name}
*{type} {size}, {alignment}*
### Descripción
{description}
### Estadísticas
- **Clase de Armadura:** {armor_class.value} ({armor_class.type})
- **Puntos de Golpe:** {hit_points.value} ({hit_points.hit_dice} + {hit_points.modifier})
- **Velocidad:** {speed.walk} pies{speed.fly_text}
### Rasgos
{traits_formatted}
### Acciones
{actions_formatted}
{{homebreweryCredits
Donde Duermen los Dados
:
[Https://ko-fi.com/dondeduermenlosdados](https://ko-fi.com/dondeduermenlosdados)
}}""",
    "template/monster/monster.json": {
        "required_fields": ["id", "name", "type", "alignment"],
        "optional_fields": ["description", "armor_class", "hit_points", "speed"],
        "schema": {}
    },
    "template/item/item.md": """# {name}
*{type}*
### Descripción
{description}
### Detalles
- **Rareza:** {rarity}
- **Costo:** {mechanics.cost}""",
    "template/item/weapon.md": """# {name}
*{type}*
### Descripción
{description}
### Detalles
- **ID:** {id}
- **Subtipo:** {subtype}
- **Alineamiento:** {alignment}
{{homebreweryCredits
Donde Duermen los Dados
:
[Https://ko-fi.com/dondeduermenlosdados](https://ko-fi.com/dondeduermenlosdados)
}}""",
    "template/item/potion.md": """# {name}
*{type}*
### Descripción
{description}
### Detalles
- **ID:** {id}
- **Subtipo:** {subtype}
- **Alineamiento:** {alignment}
{{homebreweryCredits
Donde Duermen los Dados
:
[Https://ko-fi.com/dondeduermenlosdados](https://ko-fi.com/dondeduermenlosdados)
}}""",
    "template/pnj/pnj.md": """# {name}
*{type}*
### Descripción
{description}
### Detalles
- **ID:** {id}
- **Subtipo:** {subtype}
- **Alineamiento:** {alignment}
{{homebreweryCredits
Donde Duermen los Dados
:
[Https://ko-fi.com/dondeduermenlosdados](https://ko-fi.com/dondeduermenlosdados)
}}""",
    "template/pj/pj.md": """# {name}
*{type}*
### Descripción
{description}
### Detalles
- **ID:** {id}
- **Subtipo:** {subtype}
- **Alineamiento:** {alignment}
{{homebreweryCredits
Donde Duermen los Dados
:
[Https://ko-fi.com/dondeduermenlosdados](https://ko-fi.com/dondeduermenlosdados)
}}""",
    "template/spell/spell.md": """# {name}
*{type}*
### Descripción
{description}
### Detalles
- **ID:** {id}
- **Subtipo:** {subtype}
- **Alineamiento:** {alignment}
{{homebreweryCredits
Donde Duermen los Dados
:
[Https://ko-fi.com/dondeduermenlosdados](https://ko-fi.com/dondeduermenlosdados)
}}""",
    "template/item/item.json": {"required_fields": [], "optional_fields": [], "schema": {}},
    "template/pnj/pnj.json": {"required_fields": [], "optional_fields": [], "schema": {}},
    "template/pj/pj.json": {"required_fields": [], "optional_fields": [], "schema": {}},
    "template/spell/spell.json": {"required_fields": [], "optional_fields": [], "schema": {}},
    "template/cover/adventure/portada.md": "# {title}\n## {subtitle}",
    "template/cover/adventure/contraportada.md": "# Contraportada",
    "template/cover/item_pack/portada.md": "# {title}",
    "template/cover/item_pack/contraportada.md": "# Contraportada"
}

def create_directories():
    """Crea las carpetas necesarias si no existen."""
    for directory in DIRECTORIES:
        path = os.path.join(BASE_DIR, directory)
        try:
            os.makedirs(path, exist_ok=True)
            logging.info(f"Creada carpeta: {path}")
        except Exception as e:
            logging.error(f"Error al crear carpeta {path}: {e}")

def create_file(file_path, content):
    """Crea un archivo si no existe, con el contenido especificado."""
    full_path = os.path.join(BASE_DIR, file_path)
    if os.path.exists(full_path):
        logging.info(f"{full_path} ya existe, omitiendo...")
        return
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if isinstance(content, dict):
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        logging.info(f"Creado archivo: {full_path}")
    except Exception as e:
        logging.error(f"Error al crear archivo {full_path}: {e}")

def main():
    """Función principal para crear carpetas y archivos."""
    logging.info("Iniciando configuración de carpetas y archivos...")
    create_directories()
    for file_path, content in FILES.items():
        create_file(file_path, content)
    logging.info("Configuración completada.")
    logging.info("Verifica las plantillas completas (monster.md, monster.json, item.md) desde los artefactos correspondientes.")
    logging.info("Copia los JSONs de entrada (bestia_resina.json, etc.) a input/ manualmente.")
    logging.info(f"Ejecuta el programa con: python3 {BASE_DIR}/programa_sh.py --batch overwrite")

if __name__ == "__main__":
    main()
