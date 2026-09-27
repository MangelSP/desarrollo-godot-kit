extends SceneTree
## Convierte un mapa de Tiled (.tmx) en una escena con un TileMapLayer por capa de tiles, usando
## el TileSet de Godot que tiene la colisión y la navegación. Lee el .tmx directamente con
## TmxReader (tools/tmx_reader.gd): no llama a Tiled. Ver docs/adr/0009-flujo-tiled-godot.md.
##
## No se llama a mano: lo corre tools/export_maps.sh.
##   Godot --headless --path <repo> -s res://tools/tiled_to_godot.gd -- <res://origen.tmx> <res://salida.tscn> <res://tileset.tres>
##
## Qué hace:
## - Cada capa de tiles del .tmx pasa a ser un TileMapLayer con el mismo nombre y z_index.
## - Cada celda se copia (coordenadas de atlas y giros) al TileSet de Godot, buscando la fuente
##   por la ruta de la imagen del tileset. Si un tile pintado no existe en el TileSet de Godot, falla.
## - Los objetos con la propiedad resPath (propia o de su plantilla .tx) se instancian bajo Objects.
## - Falla si una celda tiene colisión y navegación a la vez (un edificio sobre una calle), si se
##   pintó un tile de solo referencia (type = "pothole"), si faltan las capas Ground o Buildings o
##   si un nombre de capa de tiles se repite, es "Objects" o no vale como nombre de nodo.
## - Si falla, no escribe nada: la escena anterior queda intacta. Si no, escribe en un temporal
##   junto a la salida y lo renombra al final.
## - Conserva el UID de la escena de salida si ya existía, para no romper a quien la instancia.

## Se precarga en vez de usar el class_name: con -s la caché de clases globales puede no estar al día.
const Tmx := preload("res://tools/tmx_reader.gd")

const OBJECTS_NODE: StringName = &"Objects"
## Capas de tiles que architecture.md §1.2 y el envoltorio dan por hechas.
const REQUIRED_LAYERS: PackedStringArray = ["Ground", "Buildings"]
## Capa de datos personalizada del TileSet de Godot con el tipo de cada tile.
const TYPE_DATA_LAYER: String = "type"
## Tipos de tile que están en el atlas solo como referencia visual y no se pintan (ADR 0009 §5).
## Valor: con qué se reemplaza.
const REFERENCE_ONLY_TYPES: Dictionary[String, String] = {"pothole": "usa la plantilla pothole.tx"}
## ResourceSaver elige el formato por la extensión, así que el temporal tiene que acabar en .tscn.
const TMP_SUFFIX: String = ".tmp.tscn"

var _errors: PackedStringArray = PackedStringArray()


func _initialize() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	if args.size() < 3:
		printerr("Uso: -- <res://origen.tmx> <res://salida.tscn> <res://tileset.tres>")
		quit(2)
		return
	var tmx_path: String = ProjectSettings.localize_path(args[0])
	var out_path: String = ProjectSettings.localize_path(args[1])
	var tileset_path: String = ProjectSettings.localize_path(args[2])

	var map: Tmx.TmxMap = Tmx.read(tmx_path)
	for message: String in map.errors:
		_fail(message)
	var tile_set: TileSet = ResourceLoader.load(tileset_path, "TileSet") as TileSet
	if tile_set == null:
		_fail("No se pudo cargar el TileSet: %s" % tileset_path)
	if not _errors.is_empty():
		_finish()
		return

	var out_root: Node2D = _convert(map, tile_set, out_path.get_file().get_basename())
	out_root.editor_description = "GENERADO por tools/export_maps.sh desde %s. No se edita a mano: se edita el .tmx en Tiled y se re-exporta." % tmx_path
	if _errors.is_empty():
		_check_required_layers(out_root)
		_check_reference_tiles(out_root)
		_check_collision_vs_navigation(out_root)
	if _errors.is_empty():
		_save(out_root, out_path)
	out_root.free()
	_finish()


func _convert(map: Tmx.TmxMap, tile_set: TileSet, root_name: String) -> Node2D:
	var out_root: Node2D = Node2D.new()
	out_root.name = root_name
	if map.tile_size != tile_set.tile_size:
		_fail("Tamaño de tile distinto: el .tmx usa %s y el TileSet de Godot %s" % [map.tile_size, tile_set.tile_size])
		return out_root
	_copy_layers(map, tile_set, out_root)
	var objects: Node2D = _create_objects(map)
	if objects != null:
		out_root.add_child(objects)
		objects.owner = out_root
		for child: Node in objects.get_children():
			child.owner = out_root
	return out_root


func _copy_layers(map: Tmx.TmxMap, tile_set: TileSet, out_root: Node2D) -> void:
	_check_layer_names(map)
	var source_ids: PackedInt32Array = _map_sources(map, tile_set)
	if not _errors.is_empty():
		return
	for tmx_layer: Tmx.TmxTileLayer in map.tile_layers:
		var layer: TileMapLayer = TileMapLayer.new()
		layer.name = tmx_layer.name
		layer.z_index = tmx_layer.z_index
		layer.y_sort_enabled = tmx_layer.y_sort_enabled
		layer.tile_set = tile_set
		for cell: Tmx.TmxCell in tmx_layer.cells:
			var source_id: int = source_ids[cell.tileset_index]
			var atlas_source: TileSetAtlasSource = tile_set.get_source(source_id) as TileSetAtlasSource
			if not atlas_source.has_tile(cell.atlas_coords) or not atlas_source.has_alternative_tile(cell.atlas_coords, 0):
				_fail("Capa %s, celda %s: el tile %s (gid %d) no existe en el TileSet de Godot" % [layer.name, cell.coords, cell.atlas_coords, cell.gid])
				continue
			# Tiled no tiene alternativas propias: la alternativa de Godot es 0 + los bits de giro.
			layer.set_cell(cell.coords, source_id, cell.atlas_coords, cell.transform)
		out_root.add_child(layer)
		layer.owner = out_root


## Los nombres de las capas de tiles pasan tal cual a nombres de nodo: si dos se repiten, si uno
## choca con el nodo de los objetos o si tiene caracteres que Godot no admite en un nombre de nodo,
## Godot los renombraría en silencio (Ground2, Ground_1…) y las rutas de §1.2 se romperían.
func _check_layer_names(map: Tmx.TmxMap) -> void:
	var seen: Dictionary[String, bool] = {}
	for tmx_layer: Tmx.TmxTileLayer in map.tile_layers:
		var layer_name: String = tmx_layer.name
		if layer_name.is_empty():
			_fail("Hay una capa de tiles sin nombre; ponle uno en Tiled")
		elif layer_name.validate_node_name() != layer_name:
			_fail("La capa de tiles \"%s\" tiene caracteres que Godot no admite en un nombre de nodo (. : @ / \" %%); renómbrala en Tiled" % layer_name)
		elif layer_name == String(OBJECTS_NODE):
			_fail("La capa de tiles \"%s\" usa el nombre reservado para el nodo de los objetos; renómbrala en Tiled" % layer_name)
		elif seen.has(layer_name):
			_fail("Hay dos capas de tiles llamadas \"%s\"; los nombres tienen que ser únicos (pasan a ser nombres de nodo)" % layer_name)
		seen[layer_name] = true


## Tileset de Tiled (por índice) → fuente de Godot, emparejadas por la ruta de la imagen del atlas.
func _map_sources(map: Tmx.TmxMap, tile_set: TileSet) -> PackedInt32Array:
	var by_texture: Dictionary[String, int] = {}
	for i: int in tile_set.get_source_count():
		var id: int = tile_set.get_source_id(i)
		var atlas: TileSetAtlasSource = tile_set.get_source(id) as TileSetAtlasSource
		if atlas != null and atlas.texture != null:
			by_texture[atlas.texture.resource_path] = id
	var result: PackedInt32Array = PackedInt32Array()
	for tileset: Tmx.TmxTileset in map.tilesets:
		if by_texture.has(tileset.image):
			result.append(by_texture[tileset.image])
		else:
			result.append(-1)
			_fail("La imagen %s del tileset \"%s\" (%s) no está en ninguna fuente del TileSet de Godot" % [tileset.image, tileset.name, tileset.source])
	return result


## Una instancia limpia de la escena de resPath por objeto, con nombres estables por orden:
## Pothole1, Pothole2… (con plantillas, Tiled repite el nombre en todos los objetos).
func _create_objects(map: Tmx.TmxMap) -> Node2D:
	var objects: Node2D = null
	var counters: Dictionary[String, int] = {}
	for tmx_object: Tmx.TmxObject in map.objects:
		if tmx_object.res_path.is_empty():
			continue  # sin resPath: nota o guía en Tiled, no se exporta
		var label: String = "Objeto %d (%s) de la capa %s" % [tmx_object.id, tmx_object.name, tmx_object.layer]
		var scene: PackedScene = ResourceLoader.load(tmx_object.res_path, "PackedScene") as PackedScene
		if scene == null:
			_fail("%s: no se pudo cargar la escena %s" % [label, tmx_object.res_path])
			continue
		var node: Node = scene.instantiate(PackedScene.GEN_EDIT_STATE_INSTANCE)
		var instance: Node2D = node as Node2D
		if instance == null:
			if node != null:
				node.free()
			_fail("%s: %s no tiene raíz Node2D" % [label, tmx_object.res_path])
			continue
		instance.position = tmx_object.position
		var base_name: String = tmx_object.res_path.get_file().get_basename()
		var count: int = counters.get(base_name, 0) + 1
		counters[base_name] = count
		instance.name = "%s%d" % [base_name, count]
		if objects == null:
			objects = Node2D.new()
			objects.name = OBJECTS_NODE
		objects.add_child(instance)
	return objects


## architecture.md §1.2 y el envoltorio dependen de estos nombres: pasan tal cual desde el .tmx.
func _check_required_layers(out_root: Node2D) -> void:
	for layer_name: String in REQUIRED_LAYERS:
		if not (out_root.get_node_or_null(layer_name) is TileMapLayer):
			_fail("Falta la capa de tiles \"%s\" en el .tmx (se necesitan %s, con ese nombre exacto)" % [layer_name, ", ".join(REQUIRED_LAYERS)])


## Tiles que están en el atlas solo como referencia visual (p. ej. el hoyo): pintados no hacen
## nada, porque su comportamiento vive en una escena. Se detectan por el dato "type" del TileSet.
func _check_reference_tiles(out_root: Node2D) -> void:
	for child: Node in out_root.get_children():
		var layer: TileMapLayer = child as TileMapLayer
		if layer == null:
			continue
		if layer.tile_set.get_custom_data_layer_by_name(TYPE_DATA_LAYER) < 0:
			if not REFERENCE_ONLY_TYPES.is_empty():
				_fail("El TileSet %s no tiene la capa de datos personalizada \"%s\": sin ella no se pueden detectar los tiles de solo referencia (%s)" % [layer.tile_set.resource_path, TYPE_DATA_LAYER, ", ".join(REFERENCE_ONLY_TYPES.keys())])
				return
			continue
		for coords: Vector2i in layer.get_used_cells():
			var data: TileData = layer.get_cell_tile_data(coords)
			if data == null:
				continue
			var type: String = str(data.get_custom_data(TYPE_DATA_LAYER))
			if REFERENCE_ONLY_TYPES.has(type):
				_fail("Capa %s, celda %s: el tile \"%s\" es solo de referencia visual y no se pinta; %s" % [layer.name, coords, type, REFERENCE_ONLY_TYPES[type]])


## Reglas de la grilla (ADR 0009):
## - una celda no puede ser a la vez sólida (colisión) y transitable (navegación);
## - una celda tiene como máximo un polígono de navegación entre todas las capas: si hay dos
##   en el mismo sitio, el NavigationServer no puede unir los bordes y las rutas salen vacías.
func _check_collision_vs_navigation(out_root: Node2D) -> void:
	var solid: Dictionary[Vector2i, String] = {}
	var walkable: Dictionary[Vector2i, String] = {}
	for child: Node in out_root.get_children():
		var layer: TileMapLayer = child as TileMapLayer
		if layer == null:
			continue
		var tile_set: TileSet = layer.tile_set
		for coords: Vector2i in layer.get_used_cells():
			var data: TileData = layer.get_cell_tile_data(coords)
			if data == null:
				continue
			for p: int in tile_set.get_physics_layers_count():
				if data.get_collision_polygons_count(p) > 0:
					solid[coords] = String(layer.name)
			for n: int in tile_set.get_navigation_layers_count():
				if data.get_navigation_polygon(n) == null:
					continue
				var where: String = "%s (capa de navegación %d del TileSet)" % [layer.name, n]
				if walkable.has(coords):
					_fail("Celda %s: dos polígonos de navegación, en %s y en %s. Deja uno solo." % [coords, walkable[coords], where])
				walkable[coords] = where
	for coords: Vector2i in solid:
		if walkable.has(coords):
			_fail("Celda %s: colisión en %s y navegación en %s. Borra el suelo debajo del edificio." % [coords, solid[coords], walkable[coords]])


## Escritura atómica: todo (guardar, UID, ids estables) se hace en <Salida>.tmp.tscn y al final
## se renombra encima de la salida. Si algo falla, se borra el temporal y la salida queda intacta.
func _save(out_root: Node2D, out_path: String) -> void:
	var dir: String = ProjectSettings.globalize_path(out_path.get_base_dir())
	DirAccess.make_dir_recursive_absolute(dir)
	# Mismo UID en cada re-exportación: las escenas que instancian el mapa lo referencian por UID.
	var uid: int = _read_scene_uid(out_path)
	if uid == ResourceUID.INVALID_ID:
		uid = ResourceUID.create_id()
	var packed: PackedScene = PackedScene.new()
	var pack_error: Error = packed.pack(out_root)
	if pack_error != OK:
		_fail("No se pudo empaquetar la escena: %s" % error_string(pack_error))
		return
	var tmp_path: String = out_path.get_basename() + TMP_SUFFIX
	var save_error: Error = ResourceSaver.save(packed, tmp_path)
	if save_error != OK:
		_fail("No se pudo guardar %s: %s" % [tmp_path, error_string(save_error)])
		_remove(tmp_path)
		return
	var uid_error: Error = ResourceSaver.set_uid(tmp_path, uid)
	if uid_error != OK:
		_fail("No se pudo poner el UID %s en %s: %s" % [ResourceUID.id_to_text(uid), tmp_path, error_string(uid_error)])
		_remove(tmp_path)
		return
	if not _postprocess(tmp_path):
		_remove(tmp_path)
		return
	var rename_error: Error = DirAccess.rename_absolute(ProjectSettings.globalize_path(tmp_path), ProjectSettings.globalize_path(out_path))
	if rename_error != OK:
		_fail("No se pudo renombrar %s a %s: %s" % [tmp_path, out_path, error_string(rename_error)])
		_remove(tmp_path)
		return
	print("OK %s" % out_path)


func _remove(path: String) -> void:
	var absolute: String = ProjectSettings.globalize_path(path)
	if FileAccess.file_exists(absolute):
		DirAccess.remove_absolute(absolute)


## Lee el UID de la cabecera del .tscn (fuera del editor la caché de UIDs no conoce el archivo).
func _read_scene_uid(path: String) -> int:
	if not FileAccess.file_exists(path):
		return ResourceUID.INVALID_ID
	var header: String = FileAccess.get_file_as_string(path).get_slice("\n", 0)
	var regex: RegEx = RegEx.create_from_string("uid=\"(uid://[0-9a-z]+)\"")
	var found: RegExMatch = regex.search(header)
	return ResourceUID.text_to_id(found.get_string(1)) if found != null else ResourceUID.INVALID_ID


## Retoca el texto guardado para que exportar dos veces el mismo .tmx dé un archivo idéntico
## (sin ruido en git):
## - Godot 4.6+ guarda un unique_id aleatorio por nodo: se reemplaza por un hash de la ruta del nodo.
## - Fuera del editor, ResourceSaver escribe los ext_resource sin uid=: se agrega el UID del
##   archivo referenciado (estable, sale de su propia cabecera), para que la referencia sobreviva
##   si alguien mueve el TileSet o Pothole.tscn.
func _postprocess(path: String) -> bool:
	if not FileAccess.file_exists(path):
		_fail("No existe %s después de guardarlo" % path)
		return false
	var lines: PackedStringArray = FileAccess.get_file_as_string(path).split("\n")
	var node_regex: RegEx = RegEx.create_from_string("^\\[node name=\"([^\"]+)\"(?:.*? parent=\"([^\"]*)\")?")
	var id_regex: RegEx = RegEx.create_from_string("unique_id=\\d+")
	var ext_regex: RegEx = RegEx.create_from_string("^\\[ext_resource (type=\"[^\"]+\") (path=\"([^\"]+)\".*)$")
	var used: Dictionary[int, bool] = {}
	for i: int in lines.size():
		var ext_match: RegExMatch = ext_regex.search(lines[i])
		if ext_match != null:
			var ext_uid: int = ResourceLoader.get_resource_uid(ext_match.get_string(3))
			if ext_uid != ResourceUID.INVALID_ID:
				lines[i] = "[ext_resource %s uid=\"%s\" %s" % [ext_match.get_string(1), ResourceUID.id_to_text(ext_uid), ext_match.get_string(2)]
			continue
		var node_match: RegExMatch = node_regex.search(lines[i])
		if node_match == null or id_regex.search(lines[i]) == null:
			continue
		var node_path: String = node_match.get_string(2) + "/" + node_match.get_string(1)
		var id: int = maxi(node_path.hash() & 0x7FFFFFFF, 1)
		while used.has(id):
			id += 1
		used[id] = true
		lines[i] = id_regex.sub(lines[i], "unique_id=%d" % id)
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		_fail("No se pudo abrir %s para escribir: %s" % [path, error_string(FileAccess.get_open_error())])
		return false
	file.store_string("\n".join(lines))
	file.close()
	return true


func _fail(message: String) -> void:
	_errors.append(message)
	printerr("ERROR: " + message)


func _finish() -> void:
	quit(0 if _errors.is_empty() else 1)
