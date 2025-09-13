export async function POST(req) {
  try {
    const formData = await req.formData();
    const file = formData.get('file');
    
    console.log('Received file:', file?.name, 'Size:', file?.size);
    
    if (!file) {
      return Response.json({ error: 'No file provided' }, { status: 400 });
    }

    console.log('Sending to backend...');
    const backendResponse = await fetch('http://localhost:5001/upload-audio', {
      method: 'POST',
      body: formData,
    });

    console.log('Response status:', backendResponse.status);
    const rawText = await backendResponse.text();
    console.log('Raw backend response:', rawText);

    if (!backendResponse.ok) {
      throw new Error(`HTTP error! status: ${backendResponse.status}\n${rawText}`);
    }

    // Try to parse JSON if possible
    let data;
    try {
      data = JSON.parse(rawText);
    } catch (e) {
      data = { error: 'Invalid JSON from backend', raw: rawText };
    }
    return Response.json(data);
  } catch (error) {
    console.error('Error:', error);
    return Response.json({ error: error.message }, { status: 500 });
  }
}