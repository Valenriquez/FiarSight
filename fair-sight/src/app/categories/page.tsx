'use client';

import { useState, useEffect } from 'react';

// Define a type for the news article
type NewsArticle = {
  title: string;
  description: string;
  url: string;
  source: string;
  published_at: string;
};

const api_request = async () => {
  const response = await fetch('http://api.mediastack.com/v1/news?access_key=5672e8681b1ddac87c9b239d4feb58ff&keywords=government&countries=us');
  const data = await response.json();
  return data.data as NewsArticle[];
};

const News = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const data = await api_request();
        setArticles(data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch news');
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="max-w-4xl mx-auto p-5">
      <h1 className="text-3xl font-bold mb-5">The Daily Herald</h1>
      <h2 className="text-2xl font-semibold mb-4">News</h2>
      <div className="space-y-4">
        {articles.map((article, index) => (
          <div key={index} className="border p-4 rounded-lg">
            <h3 className="text-xl font-semibold">{article.title}</h3>
            <p className="text-gray-600">{article.description}</p>
            <p className="text-sm text-gray-500 mt-2">
              Source: {article.source} | Published: {new Date(article.published_at).toLocaleDateString()}
            </p>
            <a href={article.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
              Read more
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default News;