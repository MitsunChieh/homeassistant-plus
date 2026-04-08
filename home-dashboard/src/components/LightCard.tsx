"use client";

import { callHAService } from "@/lib/hooks";
import type { HAState } from "@/lib/ha-client";

interface LightCardProps {
  entity: HAState;
}

export function LightCard({ entity }: LightCardProps) {
  const isOn = entity.state === "on";
  const brightness = entity.attributes.brightness as number | undefined;
  const brightnessPercent =
    brightness !== undefined ? Math.round((brightness / 255) * 100) : null;
  const friendlyName =
    (entity.attributes.friendly_name as string) || entity.entity_id;

  async function handleToggle() {
    await callHAService("light", "toggle", { entity_id: entity.entity_id });
  }

  return (
    <button
      onClick={handleToggle}
      className={`flex items-center gap-3 rounded-2xl p-4 text-left transition-colors ${
        isOn
          ? "bg-amber-500/20 border border-amber-500/30"
          : "bg-gray-800/50 border border-gray-700/50"
      }`}
    >
      <div
        className={`text-2xl ${isOn ? "text-amber-400" : "text-gray-500"}`}
      >
        {isOn ? "💡" : "🔅"}
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-sm font-medium text-gray-200 truncate">
          {friendlyName}
        </div>
        <div className="text-xs text-gray-400">
          {isOn
            ? brightnessPercent !== null
              ? `On · ${brightnessPercent}%`
              : "On"
            : "Off"}
        </div>
      </div>
    </button>
  );
}
