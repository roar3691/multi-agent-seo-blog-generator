# Multi-Agent SEO Blog Generator

This repository contains a Python-based multi-agent system that generates a high-quality, SEO-optimized blog post (approximately 2000 words) on a trending HR-related topic, built as part of the Junior Python Developer - AI/LLM Assessment (Task-id: #8921416).

## System Architecture
The system is composed of five specialized agents:
- **Research Agent**: Identifies trending HR topics for 2025 using the Gemini API.
- **Content Planning Agent**: Creates a structured outline with a title, introduction, main sections, subsections, and conclusion.
- **Content Generation Agent**: Writes a comprehensive 2000-word blog post based on the outline.
- **SEO Optimization Agent**: Enhances the content with keywords and meta tags for better search engine visibility.
- **Review Agent**: Proofreads and improves the content for grammar, clarity, and readability.

## Agent Workflow
1. **Research**: Fetches trending HR topics.
2. **Planning**: Generates a detailed blog outline.
3. **Generation**: Produces the full blog content.
4. **SEO Optimization**: Applies SEO best practices.
5. **Review**: Enhances and finalizes the content.

## Tools and Frameworks Used
- **Python 3.9+**: Core programming language.
- **Google Generative AI (Gemini) SDK**: For content generation and enhancement (version 0.7.2).
- **Markdown**: For converting text to HTML (version 3.5.2).
- **BeautifulSoup**: For HTML parsing and manipulation (version 4.12.3).

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/roar3691/multi-agent-seo-blog-generator.git
   cd multi-agent-seo-blog-generator


