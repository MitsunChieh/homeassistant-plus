"use client";

import useSWR, { mutate } from "swr";
import type { HAState } from "./ha-client";

const POLLING_INTERVAL = 5000;

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export function useHAStates() {
  const { data, error, isLoading } = useSWR<HAState[]>(
    "/api/ha/states",
    fetcher,
    { refreshInterval: POLLING_INTERVAL }
  );
  return { states: data, error, isLoading };
}

export interface AreaWithEntities {
  area_id: string;
  name: string;
  entity_ids: string[];
}

export function useHAAreas() {
  const { data, error, isLoading } = useSWR<AreaWithEntities[]>(
    "/api/ha/areas",
    fetcher
  );
  return { areas: data, error, isLoading };
}

export async function callHAService(
  domain: string,
  service: string,
  data: Record<string, unknown>
) {
  const res = await fetch("/api/ha/services", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ domain, service, data }),
  });
  if (!res.ok) throw new Error("Service call failed");
  mutate("/api/ha/states");
  return res.json();
}
