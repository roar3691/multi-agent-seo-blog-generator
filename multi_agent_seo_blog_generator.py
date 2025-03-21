# multi_agent_seo_blog_generator.py

import os  # For handling file system operations
import sys  # For system-specific parameters and functions
import subprocess  # For running pip install commands
from typing import List, Dict  # For type hints
import markdown  # For converting markdown to HTML
from bs4 import BeautifulSoup  # For parsing HTML content

# Function to dynamically install Python packages if not already installed
def install(package):
    """Installs a Python package using pip if it's not already installed."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import google.generativeai, install if missing
try:
    import google.generativeai as genai  # Google's Generative AI SDK
    from google.generativeai.types import GenerationConfig  # Configuration for content generation
except ModuleNotFoundError:
    install("google-generativeai")  # Install the package if import fails
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig

# Try to import BeautifulSoup, install if missing
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    install("beautifulsoup4==4.12.3")  # Install specific version of BeautifulSoup
    from bs4 import BeautifulSoup

# Configure Gemini API with your API key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual Gemini API key
try:
    genai.configure(api_key=GEMINI_API_KEY)  # Initialize the Gemini API client
except Exception as e:
    print(f"Failed to configure Gemini API: {e}")  # Log error and exit if configuration fails
    exit(1)

class ResearchAgent:
    """Agent responsible for researching trending HR topics."""
    def __init__(self):
        try:
            self.client = genai.GenerativeModel("gemini-1.5-flash")  # Initialize Gemini model
        except Exception as e:
            print(f"Failed to initialize ResearchAgent: {e}")  # Log initialization error
            raise
    
    def get_trending_hr_topics(self) -> Dict:
        """Fetches 5 trending HR topics for 2025 with descriptions."""
        prompt = "Research and list 5 trending HR topics in 2025 with brief descriptions"
        try:
            response = self.client.generate_content(prompt)  # Generate content using Gemini
            return {"topics": self._parse_topics(response.text)}  # Parse and return topics
        except Exception as e:
            print(f"Research failed: {e}")  # Log error if generation fails
            return {"topics": [{"title": "HR Trends in 2025", "description": "Fallback topic"}]}  # Fallback

    def _parse_topics(self, text: str) -> List[Dict]:
        """Parses the generated text into a list of topic dictionaries."""
        topics = []
        for line in text.split('\n'):  # Split text into lines
            if line.strip() and '.' in line[:3]:  # Check for numbered list format
                title = line.split('.', 1)[1].strip()  # Extract title after number
                topics.append({"title": title, "description": ""})  # Add to topics list
        return topics[:5]  # Return up to 5 topics

class ContentPlanningAgent:
    """Agent responsible for creating a structured blog outline."""
    def __init__(self):
        self.client = genai.GenerativeModel("gemini-1.5-flash")  # Initialize Gemini model
        
    def create_outline(self, topic: str) -> Dict:
        """Creates a detailed outline for a 2000-word SEO-optimized blog post."""
        prompt = f"""Create a detailed blog outline for a 2000-word SEO-optimized article about '{topic}'. 
        Include title, introduction, 4-5 main sections with 2-3 subsections each, and conclusion."""
        try:
            response = self.client.generate_content(prompt)  # Generate outline
            return {"outline": response.text}  # Return outline text
        except Exception as e:
            print(f"Planning failed: {e}")  # Log error if generation fails
            return {"outline": f"# {topic}\n\nIntroduction\n\n## Section 1\n\n### Subsection 1\n\nConclusion"}  # Fallback

class ContentGenerationAgent:
    """Agent responsible for generating the full blog content."""
    def __init__(self):
        self.client = genai.GenerativeModel("gemini-1.5-flash")  # Initialize Gemini model
        
    def generate_content(self, outline: str) -> str:
        """Generates a 2000-word blog post based on the provided outline."""
        prompt = f"""Generate a 2000-word blog post based on this outline. Use engaging tone and HR examples:
        {outline}"""
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=GenerationConfig(max_output_tokens=2500)  # Set max tokens for length
            )
            return response.text  # Return generated content
        except Exception as e:
            print(f"Content generation failed: {e}")  # Log error if generation fails
            return "Failed to generate content"  # Fallback message

class SEOOptimizationAgent:
    """Agent responsible for optimizing content for SEO."""
    def optimize_content(self, content: str, topic: str) -> Dict:
        """Optimizes blog content with keywords and meta data."""
        keywords = self._extract_keywords(topic)  # Extract keywords from topic
        optimized = content
        meta_desc = f"Explore {topic.lower()} in this comprehensive HR guide. Learn key insights and strategies."
        for keyword in keywords:  # Ensure keyword density
            if optimized.lower().count(keyword.lower()) < 5:
                optimized = optimized.replace(keyword, f"**{keyword}**", 5)  # Bold keywords
        return {
            "content": optimized,
            "meta_description": meta_desc,
            "keywords": keywords
        }
    
    def _extract_keywords(self, topic: str) -> List[str]:
        """Extracts keywords from the topic string."""
        return [word for word in topic.split() if len(word) > 3] + ["HR", "2025"]  # Basic keyword extraction

class ReviewAgent:
    """Agent responsible for proofreading and enhancing content."""
    def __init__(self):
        self.client = genai.GenerativeModel("gemini-1.5-flash")  # Initialize Gemini model
        
    def proofread(self, content: str) -> str:
        """Proofreads and improves the content for clarity and readability."""
        prompt = f"""Proofread and enhance this content. Fix grammar, improve clarity, and enhance readability:
        {content}"""
        try:
            response = self.client.generate_content(prompt)  # Generate enhanced content
            return response.text  # Return improved content
        except Exception as e:
            print(f"Review failed: {e}")  # Log error if generation fails
            return content  # Return original content as fallback

class BlogGeneratorSystem:
    """Main system coordinating all agents to generate a blog post."""
    def __init__(self):
        try:
            self.research_agent = ResearchAgent()  # Initialize all agents
            self.planning_agent = ContentPlanningAgent()
            self.content_agent = ContentGenerationAgent()
            self.seo_agent = SEOOptimizationAgent()
            self.review_agent = ReviewAgent()
        except Exception as e:
            print(f"Failed to initialize BlogGeneratorSystem: {e}")  # Log initialization error
            raise
    
    def generate_blog(self, output_dir: str = "output"):
        """Generates a complete SEO-optimized blog post."""
        print(f"Starting blog generation process...")
        os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist
        
        print("Researching trending HR topics...")
        research = self.research_agent.get_trending_hr_topics()  # Get trending topics
        selected_topic = research["topics"][0]["title"] if research["topics"] else "HR Trends in 2025"
        print(f"Selected topic: {selected_topic}")
        
        print("Creating content outline...")
        outline = self.planning_agent.create_outline(selected_topic)  # Create blog outline
        
        print("Generating blog content...")
        content = self.content_agent.generate_content(outline["outline"])  # Generate full content
        
        print("Optimizing content for SEO...")
        optimized = self.seo_agent.optimize_content(content, selected_topic)  # Optimize for SEO
        
        print("Reviewing and enhancing content...")
        final_content = self.review_agent.proofread(optimized["content"])  # Proofread content
        
        print("Saving generated content...")
        self._save_outputs(final_content, optimized, output_dir, selected_topic)  # Save outputs
        return final_content
    
    def _save_outputs(self, content: str, seo_data: Dict, output_dir: str, topic: str):
        """Saves the generated content in Markdown and HTML formats."""
        try:
            # Save as Markdown
            with open(f"{output_dir}/blog.md", "w", encoding="utf-8") as f:
                f.write(f"# {topic}\n\n{content}")
            print("Markdown file saved")
            
            # Convert to HTML and save with SEO meta tags
            html = markdown.markdown(content)
            html_full = f"""<!DOCTYPE html><html><head>
                <meta name="description" content="{seo_data['meta_description']}">
                <meta name="keywords" content="{', '.join(seo_data['keywords'])}">
                <title>{topic}</title></head><body>{html}</body></html>"""
            with open(f"{output_dir}/blog.html", "w", encoding="utf-8") as f:
                f.write(html_full)
            print("HTML file saved")
        except Exception as e:
            print(f"Failed to save outputs: {e}")  # Log error if saving fails

def main():
    """Main function to run the blog generation system."""
    try:
        system = BlogGeneratorSystem()  # Create system instance
        blog = system.generate_blog()  # Generate blog
        print("Blog generated successfully! Check the output directory.")
    except Exception as e:
        print(f"Error in blog generation: {e}")  # Log any errors during execution

if __name__ == "__main__":
    main()  # Run the main function if script is executed directly
