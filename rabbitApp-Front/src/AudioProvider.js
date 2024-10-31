import React, { createContext, useContext, useEffect, useRef, useState } from 'react';

const AudioContext = createContext();

export const useAudio = () => useContext(AudioContext);

export const AudioProvider = ({ children }) => {
  const audioRef = useRef(new Audio('sound.mp3'));
  const [volume, setVolume] = useState(100);
  const [isPlaying, setIsPlaying] = useState(false);

  const fadeOut = () => {
    const audio = audioRef.current;
    audio.volume = 0;
    setVolume(0);
    audio.pause();
    setIsPlaying(false);
  };

  const fadeIn = () => {
    const audio = audioRef.current;
    audio.volume = 1;
    setVolume(100);
    audio.play().catch((error) => console.error("Error playing audio:", error));
    setIsPlaying(true);
  };

  const toggleAudio = () => {
    if (isPlaying) {
      fadeOut();
    } else {
      fadeIn();
    }
  };

  useEffect(() => {
    const audio = audioRef.current;
    audio.loop = true;
    audio.volume = 1;
    
    return () => {
      audio.pause();
    };
  }, []);

  return (
    <AudioContext.Provider value={{ audio: audioRef.current, toggleAudio, volume }}>
      {children}
    </AudioContext.Provider>
  );
};
