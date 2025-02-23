import React, { useState, useEffect } from 'react';
import AnimatedCircle from './AnimatedCircle';

type SpeakingState = {
    is_speaking: string
    timestamp: number
}

async function* streamingFetch(url: RequestInfo, init?: RequestInit): AsyncGenerator<string> {
  const response = await fetch(url, init);
  if (!response.body) return; // Exit if no stream is available
  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  
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

export const Breathing = () => {
  const [isBreathing, setIsBreathing] = useState(false);

  useEffect(() => {
    let isCancelled = false;

    (async () => {
      try {
        // Replace 'your-endpoint' with the actual URL that streams data
        const stream = streamingFetch('http://localhost:8000/speaking_state_data_stream');
        for await (const chunk of stream) { 
          if (isCancelled) break;

          const regex = /data:\s*(\{.*\})/;
          const match = chunk.match(regex);

          if (!match || !match[1]) throw new Error("match not found for JSON parse")

          const state: SpeakingState = JSON.parse(match[1]);
          setIsBreathing(state.is_speaking.toLowerCase() === "true");
        }
      } catch (error) {
        console.error('Error while streaming:', error);
      }
    })();

    return () => {
      isCancelled = true;
    };
  }, []);
    return <AnimatedCircle active={isBreathing} />
}