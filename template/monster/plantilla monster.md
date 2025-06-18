\page
{{chapter,four
# {escape(name)}
## *{alias}*
*{capitalize(type)}, {capitalize(alignment)}*
}}

![homebrew mug](https://imgur.com/vj3ulQu.png) {position:absolute,top:50px,right:40px,width:80px}

### Descripción
{escape(description)}

{{note
### Trasfondo
{escape(background)}
}}

### Estadísticas
- **Clase de Armadura:** {armor_class.value} ({armor_class.type})
- **Puntos de Golpe:** {hit_points.value} ({hit_points.hit_dice} + {hit_points.modifier})
- **Velocidad:** {speed.walk} pies{speed.fly_text}{speed.climb_text}{speed.swim_text}{speed.burrow_text}

| **FUE** | **DES** | **CON** | **INT** | **SAB** | **CAR** |
|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| {ability_scores.strength} ({ability_scores.strength_modifier}) | {ability_scores.dexterity} ({ability_scores.dexterity_modifier}) | {ability_scores.constitution} ({ability_scores.constitution_modifier}) | {ability_scores.intelligence} ({ability_scores.intelligence_modifier}) | {ability_scores.wisdom} ({ability_scores.wisdom_modifier}) | {ability_scores.charisma} ({ability_scores.charisma_modifier}) |

- **Tiradas de Salvación:** {saving_throws_formatted}
- **Habilidades:** {skills_formatted}
- **Resistencias al Daño:** {format_array(damage_resistances)}
- **Inmunidades al Daño:** {format_array(damage_immunities)}
- **Inmunidades a Condiciones:** {format_array(condition_immunities)}
- **Sentidos:** {senses}
- **Idiomas:** {languages}
- **Desafío:** {challenge_rating} {bonus **Bonificación de Pericia** +{proficiency_bonus}}

### Rasgos
{traits_formatted}

### Acciones
{actions_formatted}

{legendary_actions_formatted}

### Tácticas de Combate
{escape(combat_tactics)}

{{homebreweryCredits
Donde Duermen los Dados
![homebrew mug](https://imgur.com/vj3ulQu.png) {position:absolute,top:50px,right:30px,width:80px}
:
[Https://ko-fi.com/dondeduermenlosdados](https://ko-fi.com/dondeduermenlosdados)
}}

{{footnote
{escape(name)} | Criatura Nº {creature_number}
}}

\page
{{chapter,four
# {escape(name)}
*{capitalize(type)}, {capitalize(alignment)}*
}}

![homebrew mug](https://imgur.com/vj3ulQu.png) {position:absolute,top:50px,right:40px,width:80px}

## Interés
{escape(interes)}

{para_el_dm}

{{monster,frame
## {escape(name)}
*{alias}*
*{capitalize(type)}, {capitalize(alignment)}*
___
**Clase de Armadura** :: {armor_class.value} ({armor_class.type})
**Puntos de Golpe** :: {hit_points.value} ({hit_points.hit_dice} + {hit_points.modifier})
**Velocidad** :: {speed.walk} pies{speed.fly_text}{speed.climb_text}{speed.swim_text}{speed.burrow_text}
___
| STR | DEX | CON | INT | WIS | CHA |
|:---:|:---:|:---:|:---:|:---:|:---:|
| {ability_scores.strength} ({ability_scores.strength_modifier}) | {ability_scores.dexterity} ({ability_scores.dexterity_modifier}) | {ability_scores.constitution} ({ability_scores.constitution_modifier}) | {ability_scores.intelligence} ({ability_scores.intelligence_modifier}) | {ability_scores.wisdom} ({ability_scores.wisdom_modifier}) | {ability_scores.charisma} ({ability_scores.charisma_modifier}) |
___
**Tiradas de Salvación** :: {saving_throws_formatted}
**Habilidades** :: {skills_formatted}
**Resistencias** :: {format_array(damage_resistances)}
**Inmunidades** :: {format_array(damage_immunities)}
**Condiciones** :: {format_array(condition_immunities)}
**Sentidos** :: {senses}
**Idiomas** :: {languages}
**Desafío** :: {challenge_rating} {bonus **Bonificación de Pericia** +{proficiency_bonus}}
___
{traits_formatted}

### Acciones
{actions_formatted}

{legendary_actions_formatted}
}}

{{homebreweryCredits
Made With
{{homebreweryIcon}}
The Homebrewery
[Homebrewery.Naturalcrit.com](https://homebrewery.naturalcrit.com)
:
Serie oficial de criaturas coleccionables creada por [Donde Duermen los Dados](https://ko-fi.com/dondeduermenlosdados) · 2025
}}

{{imageMaskCorner20,--offsetX:{image_mask.offsetX},--offsetY:{image_mask.offsetY},--rotation:{image_mask.rotation}
!{top:{image_mask.position.top},right:{image_mask.position.right},width:{image_mask.position.width},opacity:{image_mask.position.opacity}}
}}

{{footnote
{escape(name)} | Criatura Nº {creature_number}
}}