import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get("q");

  if (!query) {
    return NextResponse.json({ hits: [] });
  }

  try {
    const backendUrl = `http://backend:8000/search?q=${query}`;

    const res = await fetch(backendUrl, {
      cache: "no-store",
    });

    if (!res.ok) {
      throw new Error("Failed to fetch data from backend");
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { message: "Internal Server Error" },
      { status: 500 }
    );
  }
}
