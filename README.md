# Multi-Agent SEO Blog Generator

This repository contains a Python-based multi-agent system that generates a high-quality, SEO-optimized blog post (approximately 2000 words) on a trending HR-related topic, built as part of the Junior Python Developer - AI/LLM Assessment.

## System Architecture
The system is composed of five specialized agents:
- **Research Agent**: Identifies trending HR topics for 2025 by searching Google and scraping websites, with a fallback to the Gemini API if web scraping fails.
- **Content Planning Agent**: Creates a structured outline with a title, introduction, main sections, subsections, and conclusion using the Gemini API.
- **Content Generation Agent**: Writes a comprehensive 2000-word blog post based on the outline using the Gemini API.
- **SEO Optimization Agent**: Enhances the content with keywords and meta tags for better search engine visibility.
- **Review Agent**: Proofreads and improves the content for grammar, clarity, and readability using the Gemini API.

## Agent Workflow
1. **Research**: Fetches trending HR topics from Google Search and scrapes websites, falling back to Gemini API if needed.
2. **Planning**: Generates a detailed blog outline.
3. **Generation**: Produces the full blog content.
4. **SEO Optimization**: Applies SEO best practices.
5. **Review**: Enhances and finalizes the content.

## Tools and Frameworks Used
- **Python 3.9+**: Core programming language.
- **Google Generative AI (Gemini) SDK**: For content generation and enhancement (version 0.7.2).
- **Markdown**: For converting text to HTML (version 3.5.2).
- **BeautifulSoup**: For parsing HTML content from scraped websites (version 4.12.3).
- **Requests**: For making HTTP requests to Google Search and websites (version 2.31.0).

## Repository Structure
```
multi-agent-seo-blog-generator/
├── multi_agent_seo_blog_generator.py  # Main source code (well-commented)
├── requirements.txt                   # Dependencies list
├── README.md                          # This documentation
├── blog.md                            # Final blog post in Markdown format
├── blog.html                          # Final blog post in HTML format
└── .gitignore                         # Git ignore file
```

## Installation
Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/roar3691/multi-agent-seo-blog-generator.git
   cd multi-agent-seo-blog-generator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   The `requirements.txt` file contains:
   ```
   google-generativeai==0.7.2
   markdown==3.5.2
   beautifulsoup4==4.12.3
   requests==2.31.0
   ```

3. **Set Up API Keys**:
   - **Gemini API Key**: Replace `GEMINI_API_KEY` in `multi_agent_seo_blog_generator.py` with your actual key, or set it as an environment variable:
     ```bash
     export GEMINI_API_KEY="your-actual-gemini-api-key"
     ```
   - **Google Search API**: The code uses `GOOGLE_API_KEY` and `SEARCH_ENGINE_ID` for web scraping. Ensure these are valid (see "Additional Setup for Google Search" below).

## Execution
Run the script to generate the blog:
```bash
python multi_agent_seo_blog_generator.py
```
- Outputs will be saved as `blog.md` (Markdown) and `blog.html` (HTML) in the root directory.

## Deliverables
This repository includes all required deliverables:
- **Complete Source Code**: `multi_agent_seo_blog_generator.py` - Well-commented Python script implementing the multi-agent system (see below).
- **Requirements File**: `requirements.txt` - Lists all necessary Python dependencies.
- **Setup and Usage Instructions**: Provided in this README under "Installation" and "Execution" sections.
- **Final Blog Post**: 
  - `blog.md` - The generated blog in Markdown format.
  - `blog.html` - The generated blog in HTML format with SEO meta tags.
- **README Documentation**: This file explaining system architecture, agent workflow, tools, and setup steps.

## Source Code
Below is the complete, well-commented source code included in `multi_agent_seo_blog_generator.py`:

```python
# multi_agent_seo_blog_generator.py

import os  # For handling file system operations
import sys  # For system-specific parameters and functions
import subprocess  # For running pip install commands
from typing import List, Dict  # For type hints
import markdown  # For converting markdown to HTML
import requests  # For making HTTP requests to Google Search and websites
from bs4 import BeautifulSoup  # For parsing HTML content from websites

# Function to dynamically install Python packages if not already installed
def install(package):
    """Installs a Python package using pip if it's not already installed."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import google.generativeai, install if missing
try:
    import google.generativeai as genai  # Google's Generative AI SDK
    from google.generativeai.types import GenerationConfig  # Configuration for content generation
except ModuleNotFoundError:
    install("google-generativeai")
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig

# Try to import requests, install if missing
try:
    import requests
except ModuleNotFoundError:
    install("requests")
    import requests

# Try to import BeautifulSoup, install if missing
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    install("beautifulsoup4==4.12.3")
    from bs4 import BeautifulSoup

# Configure APIs
GEMINI_API_KEY = "AIzaSyBEh3tg2B2yaLUnayD660ZyiBNfOIITb6A"  # Your Gemini API key
GOOGLE_API_KEY = "AIzaSyC_CcvkVLouD1oOmX0iLnFv8gtzyPMbtps"  # Your Google Custom Search API key
SEARCH_ENGINE_ID = "e6da2fcb52c994349"  # Your Search Engine ID

try:
    genai.configure(api_key=GEMINI_API_KEY)  # Initialize the Gemini API client
except Exception as e:
    print(f"Failed to configure Gemini API: {e}")
    exit(1)

class ResearchAgent:
    """Agent responsible for researching trending HR topics via Google Search and web scraping."""
    def __init__(self):
        try:
            self.client = genai.GenerativeModel("gemini-1.5-flash")  # Initialize Gemini model
        except Exception as e:
            print(f"Failed to initialize ResearchAgent: {e}")
            raise
    
    def get_trending_hr_topics(self) -> Dict:
        """Fetches trending HR topics by searching Google and scraping websites."""
        urls = self._google_search_hr_topics()  # Get URLs from Google Search
        topics = []
        for url in urls[:5]:  # Limit to 5 websites for efficiency
            scraped_data = self._scrape_website(url)
            if scraped_data["title"]:
                topics.append({"title": scraped_data["title"], "description": scraped_data["content"][:100]})
        
        if not topics:  # Fallback to Gemini if no topics are scraped
            print("No topics found from web scraping, falling back to Gemini API...")
            prompt = "Research and list 5 trending HR topics in 2025 with brief descriptions"
            try:
                response = self.client.generate_content(prompt)
                return {"topics": self._parse_topics(response.text)}
            except Exception as e:
                print(f"Gemini fallback failed: {e}")
                return {"topics": [{"title": "HR Trends in 2025", "description": "Fallback topic"}]}

        return {"topics": topics[:5]}

    def _google_search_hr_topics(self) -> List[str]:
        """Uses Google Custom Search API to find HR-related websites."""
        query = "trending HR topics 2025"  # Broad query to fetch relevant pages
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query,
            "num": 10,  # Number of results per request
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "items" not in data:
                print(f"No results found. Response: {data}")
                return []
            urls = [item["link"] for item in data.get("items", [])]
            print(f"Fetched {len(urls)} URLs from Google Search: {urls}")
            return urls
        except requests.exceptions.RequestException as e:
            print(f"Google search failed: {e}")
            return []

    def _scrape_website(self, url: str) -> Dict:
        """Scrapes a website for title and content using BeautifulSoup."""
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            for tag in soup(["script", "style", "nav", "footer"]):  # Remove unwanted tags
                tag.decompose()
            
            title = soup.title.string if soup.title else url.split("/")[-1].replace("-", " ")
            content = " ".join(p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True))
            print(f"Scraped {url}: {len(content)} characters")
            return {"title": title, "content": content[:2000]}
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return {"title": "", "content": ""}

    def _parse_topics(self, text: str) -> List[Dict]:
        """Parses Gemini-generated text into a list of topic dictionaries."""
        topics = []
        for line in text.split('\n'):
            if line.strip() and '.' in line[:3]:
                title = line.split('.', 1)[1].strip()
                topics.append({"title": title, "description": ""})
        return topics[:5]

class ContentPlanningAgent:
    """Agent responsible for creating a structured blog outline."""
    def __init__(self):
        self.client = genai.GenerativeModel("gemini-1.5-flash")
        
    def create_outline(self, topic: str) -> Dict:
        """Creates a detailed outline for a 2000-word SEO-optimized blog post."""
        prompt = f"""Create a detailed blog outline for a 2000-word SEO-optimized article about '{topic}'. 
        Include title, introduction, 4-5 main sections with 2-3 subsections each, and conclusion."""
        try:
            response = self.client.generate_content(prompt)
            return {"outline": response.text}
        except Exception as e:
            print(f"Planning failed: {e}")
            return {"outline": f"# {topic}\n\nIntroduction\n\n## Section 1\n\n### Subsection 1\n\nConclusion"}

class ContentGenerationAgent:
    """Agent responsible for generating the full blog content."""
    def __init__(self):
        self.client = genai.GenerativeModel("gemini-1.5-flash")
        
    def generate_content(self, outline: str) -> str:
        """Generates a 2000-word blog post based on the provided outline."""
        prompt = f"""Generate a 2000-word blog post based on this outline. Use engaging tone and HR examples:
        {outline}"""
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=GenerationConfig(max_output_tokens=2500)
            )
            return response.text
        except Exception as e:
            print(f"Content generation failed: {e}")
            return "Failed to generate content"

class SEOOptimizationAgent:
    """Agent responsible for optimizing content for SEO."""
    def optimize_content(self, content: str, topic: str) -> Dict:
        """Optimizes blog content with keywords and meta data."""
        keywords = self._extract_keywords(topic)
        optimized = content
        meta_desc = f"Explore {topic.lower()} in this comprehensive HR guide. Learn key insights and strategies."
        for keyword in keywords:
            if optimized.lower().count(keyword.lower()) < 5:
                optimized = optimized.replace(keyword, f"**{keyword}**", 5)
        return {
            "content": optimized,
            "meta_description": meta_desc,
            "keywords": keywords
        }
    
    def _extract_keywords(self, topic: str) -> List[str]:
        """Extracts keywords from the topic string."""
        return [word for word in topic.split() if len(word) > 3] + ["HR", "2025"]

class ReviewAgent:
    """Agent responsible for proofreading and enhancing content."""
    def __init__(self):
        self.client = genai.GenerativeModel("gemini-1.5-flash")
        
    def proofread(self, content: str) -> str:
        """Proofreads and improves the content for clarity and readability."""
        prompt = f"""Proofread and enhance this content. Fix grammar, improve clarity, and enhance readability:
        {content}"""
        try:
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Review failed: {e}")
            return content

class BlogGeneratorSystem:
    """Main system coordinating all agents to generate a blog post."""
    def __init__(self):
        try:
            self.research_agent = ResearchAgent()
            self.planning_agent = ContentPlanningAgent()
            self.content_agent = ContentGenerationAgent()
            self.seo_agent = SEOOptimizationAgent()
            self.review_agent = ReviewAgent()
        except Exception as e:
            print(f"Failed to initialize BlogGeneratorSystem: {e}")
            raise
    
    def generate_blog(self, output_dir: str = "output"):
        """Generates a complete SEO-optimized blog post."""
        print(f"Starting blog generation process...")
        os.makedirs(output_dir, exist_ok=True)
        
        print("Researching trending HR topics...")
        research = self.research_agent.get_trending_hr_topics()
        selected_topic = research["topics"][0]["title"] if research["topics"] else "HR Trends in 2025"
        print(f"Selected topic: {selected_topic}")
        
        print("Creating content outline...")
        outline = self.planning_agent.create_outline(selected_topic)
        
        print("Generating blog content...")
        content = self.content_agent.generate_content(outline["outline"])
        
        print("Optimizing content for SEO...")
        optimized = self.seo_agent.optimize_content(content, selected_topic)
        
        print("Reviewing and enhancing content...")
        final_content = self.review_agent.proofread(optimized["content"])
        
        print("Saving generated content...")
        self._save_outputs(final_content, optimized, output_dir, selected_topic)
        return final_content
    
    def _save_outputs(self, content: str, seo_data: Dict, output_dir: str, topic: str):
        """Saves the generated content in Markdown and HTML formats."""
        try:
            with open(f"{output_dir}/blog.md", "w", encoding="utf-8") as f:
                f.write(f"# {topic}\n\n{content}")
            print("Markdown file saved")
            
            html = markdown.markdown(content)
            html_full = f"""<!DOCTYPE html><html><head>
                <meta name="description" content="{seo_data['meta_description']}">
                <meta name="keywords" content="{', '.join(seo_data['keywords'])}">
                <title>{topic}</title></head><body>{html}</body></html>"""
            with open(f"{output_dir}/blog.html", "w", encoding="utf-8") as f:
                f.write(html_full)
            print("HTML file saved")
        except Exception as e:
            print(f"Failed to save outputs: {e}")

def main():
    """Main function to run the blog generation system."""
    try:
        system = BlogGeneratorSystem()
        blog = system.generate_blog()
        print("Blog generated successfully! Check the output directory.")
    except Exception as e:
        print(f"Error in blog generation: {e}")

if __name__ == "__main__":
    main()
```

## Notes
- The output files are `blog.html` and `blog.md`, containing the SEO-optimized blog post in HTML and Markdown formats respectively.
- The system uses dynamic package installation to ensure dependencies are met.
- Generates approximately 2000-word blog posts.
- Includes error handling for API calls and file operations, with a fallback to Gemini API if Google Search/web scraping fails.
- Outputs are SEO-optimized with keywords and meta tags.
- Progress is logged to the console during execution.

