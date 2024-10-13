'use client'
import React from 'react';

const DebatePage = () => {
  const videoUrl = 'https://www.youtube.com/watch?v=rLEhL8Y4SdU';

  return (
    <div style={{ backgroundColor: 'black', minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <iframe 
        width="560" 
        height="315" 
        src={`https://www.youtube.com/embed/${getYouTubeId(videoUrl)}`} 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowFullScreen
      ></iframe>
    </div>
  );
};

function getYouTubeId(url: string) {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : null;
}

export default DebatePage;