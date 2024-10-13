'use client';

import { GoogleGenerativeAI } from "@google/generative-ai";
import { useState } from 'react';

export default function TryPage() {
  const [result, setResult] = useState('');

  async function generateContent() {
    const genAI = new GoogleGenerativeAI("AIzaSyDc4y4ur6rUTE-hEXnSvre7R7rdYnulrJk");
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });

    const prompt = "Write a story about a magic backpack.";

    try {
      const result = await model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();
      setResult(text);
    } catch (error) {
      console.error('Error generating content:', error);
      setResult('An error occurred while generating content.');
    }
  }

  return (
    <div>
      <button onClick={generateContent}>Generate Story</button>
      <p>{result}</p>
    </div>
  )
}