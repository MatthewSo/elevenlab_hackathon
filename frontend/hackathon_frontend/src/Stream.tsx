import React, { useState, useEffect } from 'react';

// Asynchronous generator function that yields decoded data chunks
async function* streamingFetch(url: RequestInfo, init?: RequestInit): AsyncGenerator<string> {
  const response = await fetch(url, init);
  console.log(response)
  if (!response.body) return; // Exit if no stream is available
  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  
  console.log(reader, decoder)
  
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      yield decoder.decode(value);
    }
  } catch (error) {
    console.error('Streaming error:', error);
  } finally {
    reader.releaseLock();
  }
}

const StreamComponent: React.FC = () => {
  const [data, setData] = useState<string>('');

  useEffect(() => {
    let isCancelled = false;

    (async () => {
      try {
        // Replace 'your-endpoint' with the actual URL that streams data
        const stream = streamingFetch('http://localhost:8000/spoken_language_data_stream');
        let accumulatedData = '';
        for await (const chunk of stream) { 
          if (isCancelled) break;
          accumulatedData += chunk;
          setData(accumulatedData);
        }
      } catch (error) {
        console.error('Error while streaming:', error);
      }
    })();

    return () => {
      isCancelled = true;
    };
  }, []);

  return (
    <div>
      <h1>Streamed Data</h1>
      <pre>{data}</pre>
    </div>
  );
};

export default StreamComponent;