import { useState, useEffect } from 'react';

const AnimatedCircle = ({ active }: { active: boolean }) => {
  const [showAnimated, setShowAnimated] = useState(active);

  useEffect(() => {
      setShowAnimated(active);
  }, [active]);

  return (
    <div className="circle-wrapper">
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
          background-color: #79BF6A;
          transition: opacity 0.5s ease-in-out;
        }

        .circle-static {
          transform: scale(0.7);
          opacity: ${showAnimated ? 0 : 1};
        }

        .circle-animated {
          opacity: ${showAnimated ? 1 : 0};
          animation: pulse 1.5s ease-in-out infinite;
        }

        @keyframes pulse {
          0%, 100% {
            transform: scale(0.7);
          }
          50% {
            transform: scale(1);
          }
        }
      `}</style>
      
      <div className="circle circle-static" />
      <div className="circle circle-animated" />
    </div>
  );
};

export default AnimatedCircle;
