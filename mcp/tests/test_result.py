from godot_kit_mcp.result import fail, ok, safe


def test_ok_and_fail_shape():
    assert ok("done", n=1) == {"ok": True, "summary": "done", "n": 1}
    assert fail("nope") == {"ok": False, "summary": "nope"}


def test_safe_turns_exceptions_into_fail():
    @safe
    def boom(x: int) -> dict:
        raise ValueError(f"bad {x}")

    assert boom(3) == {"ok": False, "summary": "ValueError: bad 3"}


def test_safe_keeps_signature_and_doc():
    @safe
    def tool(a: int, b: str = "x") -> dict:
        """Doc."""
        return ok("fine")

    import inspect

    assert list(inspect.signature(tool).parameters) == ["a", "b"]
    assert tool.__doc__ == "Doc."
    assert tool(1)["ok"] is True
