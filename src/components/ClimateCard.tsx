"use client";

import { callHAService } from "@/lib/hooks";
import type { HAState } from "@/lib/ha-client";

interface ClimateCardProps {
  entity: HAState;
}

const HVAC_MODES = ["off", "cool", "heat", "auto"] as const;

const MODE_LABELS: Record<string, string> = {
  off: "Off",
  cool: "Cool",
  heat: "Heat",
  auto: "Auto",
  dry: "Dry",
  fan_only: "Fan",
};

export function ClimateCard({ entity }: ClimateCardProps) {
  const friendlyName =
    (entity.attributes.friendly_name as string) || entity.entity_id;
  const currentTemp = entity.attributes.current_temperature as
    | number
    | undefined;
  const targetTemp = entity.attributes.temperature as number | undefined;
  const hvacMode = entity.state;
  const isOff = hvacMode === "off";

  async function handleSetTemp(delta: number) {
    if (targetTemp === undefined) return;
    await callHAService("climate", "set_temperature", {
      entity_id: entity.entity_id,
      temperature: targetTemp + delta,
    });
  }

  async function handleSetMode(mode: string) {
    await callHAService("climate", "set_hvac_mode", {
      entity_id: entity.entity_id,
      hvac_mode: mode,
    });
  }

  return (
    <div
      className={`rounded-2xl p-4 ${
        isOff
          ? "bg-gray-800/50 border border-gray-700/50"
          : "bg-sky-500/20 border border-sky-500/30"
      }`}
    >
      <div className="flex items-center gap-3 mb-3">
        <div className="text-2xl">{isOff ? "❄️" : "🌀"}</div>
        <div className="flex-1 min-w-0">
          <div className="text-sm font-medium text-gray-200 truncate">
            {friendlyName}
          </div>
          <div className="text-xs text-gray-400">
            {currentTemp !== undefined ? `${currentTemp}°C` : "--"}
          </div>
        </div>
        {targetTemp !== undefined && !isOff && (
          <div className="text-xl font-semibold text-gray-200">
            {targetTemp}°
          </div>
        )}
      </div>

      {!isOff && targetTemp !== undefined && (
        <div className="flex items-center justify-center gap-4 mb-3">
          <button
            onClick={() => handleSetTemp(-1)}
            className="w-10 h-10 rounded-full bg-gray-700/50 text-gray-200 text-lg font-bold hover:bg-gray-600/50 transition-colors"
          >
            −
          </button>
          <span className="text-2xl font-bold text-gray-100 w-16 text-center">
            {targetTemp}°
          </span>
          <button
            onClick={() => handleSetTemp(1)}
            className="w-10 h-10 rounded-full bg-gray-700/50 text-gray-200 text-lg font-bold hover:bg-gray-600/50 transition-colors"
          >
            +
          </button>
        </div>
      )}

      <div className="flex gap-1.5">
        {HVAC_MODES.map((mode) => (
          <button
            key={mode}
            onClick={() => handleSetMode(mode)}
            className={`flex-1 py-1.5 text-xs rounded-lg transition-colors ${
              hvacMode === mode
                ? "bg-sky-500 text-white"
                : "bg-gray-700/50 text-gray-400 hover:bg-gray-600/50"
            }`}
          >
            {MODE_LABELS[mode] ?? mode}
          </button>
        ))}
      </div>
    </div>
  );
}
