# -*- coding: utf-8 -*-
"""Shared HTTP error handling for the THINC service layer.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

The routes coerce incoming strings into THINC enums with `_enum_from_value`,
which raises `ValueError` listing the valid values. Without a handler FastAPI
turns that into a `500 Internal Server Error`, so a client mistake looked like a
server fault and the helpful message never reached the caller. These handlers map
input problems to `422` and keep the message.
"""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

INPUT_ERROR_STATUS = 422


async def value_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Return 422 with the original message for invalid input values."""

    return JSONResponse(
        status_code=INPUT_ERROR_STATUS,
        content={"detail": str(exc), "error": "invalid_input"},
    )


def install_error_handlers(app: FastAPI) -> FastAPI:
    """Register THINC input-error handling on a FastAPI app."""

    app.add_exception_handler(ValueError, value_error_handler)
    return app
