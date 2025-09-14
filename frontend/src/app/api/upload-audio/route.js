// app/api/process/route.js
export const runtime = "edge"; // optional

export async function POST(req) {
  try {
    const formData = await req.formData();
    const sessionKeys = ["session_1","session_2","session_3","session_4","session_5"];
    const hasSessions = sessionKeys.some(k => formData.get(k) !== null);

    const target = hasSessions ? "upload-multiple-sessions" : "upload-audio";
    const backendUrl = `http://localhost:5001/${target}`;

    const backendResp = await fetch(backendUrl, {
      method: "POST",
      body: formData,
    });

    const text = await backendResp.text();
    if (!backendResp.ok) {
      return new Response(JSON.stringify({ error: `Backend error ${backendResp.status}`, raw: text }), {
        status: 502,
        headers: { "Content-Type": "application/json" }
      });
    }
    try {
      const data = JSON.parse(text);
      return new Response(JSON.stringify(data), { status: 200, headers: { "Content-Type": "application/json" } });
    } catch (e) {
      return new Response(JSON.stringify({ raw: text }), { status: 200, headers: { "Content-Type": "application/json" } });
    }
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { "Content-Type": "application/json" } });
  }
}
