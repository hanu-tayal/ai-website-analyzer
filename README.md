# 🚀 AI Website Analysis Tool

An advanced AI-powered website analysis tool that provides comprehensive insights into user experience, website functionality, and actionable recommendations using Claude AI.

## ✨ Features

### 🧠 **AI-Powered Analysis**
- **Claude Code SDK Integration** - Intelligent content analysis using Anthropic's Claude
- **Website Purpose Detection** - Automatically identifies website type, industry, and user segments
- **User Insights Generation** - Analyzes user goals, pain points, and behavioral patterns
- **Smart Recommendations** - Generates prioritized, actionable improvement suggestions
- **Intelligent User Stories** - Creates context-aware user stories based on actual website content

### 🗺️ **Advanced User Journey Mapping**
- **Multi-Persona Analysis** - Tests 5 different user types (New Customer, Returning Customer, Guest, Admin, Mobile)
- **Emotional State Tracking** - Maps user emotions throughout their journey
- **Screenshot Documentation** - Captures visual evidence at each journey step
- **Drop-off Risk Assessment** - Identifies potential user abandonment points
- **Responsive Testing** - Simulates both mobile and desktop experiences

### 📊 **Enhanced Visualizations**
- **Mermaid Diagram Generation** - User flows, conversion funnels, feature maps
- **Interactive HTML Dashboards** - Visual inefficiency reports and analytics
- **Persona Journey Diagrams** - Individual user journey visualizations
- **Drop-off Heatmaps** - Visual identification of UX problems
- **Satisfaction Analysis** - Emotional journey mapping

### 🔧 **Browser Automation**
- **Playwright Integration** - Intelligent web crawling with form filling and interaction
- **Smart Navigation** - AI-guided page exploration and action selection
- **Multi-page Analysis** - Configurable depth crawling (1-10+ pages)
- **Headless/Visual Modes** - Can run with or without browser UI  

## Installation

### Prerequisites
- Python 3.8+
- Node.js (for Playwright)
- Claude Code SDK access

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-website-analyzer.git
cd ai-website-analyzer

# Create and activate virtual environment
python -m venv ai_venv
source ai_venv/bin/activate  # On Windows: ai_venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install Claude Code SDK
pip install claude-code-sdk
```

## Quick Start

### Basic Usage

```python
import asyncio
from src.intelligent_browser import IntelligentBrowser

async def main():
    browser = IntelligentBrowser(headless=False, slow_mo=1000)
    
    try:
        await browser.start()
        
        # Browse a website with AI guidance
        results = await browser.analyze_and_browse(
            url="https://example.com",
            description="A simple example website"
        )
        
        print(f"Browsing completed: {results['success']}")
        
    finally:
        await browser.close()

asyncio.run(main())
```

### Command Line Usage

```bash
# Basic browsing
python -m src.main https://example.com

# With description
python -m src.main https://example.com -d "A simple example website"

# With account creation
python -m src.main https://example.com --create-account --email "user@example.com" --password "password123"

# Headless mode
python -m src.main https://example.com --headless
```

### Demo Script

```bash
# Run the interactive demo
python examples/demo.py
```

## How It Works

### 1. Website Analysis
The tool first analyzes the target website using Claude Code SDK to understand:
- Website purpose and functionality
- Key features and user flows
- Registration requirements
- Navigation structure
- Suggested user journey

### 2. Intelligent Navigation
Based on the analysis, the tool:
- Navigates to the website
- Analyzes each page in real-time
- Determines the next logical action
- Executes actions (clicking, form filling, navigation)
- Follows natural user journeys

### 3. Account Creation
When needed, the tool can:
- Detect signup/registration forms
- Fill out account creation forms
- Handle login processes
- Navigate through onboarding flows

### 4. AI Decision Making
At each step, Claude Code SDK:
- Analyzes the current page content
- Identifies interactive elements
- Suggests the next action
- Provides form data when needed
- Determines when to stop browsing

## Configuration

### Environment Variables

```bash
# Required
CLAUDE_API_KEY="your-claude-api-key"

# Optional
PLAYWRIGHT_HEADLESS="false"  # Set to "true" for headless mode
PLAYWRIGHT_SLOW_MO="1000"    # Delay between actions in ms
```

### Browser Options

```python
browser = IntelligentBrowser(
    headless=False,      # Show browser window
    slow_mo=1000,       # Delay between actions
    api_key="your-key"  # Claude API key
)
```

## Examples

### Example 1: E-commerce Website

```python
from src.intelligent_browser import IntelligentBrowser, UserCredentials

async def browse_ecommerce():
    browser = IntelligentBrowser(headless=False)
    
    # Create user credentials
    credentials = UserCredentials(
        email="user@example.com",
        password="SecurePassword123!",
        first_name="John",
        last_name="Doe"
    )
    
    try:
        await browser.start()
        
        # Browse the e-commerce site
        results = await browser.analyze_and_browse(
            url="https://shop.example.com",
            description="An e-commerce website selling electronics"
        )
        
        # Create account if needed
        if results['success']:
            account_result = await browser.create_user_account(credentials)
            print(f"Account creation: {account_result['success']}")
            
    finally:
        await browser.close()
```

### Example 2: Social Media Platform

```python
async def browse_social_media():
    browser = IntelligentBrowser(headless=False)
    
    try:
        await browser.start()
        
        results = await browser.analyze_and_browse(
            url="https://social.example.com",
            description="A social media platform for sharing photos and videos"
        )
        
        # The AI will automatically navigate through:
        # - Homepage analysis
        # - Signup process
        # - Profile setup
        # - Feature exploration
        
    finally:
        await browser.close()
```

## API Reference

### IntelligentBrowser

Main class for AI-powered web browsing.

#### Methods

- `start()`: Start the browser session
- `close()`: Close the browser session
- `analyze_and_browse(url, description)`: Analyze and browse a website
- `create_user_account(credentials)`: Create a user account
- `login_user(credentials)`: Login with existing credentials

### UserCredentials

Container for user account information.

```python
credentials = UserCredentials(
    email="user@example.com",
    password="password123",
    first_name="John",
    last_name="Doe",
    username="johndoe"
)
```

### Error Handling

The tool includes comprehensive error handling:

- **Retry Logic**: Automatic retries with exponential backoff
- **Circuit Breaker**: Prevents cascading failures
- **Validation**: Input validation for URLs and credentials
- **Logging**: Detailed error logging and session tracking

## Troubleshooting

### Common Issues

1. **Claude API Key Not Set**
   ```bash
   export CLAUDE_API_KEY="your-key-here"
   ```

2. **Playwright Browsers Not Installed**
   ```bash
   playwright install
   ```

3. **Claude Code CLI Not Found**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

4. **Permission Errors**
   - Ensure you have write permissions in the project directory
   - Check that the browser can access the target website

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [Playwright](https://playwright.dev/) for browser automation
- [Claude Code SDK](https://github.com/anthropics/claude-code-sdk-python) for AI integration
- [Anthropic](https://www.anthropic.com/) for Claude AI capabilities
