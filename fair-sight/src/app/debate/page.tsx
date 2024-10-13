'use client'
import React from 'react';
import Image from 'next/image';

const DebatePage = () => {
  const videoUrl = 'https://www.youtube.com/watch?v=xyF60VScB-w';
  const images = [
    '/graph.png',
    '/pie_chart.png',
    '/time_line_accum.png',
    '/time_line.png',
    '/time.png'
  ];

  return (
    <div style={{ backgroundColor: 'black', minHeight: '100vh', padding: '20px' }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
        <iframe 
          width="560" 
          height="315" 
          src={`https://www.youtube.com/embed/${getYouTubeId(videoUrl)}`} 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowFullScreen
        ></iframe>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
          {images.map((image, index) => (
            <div key={index} style={{ width: '200px', height: '200px', position: 'relative' }}>
              <Image
                src={image}
                alt={`Image ${index + 1}`}
                width={200}
                height={200}
                objectFit="cover"
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

function getYouTubeId(url: string) {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : null;
}

export default DebatePage;