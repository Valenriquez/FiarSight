'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { GoogleGenerativeAI } from "@google/generative-ai";

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

// Add new types for profile options
type AgeRange = '18-24' | '25-34' | '35-44' | '45-54' | '55+';
type SexualOrientation = 'Straight' | 'Gay' | 'Lesbian' | 'Bisexual' | 'Other';
type Race = 'White' | 'Black' | 'Asian' | 'Hispanic' | 'Other';

interface Profile {
  ageRange: AgeRange | '';
  sexualOrientation: SexualOrientation | '';
  race: Race | '';
}

interface NavbarProps {
  categories: string[];
  activeCategory: string;
  setCategory: (category: string) => void;
  profile: Profile;
  setProfile: (profile: Profile) => void;
}

const Navbar: React.FC<NavbarProps> = ({ categories, activeCategory, setCategory, profile, setProfile }) => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  const updateProfile = (key: keyof Profile, value: string) => {
    setProfile({ ...profile, [key]: value });
  };

  
  return (
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
            <div className="relative ml-4">
              <button
                onClick={() => setIsProfileOpen(!isProfileOpen)}
                className="text-white hover:text-gray-300 px-3 py-2 rounded-md text-sm font-medium"
              >
                Profile
              </button>
              {isProfileOpen && (
                <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg py-2 z-10 border border-gray-200">
                  <div className="px-4 py-2 border-b border-gray-200">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Age Range</label>
                    <select
                      value={profile.ageRange}
                      onChange={(e) => updateProfile('ageRange', e.target.value)}
                      className="block w-full px-3 py-2 text-sm text-gray-700 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Select Age Range</option>
                      <option value="18-24">18-24</option>
                      <option value="25-34">25-34</option>
                      <option value="35-44">35-44</option>
                      <option value="45-54">45-54</option>
                      <option value="55+">55+</option>
                    </select>
                  </div>
                  <div className="px-4 py-2 border-b border-gray-200">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Sexual Orientation</label>
                    <select
                      value={profile.sexualOrientation}
                      onChange={(e) => updateProfile('sexualOrientation', e.target.value)}
                      className="block w-full px-3 py-2 text-sm text-gray-700 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Select Sexual Orientation</option>
                      <option value="Straight">Straight</option>
                      <option value="Gay">Gay</option>
                      <option value="Lesbian">Lesbian</option>
                      <option value="Bisexual">Bisexual</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div className="px-4 py-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Race</label>
                    <select
                      value={profile.race}
                      onChange={(e) => updateProfile('race', e.target.value)}
                      className="block w-full px-3 py-2 text-sm text-gray-700 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Select Race</option>
                      <option value="White">White</option>
                      <option value="Black">Black</option>
                      <option value="Asian">Asian</option>
                      <option value="Hispanic">Hispanic</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};


const News = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [category, setCategory] = useState('');
  const [profile, setProfile] = useState<Profile>({
    ageRange: '',
    sexualOrientation: '',
    race: '',
  });
  const [generatedContent, setGeneratedContent] = useState<string>('');

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

  useEffect(() => {
    // Load profile from localStorage
    const savedProfile = localStorage.getItem('userProfile');
    if (savedProfile) {
      setProfile(JSON.parse(savedProfile));
    }
  }, []);

  useEffect(() => {
    // Save profile to localStorage whenever it changes
    localStorage.setItem('userProfile', JSON.stringify(profile));
  }, [profile]);

  const generatePrompt = async () => {
    if (!profile.ageRange || !profile.sexualOrientation || !profile.race) {
      alert("Please complete your profile before generating content.");
      return;
    }

    const prompt = `Given a news article about ${category || 'general topics'}, provide a brief analysis or perspective that might be particularly relevant or interesting to a ${profile.ageRange} year old ${profile.race} individual who identifies as ${profile.sexualOrientation}. Consider how this demographic might view or be affected by the news, but avoid stereotypes or overgeneralizations.`;

    const genAI = new GoogleGenerativeAI("AIzaSyDc4y4ur6rUTE-hEXnSvre7R7rdYnulrJk");
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });

    try {
      const result = await model.generateContent(prompt);
      const response = await result.response;
      const text = response.text();
      setGeneratedContent(text);
    } catch (error) {
      console.error('Error generating content:', error);
      setGeneratedContent('An error occurred while generating content.');
    }
  };

  return (
    <> 
    <Navbar categories={categories} activeCategory={category} setCategory={setCategory} profile={profile} setProfile={setProfile} />
    <div className="max-w-7xl mx-auto p-5">      
      {loading && <div className="text-center text-2xl">Loading...</div>}
      {error && <div className="text-center text-2xl text-red-500">{error}</div>}
      
      {!loading && !error && (
        <>
          <div className="mb-8">
            <button 
              onClick={generatePrompt}
              className="mb-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-full transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
            >
              Generate Personalized Insight
            </button>
            {generatedContent && (
              <div className="bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden">
                <div className="bg-blue-600 text-white px-6 py-4">
                  <h2 className="text-xl font-semibold">Personalized Insight</h2>
                </div>
                <div className="px-6 py-4">
                  <p className="text-gray-800 leading-relaxed">{generatedContent}</p>
                </div>
              </div>
            )}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article, index) => (
              <NewsCard key={index} article={article} />
            ))}
          </div>
        </>
      )}
    </div>
    </>
  );
};

export default News;
