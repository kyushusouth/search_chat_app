"use client";

import { useState } from "react";

interface SearchResult {
  id: number;
  name: string;
  description: string;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSearched(true);
    setLoading(true);

    if (!query) {
      setResults([]);
      setLoading(false);
      return;
    }

    try {
      const apiUrl = `/api/search`;
      const response = await fetch(`${apiUrl}?q=${query}`);
      const data = await response.json();
      setResults(data.hits);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <h1 className="text-4xl font-bold mb-8">商品検索 (Next.js)</h1>
      <form onSubmit={handleSearch} className="w-full max-w-lg mb-8">
        <div className="flex items-center border-b border-teal-500 py-2">
          <input
            className="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="キーワードを入力 (例: カメラ)"
            aria-label="Search query"
          />
          <button
            className="flex-shrink-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 text-sm border-4 text-white py-1 px-2 rounded"
            type="submit"
            disabled={loading}
          >
            {loading ? "検索中..." : "検索"}
          </button>
        </div>
      </form>

      <div className="w-full max-w-lg">
        {loading && <p>読み込み中...</p>}
        {!loading && searched && results.length === 0 && (
          <p>検索結果がありません</p>
        )}
        <ul className="space-y-4">
          {results.map((item) => (
            <li key={item.id} className="p-4 border rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold">{item.name}</h3>
              <p className="text-gray-600">{item.description}</p>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
