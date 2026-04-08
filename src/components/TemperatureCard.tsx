"use client";

import type { HAState } from "@/lib/ha-client";

interface TemperatureCardProps {
  entity: HAState;
}

export function TemperatureCard({ entity }: TemperatureCardProps) {
  const friendlyName =
    (entity.attributes.friendly_name as string) || entity.entity_id;
  const isUnavailable =
    entity.state === "unavailable" || entity.state === "unknown";

  return (
    <div className="flex items-center gap-3 rounded-2xl p-4 bg-gray-800/50 border border-gray-700/50">
      <div className="text-2xl">🌡️</div>
      <div className="flex-1 min-w-0">
        <div className="text-sm font-medium text-gray-200 truncate">
          {friendlyName}
        </div>
        <div className="text-xs text-gray-400">
          {isUnavailable ? (
            <span className="text-gray-500">Unavailable</span>
          ) : (
            `${entity.state}°C`
          )}
        </div>
      </div>
      {!isUnavailable && (
        <div className="text-xl font-semibold text-gray-200">
          {entity.state}°
        </div>
      )}
    </div>
  );
}
