import { useState, useEffect } from 'react';

const AnimatedCircle = ({ active, color }: { active: boolean; color: string }) => {
  const [showAnimated, setShowAnimated] = useState(active);
  const [isClicked, setIsClicked] = useState(false)

  useEffect(() => {
      setShowAnimated(active);
  }, [active]);

  const sendPostRequest = async () => {
    setIsClicked(true);
    setTimeout(() => setIsClicked(false), 1000);

    await fetch('http://localhost:8000/high_alert_explaination', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      });
  }

  return (
    <div className="circle-wrapper" onClick={sendPostRequest}>
      <style>{`
        .circle-wrapper {
          position: relative;
          width: 300px;
          height: 300px;
        }

        .circle {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border-radius: 50%;
          background-color: ${getColor(color)};
          transition: opacity 0.5s ease-in-out;
          cursor: pointer;
        }

        .circle-static {
          transform: scale(0.7);
          opacity: ${showAnimated ? 0 : 1};
          animation: ${isClicked ? 'colorChange 1s forwards' : 'none'};
        }

        .circle-animated {
          opacity: ${showAnimated ? 1 : 0};
          // animation: pulse 1.5s ease-in-out infinite;
            animation: ${isClicked ? 'colorChange 1s forwards, pulse 1.5s ease-in-out infinite' : 'pulse 1.5s ease-in-out infinite'};
        }

        @keyframes pulse {
          0%, 100% {
            transform: scale(0.7);
          }
          50% {
            transform: scale(1);
          }
        }
          @keyframes colorChange {
            0% { background-color: #a0c9ed; }
            50% { background-color:rgb(112, 177, 235); }
            100% { background-color: #a0c9ed; }
        }
      `}</style>
      
      <div className="circle circle-static" />
      <div className="circle circle-animated" />
    </div>
  );
};

export default AnimatedCircle;

const getColor = (c: string) => {
    if (c === "blue") {
        return "#a0c9ed"
    }
    return "#FF0000"
}