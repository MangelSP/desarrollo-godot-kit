"""Uniform tool results. Every tool returns ok(...) or fail(...), never raises."""

import functools
from collections.abc import Callable
from typing import Any


def ok(summary: str, **data: Any) -> dict[str, Any]:
    return {"ok": True, "summary": summary, **data}


def fail(summary: str, **data: Any) -> dict[str, Any]:
    return {"ok": False, "summary": summary, **data}


def safe(fn: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # tools must never raise to the client
            return fail(f"{type(exc).__name__}: {exc}")

    return wrapper
