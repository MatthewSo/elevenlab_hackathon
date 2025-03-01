import React, { useRef, useState, useEffect } from 'react';
import { Breathing } from './Breathing';
import blue_background from "../public/blue_background.jpg"

type SentenceData = {
    sentence_id: string;
    sentence_text: string;
    consequential_idx: string;
    factuality_idx: string;
    controversial_idx: string;
    confidence_idx: string;
    timestamp: number;
    speaker: string;
    alert: boolean;
    color: string;
}

// Asynchronous generator function that yields decoded data chunks
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

const StreamComponent: React.FC = () => {
  const [data, setData] = useState<SentenceData[]>([]);
  const listRef = useRef<HTMLDivElement>(null);


  useEffect(() => {
    let isCancelled = false;

    (async () => {
      try {
        // Replace 'your-endpoint' with the actual URL that streams data
        const stream = streamingFetch('http://localhost:8000/spoken_language_data_stream');
        for await (const chunk of stream) { 
          if (isCancelled) break;

          const regex = /data:\s*(\{.*\})/;
          const match = chunk.match(regex);
          if (!match || !match[1]) throw new Error("match not found for JSON parse")

          const sentence: SentenceData = JSON.parse(match[1]);
          // console.log(sentence)
          setData(prev => [...prev, sentence]);
        }
      } catch (error) {
        console.error('Error while streaming:', error);
      }
    })();

    return () => {
      isCancelled = true;
    };
  }, []);


  useEffect(() => {
    if (listRef.current) {
        listRef.current.scrollTop = listRef.current.scrollHeight ;
      }
  }, [data]); 

    return (
        <div className="flex flex-row h-screen grid-cols-2 gap-4 libre-baskerville-regular">
            <style>{`
            .divbackg {
                background-image: url(${blue_background});
                background-position: bottom;

                }
            `}</style>

            <div ref={listRef} className="divbackg hide-scrollbar bg-[#E6FFDE] rounded-3xl p-4 w-1/2 h-[90%] overflow-y-auto pb-12">
                {data.map(s => {
                        return (
                          <div className="w-full text-left" key={`${Math.random() * 100000}`}>
                            <span className="inline text-xl w-full" key={`${Math.random()  * 10000}`} style={{ backgroundColor: gethighlightColor(s.color) }}> { s.sentence_text } </span> 
                            <br />
                          </div>
                        )
                })}
            </div>
            <div className="flex items-center justify-center p-4 w-1/2">
                <Breathing />
            </div>
        </div>
    );
};

export default StreamComponent;

const gethighlightColor = (c: string) => {
    if (c === "red") {
        return "#ff7c6b" // red
    }
    if (c === "yellow") {
        return "#f8ff6b" // yellow
    }
    if (c === "green") {
      return "#89ff6b" // green
    }
}

/*
                {data.map((sd, index) => (
                    <p
                        key={sd.sentence_id}
                        className={`whitespace-normal break-words inline`}
                    >
                        {sd.sentence_text.replace(/[^\s]/g, "—")}}
                    </p>
                ))}


*/