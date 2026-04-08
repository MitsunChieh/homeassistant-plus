import { NextResponse } from "next/server";
import { getAreas, getAreaEntities } from "@/lib/ha-client";

export interface AreaWithEntities {
  area_id: string;
  name: string;
  entity_ids: string[];
}

export async function GET() {
  try {
    const areas = await getAreas();
    const areasWithEntities: AreaWithEntities[] = await Promise.all(
      areas.map(async (area) => ({
        area_id: area.area_id,
        name: area.name,
        entity_ids: await getAreaEntities(area.area_id),
      }))
    );
    return NextResponse.json(areasWithEntities);
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Failed to fetch areas";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}
