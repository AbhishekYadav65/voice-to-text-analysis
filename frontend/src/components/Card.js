"use client";

import React, { useState, useRef, useEffect } from "react";
import { FaMicrophone, FaStop, FaUpload, FaSpinner } from "react-icons/fa";

const Card = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState("");
  const [audioBlob, setAudioBlob] = useState(null);
  const [isRecordingSupported, setIsRecordingSupported] = useState(false);
  const [isClient, setIsClient] = useState(false);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // Check if browser supports media recording after component mounts
  useEffect(() => {
    setIsClient(true);
    
    // Only check for support, don't call getUserMedia here
    const supported = typeof window !== 'undefined' && 
      typeof navigator !== 'undefined' && 
      navigator.mediaDevices && 
      navigator.mediaDevices.getUserMedia &&
      typeof MediaRecorder !== 'undefined';
    
    setIsRecordingSupported(!!supported);
  }, []);

  const startRecording = async () => {
    try {
      setError("");
      
      // Check if we're in a browser environment and have the necessary APIs
      if (typeof window === 'undefined' || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setError("Recording not supported in this browser. Please use a modern browser with microphone support.");
        return;
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setAudioBlob(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      setError("Microphone access denied. Please allow microphone access and try again.");
      console.error("Error accessing microphone:", err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processAudio = async () => {
    if (!audioBlob) {
      setError("No audio recorded. Please record audio first.");
      return;
    }

    setIsProcessing(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.wav');
      formData.append('shadow_id', `shadow_${Date.now()}`);

      const response = await fetch('http://localhost:5001/upload-audio', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.error) {
        throw new Error(result.error);
      }

      setTranscript(result.transcript || "No transcript available");
      setAnalysis(result);
      
    } catch (err) {
      setError(`Processing failed: ${err.message}. Make sure the backend is running on port 5000.`);
      console.error("Error processing audio:", err);
    } finally {
      setIsProcessing(false);
    }
  };

  const uploadFile = (event) => {
    const file = event.target.files[0];
    if (file) {
      setAudioBlob(file);
      setError("");
    }
  };

  return (
    <div className="flex flex-col items-center mt-1 px-4">
      
      {/* Main Heading */}
      <h1 className="text-4xl sm:text-5xl font-bold text-white mb-8 text-center">
        🕵️ Truth Weaver - Whispering Shadows Mystery
      </h1>

      {/* Error Display */}
      {error && (
        <div className="bg-red-600 text-white p-4 rounded-lg mb-4 max-w-2xl">
          <p className="text-center">{error}</p>
        </div>
      )}

      {/* Cards Container */}
      <div className="flex flex-col lg:flex-row justify-center items-start space-y-8 lg:space-y-0 lg:space-x-8 w-full">
        
        {/* Voice Control Card */}
        <div className="w-full sm:max-w-md lg:max-w-sm bg-gray-800 rounded-xl shadow-lg p-6 sm:p-8 flex flex-col items-center space-y-6">
          <h2 className="text-2xl sm:text-3xl font-bold text-white text-center">Voice Recording</h2>
          
          {/* Microphone Icon with Recording Animation */}
          <div className="relative">
            <FaMicrophone 
              className={`text-6xl sm:text-8xl mb-4 ${
                isRecording ? 'text-red-500 animate-pulse' : 'text-white'
              }`} 
            />
            {isRecording && (
              <div className="absolute inset-0 rounded-full border-4 border-red-500 animate-ping"></div>
            )}
          </div>

          {/* Recording Controls */}
          <div className="flex flex-col space-y-4 w-full">
            {!isRecording ? (
              <button 
                onClick={startRecording}
                disabled={!isClient || !isRecordingSupported}
                className="bg-green-600 hover:bg-green-700 disabled:bg-gray-500 text-white rounded-xl px-6 sm:px-8 py-3 sm:py-4 text-lg sm:text-xl w-full transition-all duration-300 flex items-center justify-center space-x-2"
              >
                <FaMicrophone />
                <span>{!isClient ? "Loading..." : (isRecordingSupported ? "Start Recording" : "Recording Not Supported")}</span>
              </button>
            ) : (
              <button 
                onClick={stopRecording}
                className="bg-red-600 hover:bg-red-700 text-white rounded-xl px-6 sm:px-8 py-3 sm:py-4 text-lg sm:text-xl w-full transition-all duration-300 flex items-center justify-center space-x-2"
              >
                <FaStop />
                <span>Stop Recording</span>
              </button>
            )}

            {/* File Upload */}
            <div className="w-full">
              <label className="bg-blue-600 hover:bg-blue-700 text-white rounded-xl px-6 sm:px-8 py-3 sm:py-4 text-lg sm:text-xl w-full transition-all duration-300 flex items-center justify-center space-x-2 cursor-pointer">
                <FaUpload />
                <span>Upload Audio File</span>
                <input
                  type="file"
                  accept="audio/*"
                  onChange={uploadFile}
                  className="hidden"
                />
              </label>
            </div>

            {/* Process Button */}
            <button 
              onClick={processAudio}
              disabled={!audioBlob || isProcessing}
              className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-500 text-white rounded-xl px-6 sm:px-8 py-3 sm:py-4 text-lg sm:text-xl w-full transition-all duration-300 flex items-center justify-center space-x-2"
            >
              {isProcessing ? (
                <>
                  <FaSpinner className="animate-spin" />
                  <span>Processing...</span>
                </>
              ) : (
                <span>🕵️ Analyze Truth</span>
              )}
            </button>
          </div>

          {/* Status */}
          {audioBlob && (
            <p className="text-green-400 text-sm text-center">
              ✅ Audio ready for analysis
            </p>
          )}
        </div>

        {/* Results Card */}
        <div className="w-full sm:max-w-md lg:max-w-sm bg-gray-900 rounded-xl shadow-lg p-6 sm:p-8 flex flex-col space-y-4">
          <h2 className="text-2xl sm:text-3xl font-bold text-white text-center">Analysis Results</h2>
          
          {/* Transcript */}
          <div className="w-full">
            <h3 className="text-lg font-bold text-white mb-2">📝 Transcript:</h3>
            <div className="w-full h-32 bg-gray-700 rounded-lg p-4 overflow-y-auto">
              <p className="text-white text-sm">
                {transcript || "No transcript available yet. Record or upload audio to see results."}
              </p>
            </div>
          </div>

          {/* Analysis Results */}
          {analysis && (
            <div className="w-full">
              <h3 className="text-lg font-bold text-white mb-2">🕵️ Truth Analysis:</h3>
              <div className="w-full h-40 bg-gray-700 rounded-lg p-4 overflow-y-auto">
                <div className="text-white text-sm space-y-2">
                  <p><strong>Shadow ID:</strong> {analysis.shadow_id}</p>
                  <p><strong>Programming Experience:</strong> {analysis.revealed_truth?.programming_experience}</p>
                  <p><strong>Programming Language:</strong> {analysis.revealed_truth?.programming_language}</p>
                  <p><strong>Skill Level:</strong> {analysis.revealed_truth?.skill_mastery}</p>
                  <p><strong>Leadership Claims:</strong> {analysis.revealed_truth?.leadership_claims}</p>
                  {analysis.deception_patterns?.length > 0 && (
                    <p><strong>🚨 Deception Detected:</strong> {analysis.deception_patterns.length} pattern(s) found</p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Card;
