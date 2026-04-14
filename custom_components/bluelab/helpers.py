"""Helper functions for Bluelab integration."""

from typing import Any


def filter_non_gateway_devices(devices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Filter out gateway devices, keeping only IntelliDose units."""
    return [d for d in devices if not d.get("gateway", False)]


def get_device_display_name(device: dict[str, Any]) -> str:
    """Get display name from device label, falling back to name."""
    label = device.get("label")
    if label and label.strip():
        return label.strip()
    return device.get("name", device["id"])
