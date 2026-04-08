"use client";

import { useHAStates, useHAAreas } from "@/lib/hooks";
import { AreaSection } from "./AreaSection";
import { LightCard } from "./LightCard";
import { TemperatureCard } from "./TemperatureCard";
import { HumidityCard } from "./HumidityCard";
import { ClimateCard } from "./ClimateCard";
import type { HAState } from "@/lib/ha-client";

const SUPPORTED_DOMAINS = ["light", "sensor", "climate"];

function isSupportedEntity(entity: HAState): boolean {
  const domain = entity.entity_id.split(".")[0];
  if (domain === "sensor") {
    const deviceClass = entity.attributes.device_class as string | undefined;
    return deviceClass === "temperature" || deviceClass === "humidity";
  }
  return SUPPORTED_DOMAINS.includes(domain);
}

function EntityCard({ entity }: { entity: HAState }) {
  const domain = entity.entity_id.split(".")[0];

  if (domain === "light") return <LightCard entity={entity} />;
  if (domain === "climate") return <ClimateCard entity={entity} />;
  if (domain === "sensor") {
    const deviceClass = entity.attributes.device_class as string | undefined;
    if (deviceClass === "temperature") return <TemperatureCard entity={entity} />;
    if (deviceClass === "humidity") return <HumidityCard entity={entity} />;
  }
  return null;
}

export function Dashboard() {
  const { states, error: statesError, isLoading: statesLoading } = useHAStates();
  const { areas, error: areasError, isLoading: areasLoading } = useHAAreas();

  if (statesLoading || areasLoading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="text-gray-400 text-lg">Loading...</div>
      </div>
    );
  }

  if (statesError || areasError) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="text-red-400 text-lg">
          Failed to connect to Home Assistant
        </div>
      </div>
    );
  }

  if (!states || !areas) return null;

  const supportedEntities = states.filter(isSupportedEntity);
  const entityMap = new Map(supportedEntities.map((e) => [e.entity_id, e]));

  const assignedEntityIds = new Set<string>();
  const areaGroups = areas
    .map((area) => {
      const entities = area.entity_ids
        .filter((id) => entityMap.has(id))
        .map((id) => {
          assignedEntityIds.add(id);
          return entityMap.get(id)!;
        });
      return { ...area, entities };
    })
    .filter((area) => area.entities.length > 0);

  const unassignedEntities = supportedEntities.filter(
    (e) => !assignedEntityIds.has(e.entity_id)
  );

  return (
    <div>
      {areaGroups.map((area) => (
        <AreaSection key={area.area_id} name={area.name}>
          {area.entities.map((entity) => (
            <EntityCard key={entity.entity_id} entity={entity} />
          ))}
        </AreaSection>
      ))}
      {unassignedEntities.length > 0 && (
        <AreaSection name="Other">
          {unassignedEntities.map((entity) => (
            <EntityCard key={entity.entity_id} entity={entity} />
          ))}
        </AreaSection>
      )}
    </div>
  );
}
