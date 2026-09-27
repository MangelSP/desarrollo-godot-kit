"""MCP entry point. Tool logic lives in the other modules; this file only wires it."""

from mcp.server.mcpserver import MCPServer

server = MCPServer(
    "godot-kit",
    instructions=(
        "Tools for building 2D Godot 4 games with GDScript, Tiled and Pixelorama: "
        "run Godot headless, test with GUT, take screenshots, convert Tiled maps, "
        "make greybox art, track the MVP plan, scaffold projects and search game-dev knowledge."
    ),
)


def main() -> None:
    server.run()
