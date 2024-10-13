'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';

type NewsArticle = {
  title: string;
  description: string;
  url: string;
  source: string;
  category: string;
  published_at: string;
  image: string | null;
};

const ensureAbsoluteUrl = (url: string): string => {
  if (!url) return '/path/to/fallback-image.jpg'; // Replace with your fallback image path
  if (url.startsWith('//')) return `https:${url}`;
  if (url.startsWith('/')) return `https://www.wral.com${url}`;
  if (!url.startsWith('http://') && !url.startsWith('https://')) return `https://${url}`;
  return url;
};

const api_request = async (category: string = '') => {
  try {
    const response = await fetch(`http://api.mediastack.com/v1/news?access_key=5672e8681b1ddac87c9b239d4feb58ff&categories=${category}&countries=us`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log("API Response:", data);
    if (!data.data || !Array.isArray(data.data)) {
      console.error("Unexpected data structure:", data);
      return [];
    }
    return data.data as NewsArticle[];
  } catch (error) {
    console.error("Error fetching news:", error);
    throw error;
  }
};

const NewsCard = ({ article }: { article: NewsArticle }) => (
  <div className="bg-white shadow-md rounded-lg overflow-hidden">
    {article.image && (
      <div className="relative w-full h-48">
        <Image
          src={ensureAbsoluteUrl(article.image)}
          alt={article.title}
          layout="fill"
          objectFit="cover"
          className="rounded-t-lg"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = '/path/to/fallback-image.jpg'; // Replace with your fallback image path
          }}
        />
      </div>
    )}
    <div className="p-4">
      <h3 className="text-xl font-semibold mb-2 text-gray-800">{article.title}</h3>
      <p className="text-gray-600 mb-4">{article.description}</p>
      <div className="flex justify-between items-center">
        <span className="text-sm text-gray-500">{article.source}</span>
        <span className="text-sm text-gray-500">{new Date(article.published_at).toLocaleDateString()}</span>
      </div>
    </div>
    <div className="bg-gray-100 px-4 py-2">
      <a href={article.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
        Read more
      </a>
    </div>
  </div>
)

interface NavbarProps {
  categories: string[];
  activeCategory: string;
  setCategory: (category: string) => void;
}

const Navbar: React.FC<NavbarProps> = ({ categories, activeCategory, setCategory }) => (
  <nav className="bg-black shadow-md mb-8">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between h-16">
        <div className="flex items-center">
          <Link href="/">
            <span className="text-white text-xl font-bold">#FairSight</span>
          </Link>
        </div>
        <div className="flex items-center">
          <div className="flex space-x-8">
            
            {categories.map((cat) => (
              <Link key={cat} href="#" onClick={() => setCategory(cat)}>
                <span className={`${activeCategory === cat ? 'border-blue-500 text-white' : 'border-transparent text-gray-300 hover:border-gray-500 hover:text-white'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium capitalize`}>
                  {cat}
                </span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  </nav>
);

const News = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [category, setCategory] = useState('');


  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true);
        const data = await api_request(category);
        setArticles(data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch news');
        setLoading(false);
      }
    };

    fetchNews();
  }, [category]);

  const categories = ['general', 'politics', 'technology', 'business', 'entertainment'];

  return (
    <> 
    <Navbar categories={categories} activeCategory={category} setCategory={setCategory} />
    <div className="max-w-7xl mx-auto p-5">      
      {loading && <div className="text-center text-2xl">Loading...</div>}
      {error && <div className="text-center text-2xl text-red-500">{error}</div>}
      
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((article, index) => (
            <NewsCard key={index} article={article} />
          ))}
        </div>
      )}
    </div>
    </>
  );
};

export default News;
