extends SceneTree
## Bundled with godot-kit-mcp. Loads a scene, waits N frames and saves the window as PNG.
##   godot --path <project> --windowed --resolution WxH -s screenshot.gd -- <res://scene.tscn> <frames> <out.png>
## Needs a display: on headless Linux run it under xvfb-run.

var _frames_left: int = 0
var _out: String = ""


func _initialize() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	if args.size() < 3:
		printerr("usage: -- <res://scene.tscn> <frames> <out.png>")
		quit(2)
		return
	var packed: PackedScene = load(args[0]) as PackedScene
	if packed == null:
		printerr("cannot load scene: ", args[0])
		quit(1)
		return
	_frames_left = maxi(1, args[1].to_int())
	_out = args[2]
	root.add_child(packed.instantiate())


func _process(_delta: float) -> bool:
	if _out.is_empty():
		return false
	_frames_left -= 1
	if _frames_left > 0:
		return false
	var img: Image = root.get_texture().get_image()
	img.convert(Image.FORMAT_RGBA8)
	var err: Error = img.save_png(_out)
	if err != OK:
		printerr("cannot save png: ", error_string(err))
		quit(1)
	else:
		quit(0)
	_out = ""
	return false
