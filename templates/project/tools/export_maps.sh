#!/usr/bin/env bash
# Regenera las escenas de mapa desde los .tmx de Tiled, sin abrir ninguna GUI y sin llamar a Tiled:
# el conversor lee el .tmx directamente (tools/tmx_reader.gd). Tiled solo se usa como editor.
# Decisión y detalles: docs/adr/0009-flujo-tiled-godot.md
#
# Uso (desde cualquier carpeta):
#   tools/export_maps.sh                                 # todos los scenes/world/tiled/*.tmx
#   tools/export_maps.sh scenes/world/tiled/level.tmx    # solo ese mapa
#
# Por cada <nombre>.tmx escribe scenes/world/generated/<Nombre>Map.tscn (PascalCase + "Map").
# Esa escena es GENERADA: no se edita a mano. Lo que el .tmx no resuelve va en la escena
# envoltorio (scenes/world/<Nombre>.tscn), que la instancia.
#
# El .tmx tiene que estar guardado con las capas en CSV (lo normal en Tiled:
# Map → Map Properties → Tile Layer Format → CSV).
#
# Variables opcionales: GODOT (ejecutable), TILESET (res:// del TileSet de Godot), OUT_DIR (carpeta
# de salida; tiene que empezar por res:// y no llevar ..), TIMEOUT_S (segundos máximos por llamada
# a Godot) y KILL_AFTER_S (segundos de gracia entre SIGTERM y SIGKILL). Los valores por defecto son
# los de esta máquina y del ADR 0009.
#
# Si un mapa falla (el conversor lo rechaza), su escena anterior queda intacta, se sigue con los
# demás y el script sale con código 1.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GODOT="${GODOT:-/Applications/Godot_mono.app/Contents/MacOS/Godot}"
TILESET="${TILESET:-res://scenes/world/visual/tileset/tiles.tres}"
OUT_DIR="${OUT_DIR:-res://scenes/world/generated}"
TIMEOUT_S="${TIMEOUT_S:-120}"
KILL_AFTER_S="${KILL_AFTER_S:-5}"

# stderr original: el aviso de interrupción tiene que verse aunque llegue durante --import, que
# redirige su salida a un log.
exec 3>&2

# Proceso en curso y su vigilante, para no dejar huérfanos si se interrumpe el script.
child_pid=""
watcher_pid=""
tmp=""

# Termina un proceso y sus hijos directos: SIGTERM y, si sigue vivo después de KILL_AFTER_S
# segundos, SIGKILL.
stop_process() {
	local pid="$1"
	pkill -TERM -P "$pid" 2>/dev/null || true
	kill -TERM "$pid" 2>/dev/null || return 0
	local waited=0
	while kill -0 "$pid" 2>/dev/null && [[ $waited -lt $KILL_AFTER_S ]]; do
		sleep 1
		waited=$((waited + 1))
	done
	if kill -0 "$pid" 2>/dev/null; then
		pkill -KILL -P "$pid" 2>/dev/null || true
		kill -KILL "$pid" 2>/dev/null || true
	fi
}

# Corre un comando con límite de tiempo sin depender del `timeout` de GNU (no viene en macOS).
# Si el conversor tuviera un error de ejecución antes de llamar a quit(), Godot se quedaría
# esperando para siempre; así se corta (SIGTERM y, si no basta, SIGKILL) y cuenta como fallo
# (código 124).
run_with_timeout() {
	local secs="$1"; shift
	# El marcador va dentro de $tmp: si el script se corta, cleanup() lo borra con la carpeta.
	local marker
	marker="$(mktemp "${tmp:?}/timeout.XXXXXX")"
	rm -f "$marker"
	"$@" &
	child_pid=$!
	( sleep "$secs"
	  if kill -0 "$child_pid" 2>/dev/null; then
		: >"$marker"
		stop_process "$child_pid"
	  fi ) 2>/dev/null &
	watcher_pid=$!
	local rc=0
	wait "$child_pid" 2>/dev/null || rc=$?
	pkill -P "$watcher_pid" 2>/dev/null || true
	kill "$watcher_pid" 2>/dev/null || true
	wait "$watcher_pid" 2>/dev/null || true
	child_pid=""
	watcher_pid=""
	if [[ -e "$marker" ]]; then
		rm -f "$marker"
		echo "ERROR: $(basename "$1") pasó de ${secs} s y se detuvo (¿error de ejecución antes de quit()?)" >&2
		return 124
	fi
	return $rc
}

cleanup() {
	[[ -n "$tmp" ]] && rm -rf "$tmp"
	return 0
}

# Ctrl+C o SIGTERM: detiene Godot y el vigilante antes de salir.
on_signal() {
	local code="$1"
	trap - INT TERM
	if [[ -n "$watcher_pid" ]]; then
		pkill -P "$watcher_pid" 2>/dev/null || true
		kill "$watcher_pid" 2>/dev/null || true
	fi
	[[ -n "$child_pid" ]] && stop_process "$child_pid"
	echo "Interrumpido; la escena que se estaba generando queda como estaba" >&3
	exit "$code"
}

trap cleanup EXIT
trap 'on_signal 130' INT
trap 'on_signal 143' TERM

[[ -x "$GODOT" ]] || { echo "ERROR: no encuentro $GODOT (define GODOT)" >&2; exit 2; }

# OUT_DIR tiene que ser una carpeta del proyecto: fuera de res:// (p. ej. user://) la escena sale
# sin uid= y el editor deja un .tmp.tscn.uidren suelto, aunque el conversor diga OK.
case "$OUT_DIR" in
	res://*) ;;
	*) echo "ERROR: OUT_DIR tiene que empezar por res:// y es \"$OUT_DIR\"" >&2; exit 2 ;;
esac
case "/${OUT_DIR#res://}/" in
	*/../*) echo "ERROR: OUT_DIR no puede salir del proyecto con .. (\"$OUT_DIR\")" >&2; exit 2 ;;
esac

maps=()
if [[ $# -gt 0 ]]; then
	for arg in "$@"; do maps+=("$(cd "$(dirname "$arg")" && pwd)/$(basename "$arg")"); done
else
	shopt -s nullglob
	maps=("$ROOT"/scenes/world/tiled/*.tmx)
	shopt -u nullglob
fi
[[ ${#maps[@]} -gt 0 ]] || { echo "No hay .tmx que exportar en scenes/world/tiled/" >&2; exit 0; }

tmp="$(mktemp -d)"

# Temporales de una conversión interrumpida (el conversor escribe <Mapa>Map.tmp.tscn y lo renombra).
# Se borran antes de --import para que el editor no los registre ni les cree un .uid.
out_fs="$ROOT/${OUT_DIR#res://}"
if [[ -d "$out_fs" ]]; then
	find "$out_fs" -maxdepth 1 -name '*.tmp.tscn' -type f -print -delete | sed 's/^/Borrado temporal viejo: /' >&2
fi

# Asegura que el PNG del tileset esté importado (en un clon nuevo no existe .godot/).
if ! run_with_timeout "$TIMEOUT_S" "$GODOT" --headless --path "$ROOT" --import >"$tmp/import.log" 2>&1; then
	cat "$tmp/import.log" >&2
	echo "ERROR: falló la importación del proyecto" >&2
	exit 1
fi

status=0
for tmx in "${maps[@]}"; do
	case "$tmx" in
		"$ROOT"/*) ;;
		*) echo "ERROR: $tmx está fuera del proyecto; el mapa, el .tsx y el PNG tienen que estar dentro de res://" >&2; status=1; continue ;;
	esac
	name="$(basename "$tmx" .tmx)"
	pascal="$(awk -F_ '{ for (i = 1; i <= NF; i++) printf "%s%s", toupper(substr($i, 1, 1)), substr($i, 2) }' <<<"$name")"
	out="$OUT_DIR/${pascal}Map.tscn"
	source_res="res://${tmx#"$ROOT"/}"

	echo "== $source_res -> $out"
	if ! run_with_timeout "$TIMEOUT_S" "$GODOT" --headless --path "$ROOT" -s res://tools/tiled_to_godot.gd -- "$source_res" "$out" "$TILESET"; then
		echo "ERROR: no se generó $out; la escena anterior queda como estaba" >&2
		status=1
	fi
done
exit $status
