
#  README.md

### Generador de Contenido D&D 5e para Homebrewery

Genera contenido para *D&D 5e 2025* en formato Markdown compatible con Homebrewery a partir de todos los archivos JSON en `input/`, usando el modo `single` (Markdown principal con portada, contenido, contraportada, y archivos separados). Verifica si los archivos en `outh/` existen y compara su contenido para procesar solo entidades modificadas. Soporta plantillas por subtipo (por ejemplo, pociones). Genera portadas y contraportadas usando un enfoque híbrido: plantillas específicas (`portada.md`, `contraportada.md`) mapeadas en `template_map.json` o plantillas dinámicas en `config/cover_settings.json`, con personalización vía `cover` en los JSON. Cada JSON se simula para tomar al menos 15 segundos, asegurando que la barra de progreso sea visible. En modo interactivo, pregunta para confirmar la sobreescritura; en modo batch (`--batch overwrite`), sobreescribe automáticamente. Muestra un resumen visual con colores y arte ASCII. Los mensajes se guardan en `log.txt`.

## Estructura de Carpetas
```
- config/               # Archivos de configuración (type_to_folder.json, required_fields.json, cover_settings.json)
- input/                # Archivos JSON con metadatos y entidades
- template/             # Plantillas de texto (.md, incluyendo portada.md, contraportada.md)
- outh/                 # Archivos Markdown, JSON y JSON de referencias
- template_map.json     # Mapeo de tipos/subtipos y portadas/contraportadas
- programa_sh.py        # Programa principal
- log.txt               # Registro de procesamiento
```

## Requisitos
- Python 3.13
- Bibliotecas `tqdm` y `colorama`:
  ```bash
  C:/laragon/bin/python/python-3.13/pip.exe install tqdm colorama
  ```

## Instalación
1. Crear las carpetas:
   ```bash
   mkdir -p c:/Users/Juan/Desktop/json_j2/programa/config
   mkdir -p c:/Users/Juan/Desktop/json_j2/programa/input
   mkdir -p c:/Users/Juan/Desktop/json_j2/programa/template
   mkdir -p c:/Users/Juan/Desktop/json_j2/programa/outh
   ```
2. Instalar `tqdm` y `colorama` (ver Requisitos).
3. Configurar `template_map.json`, `config/type_to_folder.json`, `config/required_fields.json`, y `config/cover_settings.json`.
4. Añadir plantillas (por ejemplo, `item.md`, `potion.md`, `character.md`, `portada.md`, `contraportada.md`) a `template/`.
5. Añadir JSON con metadatos, entidades, y opcionalmente `cover` (por ejemplo, `modulo_dragon_lance.json`) a `input/`.

## Uso
1. Ejecutar el programa en modo interactivo:
   ```bash
   C:/laragon/bin/python/python-3.13/python.exe c:/Users/Juan/Desktop/json_j2/programa/programa_sh.py
   ```
   O en modo batch:
   ```bash
   C:/laragon/bin/python/python-3.13/python.exe c:/Users/Juan/Desktop/json_j2/programa/programa_sh.py --batch overwrite
   ```
2. Carga todos los JSON en `input/` y verifica si sus archivos en `outh/` existen y no han cambiado.
3. Omite los JSON sin cambios; procesa los modificados, mostrando una barra de progreso (mínimo 15 segundos por JSON).
4. Genera portadas y contraportadas usando plantillas mapeadas en `template_map.json` o dinámicas en `config/cover_settings.json`.
5. En modo interactivo, pregunta "¿Sobreescribir <ruta>? (s/n): "; en modo batch, sobreescribe automáticamente.
6. Muestra un resumen visual con colores y arte ASCII (Procesado, Omitido, Error).
7. Verificar el Markdown en `outh/<juego>/<entorno_de_campanya>/<modul_tipe>/<tipo_plural>/` usando Homebrewery.
8. Consultar `log.txt` para detalles.

## Estructura JSON
- **Metadatos**: `juego`, `entorno_de_campanya`, `modul_tipe`.
- **Cover** (opcional): `title`, `subtitle`, `author`, `description`, `credits` para personalizar portada/contraportada.
- **Entidades**: Objeto con listas de `items`, `monsters`, `pnj`, etc.
- **Referencias**: Generadas en `<modul_tipe>_referencias.json` con rutas a los Markdown.

Ejemplo:
```json
{
  "juego": "D&D 5e 2024",
  "entorno_de_campanya": "Dragon Lance",
  "modul_tipe": "adventur",
  "cover": {
    "title": "El Módulo Épico",
    "subtitle": "Aventuras en Krynn",
    "author": "Juan",
    "description": "Un viaje épico por el mundo de Dragon Lance.",
    "credits": "Diseñado por Juan para D&D 5e 2025"
  },
  "entidades": {
    "items": [
      {
        "id": "ITEM001",
        "type": "item",
        "subtype": "potion",
        "name": "Poción de Curación",
        "rarity": "común",
        "description": "líquida roja brillante",
        "mechanics": {
          "cost": 50,
          "effects": "Recuperas 2d4 + 2 puntos de golpe",
          "duration": "Instantáneo"
        }
      }
    ]
  }
}
```

## Estructura de Salida
- `outh/<juego>/<entorno_de_campanya>/<modul_tipe>/<tipo_plural>/<nombre_entidad>.md`
- `outh/<juego>/<entorno_de_campanya>/<modul_tipe>/<nombre_entidad>.json`
- `outh/<juego>/<entorno_de_campanya>/<modul_tipe>/<modul_tipe>.md` (con portada, contenido, contraportada)
- `outh/<juego>/<entorno_de_campanya>/<modul_tipe>/<nombre_json>_referencias.json`

Ejemplo:
- `outh/D&D_5e_2024/Dragon_Lance/adventur/items/Poción_de_Curación.md`
- `outh/D&D_5e_2024/Dragon_Lance/adventur/adventur.md` (incluye portada y contraportada)
- `outh/D&D_5e_2024/Dragon_Lance/adventur/modulo_dragon_lance_referencias.json`

## Configuración
- `config/type_to_folder.json`: Mapea tipos a carpetas plurales.
- `config/required_fields.json`: Define campos obligatorios por tipo.
- `config/cover_settings.json`: Define plantillas dinámicas y valores por defecto para portada/contraportada.
- `template_map.json`: Mapea tipos, subtipos, y portadas/contraportadas.

## Plantillas Soportadas
Ver `template_map.json`. Ejemplos:
- `item.md`: Ítems genéricos
- `potion.md`: Pociones
- `character.md`: PNJ y PJ
- `monster.md`: Monstruos
- `spell.md`: Hechizos
- `portada.md`: Portada personalizada
- `contraportada.md`: Contraportada personalizada

## Depuración
- Consultar `log.txt` para errores, detalles, JSON omitidos, y retrasos.
- Verifica que `config/` contenga `type_to_folder.json`, `required_fields.json`, y `cover_settings.json`.
- Verifica que `template/` contenga plantillas `.md` (incluyendo `portada.md`, `contraportada.md` si se usan).
- Asegúrate de que los archivos estén en UTF-8 sin BOM.
```
---

### Configuración y Prueba

1. **Instalar Dependencias**:
   ```bash
   C:/laragon/bin/python/python-3.13/pip.exe install tqdm colorama
   ```

2. **Verificar la Estructura de Carpetas**:
   ```bash
   ls -l c:/Users/Juan/Desktop/json_j2/programa/
   ```
   Deberías ver:
   ```
   config/
   input/
   outh/
   template/
   template_map.json
   programa_sh.py
   log.txt
   ```

3. **Configuración de Archivos**:
   - En `config/`:
     - `type_to_folder.json` (artefacto `9b800a37-8eee-4604-9dcf-77786b4d0c94`).
     - `required_fields.json` (artefacto `cc07b4b9-c0bd-4a5a-90ee-98ad8d9beff6`).
     - `cover_settings.json` (artefacto `c9a0948a-0af3-4b2f-8c2e-ef43ce4b92f6`).
   - En `template/`:
     - `item.md` (artefacto `4b1bdd47-1968-44cd-b7ed-013360afceed`).
     - `potion.md` (artefacto `608adf1e-66e1-40e2-a3cd-ac045db82524`).
     - `character.md` (artefacto `bea59182-69d3-4d2e-9516-9c5fa6bea6d7`).
     - `monster.md` (artefacto `80f357a2-bcae-45d6-ab47-7391cd977147`).
     - `spell.md` (artefacto `85b7fa54-dacb-4974-85d4-9cc1c89c2c19`).
     - `portada.md` (artefacto `f3a4b5c6-d7e8-4f9a-0b1c-2d3e4f5a6b7c`).
     - `contraportada.md` (artefacto `a0b1c2d3-e4f5-4a6b-7c8d-9e0f1a2b3c4d`).
   - En `input/`:
     - `modulo_dragon_lance.json` (artefacto `869d3be4-4a74-45a6-901a-95f355086441`).
     - `modulo_forgotten_realms.json` (artefacto `42a099c5-a8a8-4fe4-8d2f-2bd6925fa76d`).
     - `modulo_eberron.json` (artefacto `db5d4bfc-d1b4-426b-8685-0e20c1b2fa24`).
   - En la raíz:
     - `template_map.json` (artefacto `73982883-8bb2-4770-9a47-4e6e1898442a`).
     - `programa_sh.py` (artefacto `d22f7ebb-40b5-4c72-b766-1d229ba1a830`).

4. **Ejecutar el Programa**:
   - **Modo Interactivo**:
     ```bash
     C:/laragon/bin/python/python-3.13/python.exe c:/Users/Juan/Desktop/json_j2/programa/programa_sh.py
     ```
   - **Modo Batch**:
     ```bash
     C:/laragon/bin/python/python-3.13/python.exe c:/Users/Juan/Desktop/json_j2/programa/programa_sh.py --batch overwrite
     ```
   - Verás la barra de progreso, preguntas de sobreescritura (en modo interactivo), y el resumen visual:
     ```
     Processing JSON files: 33%|███▎      | 1/3 [00:15<00:30, 15.00s/it]
     ¿Sobreescribir outh/D&D_5e_2024/Dragon_Lance/adventur/items/Poción_de_Curación.md? (s/n): s
     ...
     Processing JSON files: 100%|██████████| 3/3 [00:45<00:00, 15.00s/it]

     ╔══════════════════════════════╗
     ║       Resumen de Proceso     ║
     ╚══════════════════════════════╝
     - modulo_dragon_lance.json: Procesado
     - modulo_forgotten_realms.json: Omitido
     - modulo_eberron.json: Procesado
     ╚══════════════════════════════╝
     ```

5. **Verificar la Salida**:
   - Archivos generados:
     - `outh/D&D_5e_2024/Dragon_Lance/adventur/adventur.md` (con portada y contraportada usando `portada.md` y `contraportada.md`).
     - `outh/D&D_5e_2024/Dragon_Lance/adventur/items/Poción_de_Curación.md`.
     - etc.
   - Copia `adventur.md` y pégalo en https://homebrewery.naturalcrit.com/new. Verifica que la portada y contraportada se rendericen con `phb#first-page` y `phb#page-cover`.
   - Revisa `log.txt` para detalles (por ejemplo, "Portada generada con plantilla portada.md").

6. **Probar el Enfoque Híbrido**:
   - **Plantilla Específica**:
     - Verifica que `modulo_dragon_lance.json` use `portada.md` y `contraportada.md` (mapeadas en `template_map.json` para `adventure`).
   - **Plantilla Dinámica**:
     - Modifica `modulo_forgotten_realms.json` (sin `cover`) y elimina su mapeo en `template_map.json`. Debería usar la plantilla dinámica de `cover_settings.json`.
   - **Personalización**:
     - Cambia el `cover` en `modulo_dragon_lance.json` (por ejemplo, `"author": "Equipo Krynn"`) y reejecuta. El Markdown debería actualizarse.
   - **Comparación**:
     - Modifica `portada.md` o `cover_settings.json` y reejecuta. `log.txt` debería mostrar "Markdown principal modificado".

7. **Si hay Errores**:
   - Consulta `log.txt` para detalles.
   - Verifica que `cover_settings.json`, `portada.md`, y `contraportada.md` existan.
   - Asegúrate de que los archivos estén en UTF-8 sin BOM.
   - Confirma que `tqdm` y `colorama` estén instalados.

---

### Respuesta a tus Preguntas

1. **¿Por qué Opción 3?**
   - Elegiste la Opción 3 por su flexibilidad: combina plantillas personalizadas (`portada.md`, `contraportada.md`) con configuración dinámica para casos genéricos o personalizados vía JSON. ¿Quieres ajustar las plantillas (por ejemplo, añadir imágenes o CSS en Homebrewery)?

2. **¿Más Personalización?**
   - La portada usa `phb#first-page` y la contraportada `phb#page-cover`. ¿Quieres más campos (por ejemplo, fecha, versión)? ¿O un diseño más complejo (necesitaría CSS adicional)?

3. **¿Más Plantillas o JSON?**
   - He añadido `portada.md` y `contraportada.md`. ¿Necesitas plantillas para otros subtipos (por ejemplo, `location`, `mount`)? ¿O un JSON con más entidades?

4. **¿Pruebas Específicas?**
   - Prueba modificar `cover_settings.json`, `portada.md`, o el `cover` en los JSON. ¿Quieres un Replit configurado para probar online?

---


