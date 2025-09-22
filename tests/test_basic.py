"""
Basic tests for the Playwright AI Browser.
"""
import pytest
import asyncio
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from intelligent_browser import IntelligentBrowser, UserCredentials
from website_analyzer import WebsiteAnalyzer
from browser_automation import BrowserAutomation


class TestUserCredentials:
    """Test UserCredentials class."""
    
    def test_credentials_creation(self):
        """Test creating user credentials."""
        creds = UserCredentials(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        
        assert creds.email == "test@example.com"
        assert creds.password == "password123"
        assert creds.first_name == "Test"
        assert creds.last_name == "User"
        assert creds.username == ""  # Should be empty by default


class TestWebsiteAnalyzer:
    """Test WebsiteAnalyzer class."""
    
    def test_analyzer_creation(self):
        """Test creating website analyzer."""
        analyzer = WebsiteAnalyzer()
        assert analyzer is not None
    
    def test_build_analysis_prompt(self):
        """Test building analysis prompt."""
        analyzer = WebsiteAnalyzer()
        prompt = analyzer._build_analysis_prompt("https://example.com", "Test website")
        
        assert "https://example.com" in prompt
        assert "Test website" in prompt
        assert "Purpose" in prompt
        assert "Key Features" in prompt
    
    def test_parse_analysis_response(self):
        """Test parsing analysis response."""
        analyzer = WebsiteAnalyzer()
        
        # Test with valid JSON
        valid_json = '{"purpose": "Test", "key_features": ["feature1"]}'
        result = analyzer._parse_analysis_response(valid_json)
        assert result["purpose"] == "Test"
        assert result["key_features"] == ["feature1"]
        
        # Test with invalid JSON
        invalid_json = "This is not JSON"
        result = analyzer._parse_analysis_response(invalid_json)
        assert "purpose" in result  # Should return fallback structure


class TestBrowserAutomation:
    """Test BrowserAutomation class."""
    
    def test_browser_creation(self):
        """Test creating browser automation."""
        browser = BrowserAutomation(headless=True)
        assert browser is not None
        assert browser.headless is True
        assert browser.slow_mo == 1000  # Default value
    
    def test_browser_creation_with_params(self):
        """Test creating browser with custom parameters."""
        browser = BrowserAutomation(headless=False, slow_mo=500)
        assert browser.headless is False
        assert browser.slow_mo == 500


class TestIntelligentBrowser:
    """Test IntelligentBrowser class."""
    
    def test_browser_creation(self):
        """Test creating intelligent browser."""
        browser = IntelligentBrowser(headless=True)
        assert browser is not None
        assert browser.browser is not None
        assert browser.analyzer is not None
    
    def test_credentials_assignment(self):
        """Test assigning credentials."""
        browser = IntelligentBrowser()
        creds = UserCredentials("test@example.com", "password123")
        
        browser.credentials = creds
        assert browser.credentials.email == "test@example.com"
        assert browser.credentials.password == "password123"


@pytest.mark.asyncio
class TestAsyncFunctionality:
    """Test async functionality."""
    
    async def test_browser_start_stop(self):
        """Test starting and stopping browser."""
        browser = IntelligentBrowser(headless=True)
        
        try:
            await browser.start()
            assert browser.browser.browser is not None
            assert browser.browser.context is not None
            assert browser.browser.page is not None
        finally:
            await browser.close()
    
    async def test_navigate_to_url(self):
        """Test navigating to a URL."""
        browser = IntelligentBrowser(headless=True)
        
        try:
            await browser.start()
            
            # Navigate to a simple test page
            page_info = await browser.browser.navigate_to("data:text/html,<html><body><h1>Test Page</h1></body></html>")
            
            assert "error" not in page_info
            assert page_info["title"] == ""
            assert "Test Page" in page_info["content"]
            
        finally:
            await browser.close()
    
    async def test_page_info_extraction(self):
        """Test extracting page information."""
        browser = IntelligentBrowser(headless=True)
        
        try:
            await browser.start()
            
            # Navigate to a test page with forms and links
            test_html = """
            <html>
                <head><title>Test Page</title></head>
                <body>
                    <h1>Test Page</h1>
                    <form action="/submit" method="post">
                        <input type="text" name="username" placeholder="Username">
                        <input type="password" name="password" placeholder="Password">
                        <button type="submit">Submit</button>
                    </form>
                    <a href="/about">About</a>
                    <a href="/contact">Contact</a>
                </body>
            </html>
            """
            
            page_info = await browser.browser.navigate_to(f"data:text/html,{test_html}")
            
            assert page_info["title"] == "Test Page"
            assert len(page_info["forms"]) == 1
            assert len(page_info["links"]) == 2
            assert len(page_info["buttons"]) == 1
            
            # Check form details
            form = page_info["forms"][0]
            assert form["action"] == "/submit"
            assert form["method"] == "post"
            assert len(form["fields"]) == 2
            
        finally:
            await browser.close()


def test_imports():
    """Test that all modules can be imported."""
    try:
        from intelligent_browser import IntelligentBrowser, UserCredentials
        from website_analyzer import WebsiteAnalyzer
        from browser_automation import BrowserAutomation
        from error_handling import ErrorHandler, retry_with_backoff
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import modules: {e}")


if __name__ == "__main__":
    # Run basic tests
    print("Running basic tests...")
    
    # Test imports
    test_imports()
    print("✅ Import tests passed")
    
    # Test UserCredentials
    test_creds = TestUserCredentials()
    test_creds.test_credentials_creation()
    print("✅ UserCredentials tests passed")
    
    # Test WebsiteAnalyzer
    test_analyzer = TestWebsiteAnalyzer()
    test_analyzer.test_analyzer_creation()
    test_analyzer.test_build_analysis_prompt()
    test_analyzer.test_parse_analysis_response()
    print("✅ WebsiteAnalyzer tests passed")
    
    # Test BrowserAutomation
    test_browser = TestBrowserAutomation()
    test_browser.test_browser_creation()
    test_browser.test_browser_creation_with_params()
    print("✅ BrowserAutomation tests passed")
    
    # Test IntelligentBrowser
    test_intelligent = TestIntelligentBrowser()
    test_intelligent.test_browser_creation()
    test_intelligent.test_credentials_assignment()
    print("✅ IntelligentBrowser tests passed")
    
    print("\n🎉 All basic tests passed!")
