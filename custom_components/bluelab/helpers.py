"""Helper functions for Bluelab integration."""

from typing import Any


def classify_devices(
    devices: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Classify devices into gateways and IntelliDose units.

    Returns (gateways, intellidose) tuple.
    """
    gateways = []
    intellidose = []
    for d in devices:
        if d.get("gateway", False):
            gateways.append(d)
        else:
            intellidose.append(d)
    return gateways, intellidose


def get_device_display_name(device: dict[str, Any]) -> str:
    """Get display name for a device.

    For gateways: uses additionalInfo.deviceIdentifier, falls back to name.
    For IntelliDose: uses label, falls back to name.
    """
    if device.get("gateway", False):
        additional = device.get("additionalInfo", {})
        identifier = additional.get("deviceIdentifier")
        if identifier and identifier.strip():
            return identifier.strip()
        return device.get("name", device["id"])

    label = device.get("label")
    if label and label.strip():
        return label.strip()
    return device.get("name", device["id"])
