"""
Playwright browser automation module for intelligent web browsing.
"""
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import json
import time
from pathlib import Path


class BrowserAutomation:
    """Handles browser automation using Playwright with AI-guided navigation."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 1000):
        """Initialize browser automation.
        
        Args:
            headless: Whether to run browser in headless mode
            slow_mo: Delay between actions in milliseconds
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        
    async def start_browser(self) -> None:
        """Start the browser and create a new context."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        self.page = await self.context.new_page()
        
    async def close_browser(self) -> None:
        """Close the browser and cleanup resources."""
        try:
            if self.page and not self.page.is_closed():
                await self.page.close()
        except Exception as e:
            print(f"Page close warning: {e}")
        
        try:
            if self.context and not self.context.is_closed():
                await self.context.close()
        except Exception as e:
            print(f"Context close warning: {e}")
        
        try:
            if self.browser and not self.browser.is_connected():
                await self.browser.close()
        except Exception as e:
            print(f"Browser close warning: {e}")
        
        try:
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"Playwright stop warning: {e}")
            
    async def navigate_to(self, url: str) -> Dict[str, Any]:
        """Navigate to a URL and return page information.
        
        Args:
            url: The URL to navigate to
            
        Returns:
            Dictionary containing page information
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start_browser() first.")
            
        try:
            response = await self.page.goto(url, wait_until='networkidle')
            await self.page.wait_for_load_state('domcontentloaded')
            
            # Get page content and metadata
            page_info = await self._get_page_info()
            page_info['url'] = url
            page_info['status'] = response.status if response else 0
            
            return page_info
            
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'status': 0,
                'content': '',
                'title': '',
                'forms': [],
                'links': [],
                'buttons': []
            }
    
    async def _get_page_info(self) -> Dict[str, Any]:
        """Extract comprehensive information from the current page."""
        try:
            # Get basic page information
            title = await self.page.title()
            content = await self.page.content()
            
            # Extract interactive elements
            forms = await self._extract_forms()
            links = await self._extract_links()
            buttons = await self._extract_buttons()
            inputs = await self._extract_inputs()
            
            return {
                'title': title,
                'content': content,
                'forms': forms,
                'links': links,
                'buttons': buttons,
                'inputs': inputs,
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {
                'title': '',
                'content': '',
                'forms': [],
                'links': [],
                'buttons': [],
                'inputs': [],
                'error': str(e),
                'timestamp': time.time()
            }
    
    async def _extract_forms(self) -> List[Dict[str, Any]]:
        """Extract form information from the page."""
        forms = []
        try:
            form_elements = await self.page.query_selector_all('form')
            for form in form_elements:
                form_info = {
                    'action': await form.get_attribute('action') or '',
                    'method': await form.get_attribute('method') or 'get',
                    'fields': []
                }
                
                # Extract input fields
                inputs = await form.query_selector_all('input, select, textarea')
                for input_elem in inputs:
                    field_info = {
                        'type': await input_elem.get_attribute('type') or 'text',
                        'name': await input_elem.get_attribute('name') or '',
                        'id': await input_elem.get_attribute('id') or '',
                        'placeholder': await input_elem.get_attribute('placeholder') or '',
                        'required': await input_elem.get_attribute('required') is not None
                    }
                    form_info['fields'].append(field_info)
                
                forms.append(form_info)
        except Exception as e:
            print(f"Error extracting forms: {e}")
            
        return forms
    
    async def _extract_links(self) -> List[Dict[str, Any]]:
        """Extract link information from the page."""
        links = []
        try:
            link_elements = await self.page.query_selector_all('a[href]')
            for link in link_elements:
                href = await link.get_attribute('href')
                text = await link.inner_text()
                if href and text.strip():
                    links.append({
                        'href': href,
                        'text': text.strip(),
                        'title': await link.get_attribute('title') or ''
                    })
        except Exception as e:
            print(f"Error extracting links: {e}")
            
        return links
    
    async def _extract_buttons(self) -> List[Dict[str, Any]]:
        """Extract button information from the page."""
        buttons = []
        try:
            button_elements = await self.page.query_selector_all('button, input[type="submit"], input[type="button"]')
            for button in button_elements:
                text = await button.inner_text()
                button_type = await button.get_attribute('type') or 'button'
                button_id = await button.get_attribute('id') or ''
                button_class = await button.get_attribute('class') or ''
                
                if text.strip() or button_id or button_class:
                    buttons.append({
                        'text': text.strip(),
                        'type': button_type,
                        'id': button_id,
                        'class': button_class
                    })
        except Exception as e:
            print(f"Error extracting buttons: {e}")
            
        return buttons
    
    async def _extract_inputs(self) -> List[Dict[str, Any]]:
        """Extract input field information from the page."""
        inputs = []
        try:
            input_elements = await self.page.query_selector_all('input, select, textarea')
            for input_elem in input_elements:
                input_info = {
                    'type': await input_elem.get_attribute('type') or 'text',
                    'name': await input_elem.get_attribute('name') or '',
                    'id': await input_elem.get_attribute('id') or '',
                    'placeholder': await input_elem.get_attribute('placeholder') or '',
                    'required': await input_elem.get_attribute('required') is not None,
                    'value': await input_elem.get_attribute('value') or ''
                }
                inputs.append(input_info)
        except Exception as e:
            print(f"Error extracting inputs: {e}")
            
        return inputs
    
    async def click_element(self, selector: str, timeout: int = 10000) -> bool:
        """Click an element on the page.
        
        Args:
            selector: CSS selector for the element to click
            timeout: Maximum time to wait for the element
            
        Returns:
            True if successful, False otherwise
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.click(selector)
            await self.page.wait_for_load_state('networkidle')
            return True
        except Exception as e:
            print(f"Error clicking element {selector}: {e}")
            return False
    
    async def fill_form(self, form_data: Dict[str, str]) -> bool:
        """Fill out a form with the provided data.
        
        Args:
            form_data: Dictionary mapping field names/selectors to values
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for field, value in form_data.items():
                # Try different selectors
                selectors = [
                    f'input[name="{field}"]',
                    f'input[id="{field}"]',
                    f'textarea[name="{field}"]',
                    f'select[name="{field}"]',
                    f'#{field}',
                    f'[name="{field}"]'
                ]
                
                filled = False
                for selector in selectors:
                    try:
                        await self.page.wait_for_selector(selector, timeout=2000)
                        await self.page.fill(selector, str(value))
                        filled = True
                        break
                    except:
                        continue
                
                if not filled:
                    print(f"Could not find field: {field}")
                    return False
                    
            return True
            
        except Exception as e:
            print(f"Error filling form: {e}")
            return False
    
    async def submit_form(self, form_selector: str = 'form') -> bool:
        """Submit a form.
        
        Args:
            form_selector: CSS selector for the form to submit
            
        Returns:
            True if successful, False otherwise
        """
        try:
            await self.page.wait_for_selector(form_selector)
            await self.page.evaluate(f'document.querySelector("{form_selector}").submit()')
            await self.page.wait_for_load_state('networkidle')
            return True
        except Exception as e:
            print(f"Error submitting form: {e}")
            return False
    
    async def wait_for_navigation(self, timeout: int = 10000) -> bool:
        """Wait for page navigation to complete.
        
        Args:
            timeout: Maximum time to wait
            
        Returns:
            True if navigation completed, False if timeout
        """
        try:
            await self.page.wait_for_load_state('networkidle', timeout=timeout)
            return True
        except Exception as e:
            print(f"Navigation timeout: {e}")
            return False
    
    async def take_screenshot(self, path: str = None) -> str:
        """Take a screenshot of the current page.
        
        Args:
            path: Optional path to save the screenshot
            
        Returns:
            Path where screenshot was saved
        """
        if not path:
            timestamp = int(time.time())
            path = f"screenshot_{timestamp}.png"
            
        try:
            await self.page.screenshot(path=path)
            return path
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return ""
    
    async def get_current_url(self) -> str:
        """Get the current page URL."""
        if self.page:
            return self.page.url
        return ""
    
    async def get_page_content(self) -> str:
        """Get the current page content."""
        if self.page:
            return await self.page.content()
        return ""
