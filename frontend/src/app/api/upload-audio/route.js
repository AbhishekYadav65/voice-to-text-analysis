// app/api/process/route.js
// frontend/src/app/api/process/route.js
export async function POST(req) {
  try {
    const formData = await req.formData();
    const sessionKeys = ["session_1","session_2","session_3","session_4","session_5"];
    const hasSessions = sessionKeys.some(k => formData.get(k));

    const endpoint = hasSessions ? "upload-multiple-sessions" : "upload-audio";
    const backendUrl = process.env.BACKEND_URL || "http://localhost:5001";
    const targetUrl = `${backendUrl}/${endpoint}`;

    const backendResp = await fetch(targetUrl, {
      method: "POST",
      body: formData,
    });

    const text = await backendResp.text();
    const data = JSON.parse(text);
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
