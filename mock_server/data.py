"""
Mock data for all tool endpoints.
All data is fictional — no external API calls are made.
"""

WEATHER_DATA = {
    "london": {"city": "London", "temperature": 11, "unit": "C", "condition": "Rainy", "humidity": 85},
    "new york": {"city": "New York", "temperature": 18, "unit": "C", "condition": "Partly Cloudy", "humidity": 62},
    "tokyo": {"city": "Tokyo", "temperature": 22, "unit": "C", "condition": "Clear", "humidity": 55},
    "paris": {"city": "Paris", "temperature": 16, "unit": "C", "condition": "Sunny", "humidity": 60},
    "sydney": {"city": "Sydney", "temperature": 25, "unit": "C", "condition": "Clear", "humidity": 50},
    "berlin": {"city": "Berlin", "temperature": 12, "unit": "C", "condition": "Cloudy", "humidity": 72},
}

NEWS_DATA = {
    "technology": [
        {"headline": "New AI model surpasses benchmarks in reasoning tasks", "source": "Tech Daily"},
        {"headline": "Quantum computing milestone reached by research team", "source": "Science Now"},
        {"headline": "Open-source LLM released with 70 billion parameters", "source": "Dev Weekly"},
    ],
    "science": [
        {"headline": "Researchers discover new deep-sea species off Pacific coast", "source": "Nature Brief"},
        {"headline": "Mars rover finds evidence of ancient water channels", "source": "Space Report"},
        {"headline": "Breakthrough in fusion energy announced by research lab", "source": "Energy Today"},
    ],
    "world": [
        {"headline": "Global climate summit concludes with new emissions targets", "source": "World News"},
        {"headline": "International space station crew completes record EVA", "source": "Space Daily"},
        {"headline": "New trade agreement signed between major economies", "source": "Financial Times"},
    ],
    "default": [
        {"headline": "Scientists develop new method for carbon capture", "source": "Green Report"},
        {"headline": "Global internet traffic reaches new record high", "source": "Net Monitor"},
        {"headline": "Researchers publish findings on urban heat island effect", "source": "Climate Watch"},
    ],
}

SEARCH_DATA = {
    "python": [
        {"title": "Python 3.13 Released — Key New Features", "snippet": "Python 3.13 introduces a new interactive interpreter and free-threaded mode for improved concurrency."},
        {"title": "Why Python Dominates Data Science", "snippet": "Python's ecosystem of libraries makes it the language of choice for machine learning and data analysis."},
        {"title": "Python vs Rust: When to Use Which", "snippet": "Rust offers memory safety and performance; Python offers speed of development and library breadth."},
    ],
    "ai": [
        {"title": "The State of AI in 2026", "snippet": "Large language models continue to advance rapidly, with agentic systems emerging as the next frontier."},
        {"title": "Open Source AI Is Catching Up to Proprietary Models", "snippet": "Models like Llama 3 and Mistral are now competitive with closed-source alternatives on many benchmarks."},
        {"title": "AI Agents: From Chatbots to Autonomous Systems", "snippet": "Modern AI agents can plan, use tools, and recover from errors — a significant leap beyond simple chatbots."},
    ],
    "matrix": [
        {"title": "The Matrix (1999) — Film Analysis", "snippet": "The Wachowskis' landmark film explores themes of simulation, control, and the nature of reality."},
        {"title": "Agent Smith: The Perfect Villain", "snippet": "Hugo Weaving's portrayal of Agent Smith remains one of cinema's most iconic antagonists."},
        {"title": "Matrix Resurrections and the Legacy of the Franchise", "snippet": "The fourth Matrix film revisits themes of choice, identity, and the cost of returning to the system."},
    ],
    "default": [
        {"title": "Search result: No specific data available", "snippet": "The mock server does not have specific data for this query. In production, a real search API would be used."},
        {"title": "Related topics found", "snippet": "Try searching for: python, ai, or matrix for richer mock results."},
        {"title": "Mock search engine v1.0", "snippet": "This is a simulated search backend. All results are fictional and for demonstration purposes only."},
    ],
}

CURRENCY_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 154.50,
    "AUD": 1.53,
    "CAD": 1.37,
    "CHF": 0.90,
    "CNY": 7.24,
    "SEK": 10.42,
    "NOK": 10.55,
}