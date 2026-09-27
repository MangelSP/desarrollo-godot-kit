class_name TmxReader
extends RefCounted
## Lee un mapa de Tiled (.tmx) directamente, con XMLParser, sin llamar a Tiled ni a su plugin.
## Funciones estáticas puras: no crea nodos ni toca el TileSet de Godot. Las usa
## tools/tiled_to_godot.gd y se pueden probar con GUT. Ver docs/adr/0009-flujo-tiled-godot.md §2.
##
## Subconjunto del formato TMX que se soporta (ADR 0009 §2):
## - Mapa ortogonal, de tamaño fijo (infinite="0").
## - Tilesets externos (<tileset firstgid source="x.tsx">) o embebidos, de una sola imagen.
## - Capas de tiles con <data encoding="csv"> (lo que Tiled guarda por defecto), con las banderas
##   de giro de Tiled (bits 31, 30 y 29).
## - Capas de objetos con objetos sueltos o hechos con una plantilla .tx; la propiedad resPath
##   puede venir de la plantilla o del objeto (gana la del objeto).
## - Propiedades de capa: noExport (bool), zIndex (int) y ySortEnabled (bool), como el plugin de Tiled.
##   El tipo se comprueba: una propiedad con otro tipo en Tiled (p. ej. string) es un error.
## No se soporta (da error): base64/zlib/gzip/zstd, <data> en XML, mapas infinitos, grupos de
## capas, tilesets de colección de imágenes, la bandera de rotación hexagonal (bit 28), gids
## fuera de 0..0xFFFFFFFF, capas de otro tamaño que el mapa, capas desplazadas (offsetx/offsety),
## con paralaje (parallaxx/parallaxy) u ocultas (visible="0") sin noExport, tilesets con margin,
## spacing o <tileoffset> distinto de 0, objetos de tile (gid) u ocultos con resPath, y XML incompleto
## o mal formado (etiquetas sin cerrar o que no se corresponden).
## Todo esto se detalla en docs/adr/0009-flujo-tiled-godot.md §7.
##
## Uso:
##   var map: TmxReader.TmxMap = TmxReader.read("res://scenes/world/tiled/test_track.tmx")
##   if not map.errors.is_empty(): …

## Banderas de giro que Tiled guarda en los bits altos del gid.
const FLIP_H_FLAG: int = 0x80000000
const FLIP_V_FLAG: int = 0x40000000
const FLIP_D_FLAG: int = 0x20000000
## En mapas hexagonales es la rotación de 120°; en un mapa ortogonal no debería aparecer.
const ROTATED_HEX_FLAG: int = 0x10000000
const GID_MASK: int = 0x0FFFFFFF
## Tiled guarda cada gid como entero sin signo de 32 bits (banderas incluidas).
const MAX_RAW_GID: int = 0xFFFFFFFF

const PROP_NO_EXPORT: String = "noExport"
const PROP_Z_INDEX: String = "zIndex"
const PROP_Y_SORT: String = "ySortEnabled"
const PROP_RES_PATH: String = "resPath"


## Elemento de XML ya leído: nombre, atributos, hijos y texto.
class XmlElement:
	extends RefCounted
	var name: String = ""
	var attributes: Dictionary[String, String] = {}
	var children: Array[XmlElement] = []
	var text: String = ""

	func attr(key: String, default_value: String = "") -> String:
		return attributes.get(key, default_value)

	func first_child(child_name: String) -> XmlElement:
		for child: XmlElement in children:
			if child.name == child_name:
				return child
		return null

	func children_named(child_name: String) -> Array[XmlElement]:
		var result: Array[XmlElement] = []
		for child: XmlElement in children:
			if child.name == child_name:
				result.append(child)
		return result


## Un tileset del mapa. Las rutas son res:// (o absolutas si el .tmx se leyó por ruta absoluta).
class TmxTileset:
	extends RefCounted
	var first_gid: int = 0
	## Archivo donde está definido: el .tsx o, si está embebido, el .tmx.
	var source: String = ""
	var name: String = ""
	## Imagen del atlas; con ella se empareja la fuente del TileSet de Godot.
	var image: String = ""
	var columns: int = 0
	var tile_count: int = 0
	var tile_size: Vector2i = Vector2i.ZERO


## Una celda pintada, ya traducida a lo que entiende un TileMapLayer.
class TmxCell:
	extends RefCounted
	var coords: Vector2i = Vector2i.ZERO
	## gid sin banderas.
	var gid: int = 0
	## Índice en TmxMap.tilesets.
	var tileset_index: int = -1
	var atlas_coords: Vector2i = Vector2i.ZERO
	## Suma de TileSetAtlasSource.TRANSFORM_FLIP_H / FLIP_V / TRANSPOSE (alternativa de Godot).
	var transform: int = 0


class TmxTileLayer:
	extends RefCounted
	var name: String = ""
	var z_index: int = 0
	var y_sort_enabled: bool = false
	## En orden de filas (de arriba abajo, de izquierda a derecha); solo las celdas no vacías.
	var cells: Array[TmxCell] = []


class TmxObject:
	extends RefCounted
	var id: int = 0
	var name: String = ""
	## Nombre de la capa de objetos.
	var layer: String = ""
	## Plantilla .tx de la que sale, si tiene.
	var template: String = ""
	## x, y del objeto en píxeles (para un objeto de punto, el punto).
	var position: Vector2 = Vector2.ZERO
	## Propiedades ya combinadas: primero las de la plantilla, encima las del objeto.
	var properties: Dictionary[String, Variant] = {}
	## Escena a instanciar (propiedad resPath); vacío si el objeto no se exporta.
	var res_path: String = ""


class TmxMap:
	extends RefCounted
	var path: String = ""
	## Tamaño en celdas.
	var size: Vector2i = Vector2i.ZERO
	var tile_size: Vector2i = Vector2i.ZERO
	var tilesets: Array[TmxTileset] = []
	## Capas de tiles en el orden del .tmx (de abajo arriba), sin las que tienen noExport.
	var tile_layers: Array[TmxTileLayer] = []
	## Objetos de todas las capas de objetos, en el orden del .tmx, sin las capas con noExport.
	var objects: Array[TmxObject] = []
	## Si no está vacío, el mapa no se debe convertir.
	var errors: PackedStringArray = PackedStringArray()

	func get_tile_layer(layer_name: String) -> TmxTileLayer:
		for layer: TmxTileLayer in tile_layers:
			if layer.name == layer_name:
				return layer
		return null


## Lee un .tmx del disco (res:// o ruta absoluta).
static func read(tmx_path: String) -> TmxMap:
	var map: TmxMap = TmxMap.new()
	map.path = tmx_path
	if not FileAccess.file_exists(tmx_path):
		map.errors.append("No existe el mapa %s" % tmx_path)
		return map
	var root: XmlElement = parse_xml(FileAccess.get_file_as_bytes(tmx_path), tmx_path, map.errors)
	if root == null:
		return map
	_read_map(root, tmx_path, map)
	return map


## Lee un .tmx a partir de su texto. `tmx_path` sirve para resolver las rutas relativas
## (.tsx, .tx, imágenes) y para los mensajes.
static func read_string(xml: String, tmx_path: String) -> TmxMap:
	var map: TmxMap = TmxMap.new()
	map.path = tmx_path
	var root: XmlElement = parse_xml(xml.to_utf8_buffer(), tmx_path, map.errors)
	if root != null:
		_read_map(root, tmx_path, map)
	return map


## gid sin las banderas de giro.
static func strip_flags(raw_gid: int) -> int:
	return raw_gid & GID_MASK


## Banderas de giro de Tiled → transformación de Godot (bits de la alternativa del tile).
## Tiled aplica primero el giro diagonal y luego los espejos, igual que Godot con TRANSPOSE.
static func flags_to_transform(raw_gid: int) -> int:
	var transform: int = 0
	if raw_gid & FLIP_H_FLAG:
		transform |= TileSetAtlasSource.TRANSFORM_FLIP_H
	if raw_gid & FLIP_V_FLAG:
		transform |= TileSetAtlasSource.TRANSFORM_FLIP_V
	if raw_gid & FLIP_D_FLAG:
		transform |= TileSetAtlasSource.TRANSFORM_TRANSPOSE
	return transform


## Texto CSV de <data encoding="csv"> → gids crudos (con banderas). Si el número de valores no es
## `expected`, alguno no es un entero o tiene más de 10 cifras, agrega el error y devuelve un
## arreglo vacío. El rango exacto de cada gid (0..MAX_RAW_GID) lo comprueba quien lo usa.
static func parse_csv(text: String, expected: int, label: String, errors: PackedStringArray) -> PackedInt64Array:
	var result: PackedInt64Array = PackedInt64Array()
	for token: String in text.split(",", false):
		var value: String = token.strip_edges()
		if value.is_empty():
			continue
		if not value.is_valid_int():
			errors.append("%s: valor CSV no válido \"%s\"" % [label, value])
			return PackedInt64Array()
		# Más de 10 cifras no cabe en un gid de 32 bits (y con más de 19, to_int() se satura).
		if value.lstrip("+-").lstrip("0").length() > 10:
			errors.append("%s: valor CSV fuera de rango \"%s\" (un gid va de 0 a %d)" % [label, value, MAX_RAW_GID])
			return PackedInt64Array()
		result.append(value.to_int())
	if result.size() != expected:
		errors.append("%s: el CSV tiene %d valores y el tamaño de la capa pide %d" % [label, result.size(), expected])
		return PackedInt64Array()
	return result


## Índice del tileset al que pertenece un gid (sin banderas), o -1 si no pertenece a ninguno.
static func find_tileset(tilesets: Array[TmxTileset], gid: int) -> int:
	var found: int = -1
	for i: int in tilesets.size():
		var tileset: TmxTileset = tilesets[i]
		if gid >= tileset.first_gid and (found < 0 or tileset.first_gid > tilesets[found].first_gid):
			found = i
	if found >= 0 and gid - tilesets[found].first_gid >= tilesets[found].tile_count:
		return -1
	return found


## XML → árbol de XmlElement. Devuelve null (y agrega el error) si el XML está mal formado:
## etiqueta sin cerrar, cierre que no corresponde a la última abierta, cierre sin apertura o más
## de un elemento raíz.
static func parse_xml(buffer: PackedByteArray, label: String, errors: PackedStringArray) -> XmlElement:
	var parser: XMLParser = XMLParser.new()
	var open_error: Error = parser.open_buffer(buffer)
	if open_error != OK:
		errors.append("%s: no se pudo leer el XML (%s)" % [label, error_string(open_error)])
		return null
	var root: XmlElement = null
	var stack: Array[XmlElement] = []
	while true:
		var read_error: Error = parser.read()
		if read_error == ERR_FILE_EOF:
			break
		if read_error != OK:
			errors.append("%s: XML mal formado (%s)" % [label, error_string(read_error)])
			return null
		var node_type: XMLParser.NodeType = parser.get_node_type()
		if _is_repeated_tag(parser, node_type, buffer.size()):
			continue
		match node_type:
			XMLParser.NODE_ELEMENT:
				var element: XmlElement = XmlElement.new()
				element.name = parser.get_node_name()
				for i: int in parser.get_attribute_count():
					element.attributes[parser.get_attribute_name(i)] = parser.get_attribute_value(i)
				if not stack.is_empty():
					var parent: XmlElement = stack.back()
					parent.children.append(element)
				elif root == null:
					root = element
				else:
					errors.append("%s: XML mal formado (<%s> fuera de la raíz <%s>)" % [label, element.name, root.name])
					return null
				if not parser.is_empty():
					stack.append(element)
			XMLParser.NODE_ELEMENT_END:
				var closing: String = parser.get_node_name()
				if stack.is_empty():
					errors.append("%s: XML mal formado (</%s> sin su etiqueta de apertura)" % [label, closing])
					return null
				var open_element: XmlElement = stack.back()
				if closing != open_element.name:
					errors.append("%s: XML mal formado (</%s> no cierra <%s>)" % [label, closing, open_element.name])
					return null
				stack.pop_back()
			XMLParser.NODE_TEXT, XMLParser.NODE_CDATA:
				if not stack.is_empty():
					var current: XmlElement = stack.back()
					current.text += parser.get_node_data()
	if not stack.is_empty():
		var unclosed: XmlElement = stack.back()
		errors.append("%s: XML incompleto (<%s> sin cerrar)" % [label, unclosed.name])
		return null
	if root == null:
		errors.append("%s: el XML está vacío" % label)
	return root


## true si el nodo de etiqueta actual es una repetición falsa del XMLParser de Godot (visto en
## 4.7): si al archivo le quedan exactamente 2 caracteres tras la última etiqueta, read() devuelve
## otra vez el nodo anterior (p. ej. "</layer>\n\n" da dos </layer>). La repetición "empieza" en
## esos 2 bytes finales, donde no cabe ninguna etiqueta real (la más corta, "<a>", ocupa 3), así
## que se reconoce por su posición sin mirar el nodo anterior. Si no se descartara, un </layer>
## repetido cerraría <map> en un archivo cortado y el mapa se leería sin sus últimas capas.
static func _is_repeated_tag(parser: XMLParser, node_type: XMLParser.NodeType, buffer_size: int) -> bool:
	if node_type != XMLParser.NODE_ELEMENT and node_type != XMLParser.NODE_ELEMENT_END:
		return false
	# "<nombre>" o "<nombre/>" como mínimo nombre + 2 bytes; "</nombre>", nombre + 3.
	var min_tag_bytes: int = parser.get_node_name().to_utf8_buffer().size() + (2 if node_type == XMLParser.NODE_ELEMENT else 3)
	return buffer_size - int(parser.get_node_offset()) < min_tag_bytes


## Propiedades de Tiled (<properties><property name type value/>) → Dictionary tipado.
static func read_properties(element: XmlElement) -> Dictionary[String, Variant]:
	var result: Dictionary[String, Variant] = {}
	var properties: XmlElement = element.first_child("properties")
	if properties == null:
		return result
	for property: XmlElement in properties.children_named("property"):
		var value: String = property.attr("value", property.text)
		match property.attr("type", "string"):
			"bool":
				result[property.attr("name")] = value == "true"
			"int":
				result[property.attr("name")] = value.to_int()
			"float":
				result[property.attr("name")] = value.to_float()
			_:
				result[property.attr("name")] = value
	return result


## Ruta relativa de un archivo de Tiled → ruta del proyecto, desde la carpeta de `from_file`.
static func resolve_path(from_file: String, relative: String) -> String:
	if relative.is_absolute_path():
		return relative
	return from_file.get_base_dir().path_join(relative).simplify_path()


static func _read_map(root: XmlElement, tmx_path: String, map: TmxMap) -> void:
	if root.name != "map":
		map.errors.append("%s: no es un mapa de Tiled (la raíz es <%s>, no <map>)" % [tmx_path, root.name])
		return
	var orientation: String = root.attr("orientation", "orthogonal")
	if orientation != "orthogonal":
		map.errors.append("%s: orientación \"%s\"; solo se soportan mapas ortogonales" % [tmx_path, orientation])
	if root.attr("infinite", "0") == "1":
		map.errors.append("%s: el mapa es infinito; desmarca Map → Map Properties → Infinite y dale un tamaño fijo" % tmx_path)
	map.size = Vector2i(root.attr("width").to_int(), root.attr("height").to_int())
	map.tile_size = Vector2i(root.attr("tilewidth").to_int(), root.attr("tileheight").to_int())
	if map.size.x <= 0 or map.size.y <= 0:
		map.errors.append("%s: tamaño de mapa no válido %s" % [tmx_path, map.size])
	if not map.errors.is_empty():
		return

	for element: XmlElement in root.children_named("tileset"):
		var tileset: TmxTileset = _read_tileset(element, tmx_path, map)
		if tileset != null:
			map.tilesets.append(tileset)
	if not map.errors.is_empty():
		return

	var templates: Dictionary[String, XmlElement] = {}
	for element: XmlElement in root.children:
		match element.name:
			"layer":
				_read_tile_layer(element, map)
			"objectgroup":
				_read_object_group(element, tmx_path, map, templates)
			"group":
				map.errors.append("%s: el grupo de capas \"%s\" no se soporta; saca sus capas del grupo" % [tmx_path, element.attr("name")])
			_:
				pass  # <properties>, <tileset>, <imagelayer>, <editorsettings>: no se exportan


static func _read_tileset(element: XmlElement, tmx_path: String, map: TmxMap) -> TmxTileset:
	var tileset: TmxTileset = TmxTileset.new()
	tileset.first_gid = element.attr("firstgid").to_int()
	var definition: XmlElement = element
	tileset.source = tmx_path
	if element.attributes.has("source"):
		tileset.source = resolve_path(tmx_path, element.attr("source"))
		if not FileAccess.file_exists(tileset.source):
			map.errors.append("%s: no existe el tileset %s" % [tmx_path, tileset.source])
			return null
		definition = parse_xml(FileAccess.get_file_as_bytes(tileset.source), tileset.source, map.errors)
		if definition == null:
			return null
		if definition.name != "tileset":
			map.errors.append("%s: no es un tileset de Tiled (la raíz es <%s>)" % [tileset.source, definition.name])
			return null
	tileset.name = definition.attr("name")
	tileset.columns = definition.attr("columns").to_int()
	tileset.tile_count = definition.attr("tilecount").to_int()
	tileset.tile_size = Vector2i(definition.attr("tilewidth").to_int(), definition.attr("tileheight").to_int())
	var image: XmlElement = definition.first_child("image")
	if image == null:
		map.errors.append("%s: el tileset \"%s\" no tiene una sola imagen (los de colección de imágenes no se soportan)" % [tileset.source, tileset.name])
		return null
	tileset.image = resolve_path(tileset.source, image.attr("source"))
	if tileset.first_gid <= 0 or tileset.columns <= 0 or tileset.tile_count <= 0:
		map.errors.append("%s: el tileset \"%s\" tiene firstgid, columns o tilecount no válidos" % [tileset.source, tileset.name])
		return null
	if tileset.tile_size != map.tile_size:
		map.errors.append("%s: el tileset \"%s\" usa tiles de %s y el mapa de %s" % [tileset.source, tileset.name, tileset.tile_size, map.tile_size])
		return null
	# El lector calcula las coordenadas del atlas como (id % columns, id / columns): con margen o
	# separación no cuadrarían con el TileSet de Godot (ADR 0009 §5).
	var margin: int = definition.attr("margin", "0").to_int()
	var spacing: int = definition.attr("spacing", "0").to_int()
	if margin != 0 or spacing != 0:
		map.errors.append("%s: el tileset \"%s\" tiene margin=%d y spacing=%d; el atlas va sin margen ni separación (ADR 0009 §5)" % [tileset.source, tileset.name, margin, spacing])
		return null
	var tile_offset: XmlElement = definition.first_child("tileoffset")
	if tile_offset != null and (tile_offset.attr("x", "0").to_int() != 0 or tile_offset.attr("y", "0").to_int() != 0):
		map.errors.append("%s: el tileset \"%s\" tiene <tileoffset> (%s, %s); pon Drawing Offset en 0, 0: el conversor no lo aplica" % [tileset.source, tileset.name, tile_offset.attr("x", "0"), tile_offset.attr("y", "0")])
		return null
	return tileset


static func _read_tile_layer(element: XmlElement, map: TmxMap) -> void:
	var layer: TmxTileLayer = TmxTileLayer.new()
	layer.name = element.attr("name")
	var label: String = "%s, capa %s" % [map.path, layer.name]
	var properties: Dictionary[String, Variant] = read_properties(element)
	# noExport con un tipo que no es bool: error y no se sigue leyendo la capa (no se sabe si
	# se quería exportar).
	var errors_before: int = map.errors.size()
	if _prop_bool(properties, PROP_NO_EXPORT, false, label, map.errors) or map.errors.size() > errors_before:
		return
	if not _check_layer_attributes(element, label, map.errors):
		return
	layer.z_index = _prop_int(properties, PROP_Z_INDEX, 0, label, map.errors)
	if layer.z_index < RenderingServer.CANVAS_ITEM_Z_MIN or layer.z_index > RenderingServer.CANVAS_ITEM_Z_MAX:
		map.errors.append("%s: zIndex %d fuera del rango de Godot (%d a %d)" % [label, layer.z_index, RenderingServer.CANVAS_ITEM_Z_MIN, RenderingServer.CANVAS_ITEM_Z_MAX])
		return
	layer.y_sort_enabled = _prop_bool(properties, PROP_Y_SORT, false, label, map.errors)
	var data: XmlElement = element.first_child("data")
	if data == null:
		map.errors.append("%s: la capa no tiene <data>" % label)
		return
	var encoding: String = data.attr("encoding")
	if encoding != "csv":
		map.errors.append("%s: codificación \"%s\" no soportada; guarda el mapa en CSV (Map → Map Properties → Tile Layer Format → CSV)" % [label, encoding if not encoding.is_empty() else "XML"])
		return
	var layer_size: Vector2i = Vector2i(element.attr("width", str(map.size.x)).to_int(), element.attr("height", str(map.size.y)).to_int())
	if layer_size != map.size:
		map.errors.append("%s: la capa mide %s celdas y el mapa %s; tienen que medir lo mismo (Map → Resize Map ajusta todas las capas)" % [label, layer_size, map.size])
		return
	var width: int = layer_size.x
	var gids: PackedInt64Array = parse_csv(data.text, layer_size.x * layer_size.y, label, map.errors)
	if gids.is_empty():
		return
	for i: int in gids.size():
		var raw_gid: int = gids[i]
		if raw_gid == 0:
			continue
		@warning_ignore("integer_division")
		var coords: Vector2i = Vector2i(i % width, i / width)
		if raw_gid < 0 or raw_gid > MAX_RAW_GID:
			map.errors.append("%s, celda %s: el gid %d está fuera de rango (va de 0 a %d)" % [label, coords, raw_gid, MAX_RAW_GID])
			continue
		if raw_gid & ROTATED_HEX_FLAG:
			map.errors.append("%s, celda %s: bandera de rotación hexagonal (bit 28) en un mapa ortogonal" % [label, coords])
			continue
		var cell: TmxCell = TmxCell.new()
		cell.coords = coords
		cell.gid = strip_flags(raw_gid)
		cell.transform = flags_to_transform(raw_gid)
		cell.tileset_index = find_tileset(map.tilesets, cell.gid)
		if cell.tileset_index < 0:
			map.errors.append("%s, celda %s: el gid %d no pertenece a ningún tileset del mapa" % [label, coords, cell.gid])
			continue
		var tileset: TmxTileset = map.tilesets[cell.tileset_index]
		var local_id: int = cell.gid - tileset.first_gid
		@warning_ignore("integer_division")
		cell.atlas_coords = Vector2i(local_id % tileset.columns, local_id / tileset.columns)
		layer.cells.append(cell)
	map.tile_layers.append(layer)


static func _read_object_group(element: XmlElement, tmx_path: String, map: TmxMap, templates: Dictionary[String, XmlElement]) -> void:
	var layer_name: String = element.attr("name")
	var label: String = "%s, capa de objetos %s" % [tmx_path, layer_name]
	var errors_before: int = map.errors.size()
	if _prop_bool(read_properties(element), PROP_NO_EXPORT, false, label, map.errors) or map.errors.size() > errors_before:
		return
	if not _check_layer_attributes(element, label, map.errors):
		return
	for object_element: XmlElement in element.children_named("object"):
		var object: TmxObject = TmxObject.new()
		object.id = object_element.attr("id").to_int()
		object.layer = layer_name
		object.position = Vector2(object_element.attr("x", "0").to_float(), object_element.attr("y", "0").to_float())
		object.name = object_element.attr("name")
		var is_tile_object: bool = object_element.attributes.has("gid")
		if object_element.attributes.has("template"):
			object.template = resolve_path(tmx_path, object_element.attr("template"))
			var template_object: XmlElement = _load_template(object.template, map, templates)
			if template_object == null:
				continue
			if object.name.is_empty():
				object.name = template_object.attr("name")
			is_tile_object = is_tile_object or template_object.attributes.has("gid")
			object.properties = read_properties(template_object)
		object.properties.merge(read_properties(object_element), true)
		object.res_path = str(object.properties.get(PROP_RES_PATH, ""))
		if object.res_path.is_empty():
			map.objects.append(object)
			continue
		var object_label: String = "%s, objeto %d (%s)" % [tmx_path, object.id, object.name]
		if not (object.res_path.begins_with("res://") and object.res_path.ends_with(".tscn")):
			map.errors.append("%s: resPath tiene que ser res://<archivo>.tscn y es \"%s\"" % [object_label, object.res_path])
			continue
		# En un objeto de tile, x/y es la esquina inferior izquierda del tile y no un punto: la
		# escena quedaría corrida respecto a lo que se ve en Tiled.
		if is_tile_object:
			map.errors.append("%s: es un objeto de tile (tiene gid) y su y es la esquina inferior; usa un objeto de punto (como la plantilla pothole.tx)" % object_label)
			continue
		if object_element.attr("visible", "1") == "0":
			map.errors.append("%s: el objeto está oculto (visible=0) y tiene resPath; muéstralo o bórralo" % object_label)
			continue
		map.objects.append(object)


## Atributos de <layer> y <objectgroup> que el conversor no aplica. Si no tienen su valor neutro,
## agrega el error y devuelve false. Una capa oculta es ambigua (¿no se exporta, o se ocultó un
## momento para pintar?), así que se rechaza y se pide noExport = true o mostrarla (ADR 0009 §7).
static func _check_layer_attributes(element: XmlElement, label: String, errors: PackedStringArray) -> bool:
	var ok: bool = true
	var offset: Vector2 = Vector2(element.attr("offsetx", "0").to_float(), element.attr("offsety", "0").to_float())
	if offset != Vector2.ZERO:
		errors.append("%s: la capa está desplazada (offsetx, offsety = %s); pon Offset en 0, 0: el conversor no lo aplica" % [label, offset])
		ok = false
	var parallax: Vector2 = Vector2(element.attr("parallaxx", "1").to_float(), element.attr("parallaxy", "1").to_float())
	if parallax != Vector2.ONE:
		errors.append("%s: la capa tiene paralaje (parallaxx, parallaxy = %s); pon Parallax Factor en 1, 1: el conversor no lo aplica" % [label, parallax])
		ok = false
	if element.attr("visible", "1") == "0":
		errors.append("%s: la capa está oculta (visible=0); muéstrala o, si no se debe exportar, ponle la propiedad noExport = true" % label)
		ok = false
	return ok


## Propiedad bool: `default_value` si no está. Si en Tiled tiene otro tipo (p. ej. string, que es
## el tipo por defecto al crearla), agrega el error y devuelve `default_value`.
static func _prop_bool(properties: Dictionary[String, Variant], key: String, default_value: bool, label: String, errors: PackedStringArray) -> bool:
	if not properties.has(key):
		return default_value
	var value: Variant = properties[key]
	if typeof(value) == TYPE_BOOL:
		var result: bool = value
		return result
	errors.append("%s: la propiedad %s tiene que ser de tipo bool en Tiled (es %s)" % [label, key, _tiled_type_name(value)])
	return default_value


## Propiedad int: `default_value` si no está. Acepta int y float sin decimales (2.0). Con otro
## tipo agrega el error y devuelve `default_value`.
static func _prop_int(properties: Dictionary[String, Variant], key: String, default_value: int, label: String, errors: PackedStringArray) -> int:
	if not properties.has(key):
		return default_value
	var value: Variant = properties[key]
	match typeof(value):
		TYPE_INT:
			var result: int = value
			return result
		TYPE_FLOAT:
			var number: float = value
			# 2^53: hasta ahí un float representa todos los enteros exactos.
			if is_finite(number) and number == floorf(number) and absf(number) <= 9007199254740992.0:
				return int(number)
	errors.append("%s: la propiedad %s tiene que ser de tipo int en Tiled (es %s)" % [label, key, _tiled_type_name(value)])
	return default_value


## Tipo de Tiled con el que read_properties() leyó un valor, para los mensajes.
static func _tiled_type_name(value: Variant) -> String:
	match typeof(value):
		TYPE_BOOL:
			return "bool"
		TYPE_INT:
			return "int"
		TYPE_FLOAT:
			return "float %s" % str(value)
		_:
			return "string \"%s\"" % str(value)


## El <object> de una plantilla .tx, leído una sola vez por mapa.
static func _load_template(path: String, map: TmxMap, templates: Dictionary[String, XmlElement]) -> XmlElement:
	if templates.has(path):
		return templates[path]
	if not FileAccess.file_exists(path):
		map.errors.append("%s: no existe la plantilla %s" % [map.path, path])
		templates[path] = null
		return null
	var root: XmlElement = parse_xml(FileAccess.get_file_as_bytes(path), path, map.errors)
	var object: XmlElement = root.first_child("object") if root != null and root.name == "template" else null
	if root != null and object == null:
		map.errors.append("%s: no es una plantilla de objeto de Tiled (falta <template><object>)" % path)
	templates[path] = object
	return object
