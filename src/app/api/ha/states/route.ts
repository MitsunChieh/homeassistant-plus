import { NextResponse } from "next/server";
import { getStates } from "@/lib/ha-client";

export async function GET() {
  try {
    const states = await getStates();
    return NextResponse.json(states);
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Failed to fetch states";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}
