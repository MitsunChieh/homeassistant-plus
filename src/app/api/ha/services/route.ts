import { NextRequest, NextResponse } from "next/server";
import { callService } from "@/lib/ha-client";

export async function POST(request: NextRequest) {
  try {
    const { domain, service, data } = await request.json();
    if (!domain || !service) {
      return NextResponse.json(
        { error: "Missing domain or service" },
        { status: 400 }
      );
    }
    const result = await callService(domain, service, data ?? {});
    return NextResponse.json(result);
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Failed to call service";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}
