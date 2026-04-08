const HA_BASE_URL = process.env.HA_BASE_URL || "http://homeassistant:8123";
const HA_TOKEN = process.env.HA_TOKEN;

function getHeaders(): HeadersInit {
  if (!HA_TOKEN) throw new Error("HA_TOKEN environment variable is not set");
  return {
    Authorization: `Bearer ${HA_TOKEN}`,
    "Content-Type": "application/json",
  };
}

function getBaseUrl(): string {
  if (!HA_BASE_URL)
    throw new Error("HA_BASE_URL environment variable is not set");
  return HA_BASE_URL.replace(/\/+$/, "");
}

export interface HAState {
  entity_id: string;
  state: string;
  attributes: Record<string, unknown>;
  last_changed: string;
  last_updated: string;
}

export interface HAArea {
  area_id: string;
  name: string;
  picture: string | null;
}

export interface HAEntityRegistryEntry {
  entity_id: string;
  area_id: string | null;
  device_id: string | null;
  name: string | null;
}

export interface HADeviceRegistryEntry {
  id: string;
  area_id: string | null;
  name: string | null;
}

export async function getStates(): Promise<HAState[]> {
  const res = await fetch(`${getBaseUrl()}/api/states`, {
    headers: getHeaders(),
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`HA API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function getState(entityId: string): Promise<HAState> {
  const res = await fetch(`${getBaseUrl()}/api/states/${entityId}`, {
    headers: getHeaders(),
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`HA API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function callService(
  domain: string,
  service: string,
  data: Record<string, unknown>
): Promise<HAState[]> {
  const res = await fetch(
    `${getBaseUrl()}/api/services/${domain}/${service}`,
    {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify(data),
    }
  );
  if (!res.ok) throw new Error(`HA API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function getAreas(): Promise<HAArea[]> {
  const res = await fetch(`${getBaseUrl()}/api/template`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      template: "{{ areas() | list | to_json }}",
    }),
  });
  if (!res.ok) throw new Error(`HA API error: ${res.status} ${res.statusText}`);
  const areaIds: string[] = JSON.parse(await res.text());

  const areas: HAArea[] = [];
  for (const areaId of areaIds) {
    const nameRes = await fetch(`${getBaseUrl()}/api/template`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify({
        template: `{{ area_name('${areaId}') }}`,
      }),
    });
    if (nameRes.ok) {
      areas.push({
        area_id: areaId,
        name: await nameRes.text(),
        picture: null,
      });
    }
  }
  return areas;
}

export async function getAreaEntities(areaId: string): Promise<string[]> {
  const res = await fetch(`${getBaseUrl()}/api/template`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      template: `{{ area_entities('${areaId}') | list | to_json }}`,
    }),
  });
  if (!res.ok) throw new Error(`HA API error: ${res.status} ${res.statusText}`);
  return JSON.parse(await res.text());
}
