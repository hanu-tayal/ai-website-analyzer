# Product Analyzer Tool - Usage Guide

## 🚀 Quick Start

### Basic Usage
```bash
python product_analyzer_tool.py <website_url>
```

### Examples
```bash
# Analyze a simple API site
python product_analyzer_tool.py https://httpbin.org

# Analyze with custom depth and output directory
python product_analyzer_tool.py https://example.com --depth 5 --output ./my_analysis

# Run with visible browser (for debugging)
python product_analyzer_tool.py https://jsonplaceholder.typicode.com --no-headless

# Analyze without https:// prefix
python product_analyzer_tool.py example.com
```

## 📋 Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--depth` | `-d` | Maximum analysis depth (pages to explore) | 5 |
| `--output` | `-o` | Output directory for generated files | `analysis_output` |
| `--no-headless` | | Run browser in visible mode | headless |
| `--version` | | Show version information | |
| `--help` | `-h` | Show help message | |

## 📊 Generated Output Files

For each analysis, the tool generates:

### 1. **Analysis Data** (`analysis_<domain>_<timestamp>.json`)
- Complete analysis results
- Page types discovered
- Features identified
- User interactions mapped
- Session logs

### 2. **User Stories** (`user_stories_<domain>_<timestamp>.md`)
- User stories in Markdown format
- Acceptance criteria
- Priority levels
- Page type associations

### 3. **Mermaid Diagrams**
- `diagram_user_flow_<domain>_<timestamp>.mmd` - User flow diagram
- `diagram_page_types_<domain>_<timestamp>.mmd` - Page type diagram
- `diagram_feature_map_<domain>_<timestamp>.mmd` - Feature map diagram
- `all_diagrams_<domain>_<timestamp>.mmd` - All diagrams combined

### 4. **Summary Report** (`summary_<domain>_<timestamp>.md`)
- Analysis overview
- Generated files list
- Results summary

## 🎯 Best Websites for Testing

### Simple Sites (Good for testing)
- `https://httpbin.org` - API testing site
- `https://example.com` - Basic example site
- `https://jsonplaceholder.typicode.com` - API documentation

### Complex Sites (For real analysis)
- E-commerce sites
- SaaS platforms
- Documentation sites
- Community forums

## 🔧 Troubleshooting

### Common Issues

1. **"No user stories generated"**
   - Website may be too simple
   - Try a more complex website with forms and interactions

2. **"Analysis failed"**
   - Check internet connection
   - Verify website URL is correct
   - Try with `--no-headless` to see browser behavior

3. **"Browser crashed"**
   - Website may be too complex
   - Try reducing `--depth` parameter
   - Use `--no-headless` for debugging

### Debug Mode
```bash
python product_analyzer_tool.py <url> --no-headless --depth 2
```

## 📈 Understanding the Output

### User Stories
Generated based on discovered forms and page types:
- **Authentication** - Login/signup forms
- **E-commerce** - Product pages, shopping carts
- **User Management** - Dashboards, profiles
- **Content** - Blog posts, articles
- **Support** - Contact forms, help pages

### Mermaid Diagrams
- **User Flow** - How users navigate through the site
- **Page Types** - Different types of pages discovered
- **Feature Map** - Features and functionality identified

## 🚀 Advanced Usage

### Batch Analysis
```bash
# Analyze multiple websites
for url in "https://httpbin.org" "https://example.com" "https://jsonplaceholder.typicode.com"; do
    python product_analyzer_tool.py "$url" --output "analysis_$(date +%Y%m%d)"
done
```

### Custom Output Directory
```bash
python product_analyzer_tool.py https://example.com --output ./my_product_analysis
```

### Integration with CI/CD
```bash
# Add to your build pipeline
python product_analyzer_tool.py $WEBSITE_URL --output ./docs/product_analysis
```

## 📝 Tips for Better Results

1. **Use complex websites** - Sites with forms, user accounts, and multiple pages work best
2. **Adjust depth** - Start with depth 3-5 for most sites
3. **Check output files** - Review generated Markdown and Mermaid files
4. **Use visible mode** - Use `--no-headless` to see what the browser is doing
5. **Analyze multiple pages** - The tool works best when it can explore multiple pages

## 🎉 Success!

The tool successfully generates:
- ✅ User stories for product development
- ✅ Mermaid diagrams for process visualization
- ✅ Feature maps and user flows
- ✅ Comprehensive analysis data
- ✅ Professional documentation

Perfect for understanding any website's structure and generating product documentation!
