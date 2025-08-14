# 🏙️ NYC Airbnb Analytics Dashboard

A professional, interactive dashboard for analyzing Airbnb listings in New York City. Built with Streamlit and Plotly for comprehensive data visualization and market insights.

## 🌟 Features

### 📊 Interactive Analytics
- **Geographic Analysis**: Interactive maps showing listing distribution across NYC boroughs
- **Price Intelligence**: Comprehensive pricing analysis with trends and comparisons
- **Market Trends**: Room type distribution, seasonal patterns, and performance metrics
- **Property Analysis**: Host portfolios, minimum night requirements, and availability patterns
- **Data Insights**: Key statistics, correlations, and actionable business intelligence

### 🎛️ Dynamic Filtering
- Filter by borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
- Room type selection (Entire home/apt, Private room, Shared room)
- Price range slider for custom budget analysis
- Seasonal availability filtering (High, Medium, Low, Not Available)

### 📈 Professional Visualizations
- Interactive scatter plots and heatmaps
- Geographic mapping with clustering
- Statistical distributions and correlations
- Real-time metric calculations
- Export capabilities for filtered data

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Installation & Setup

1. **Ensure your data files are in place:**
   ```
   data/AB_NYC_Featured.csv    (primary dataset)
   data/AB_NYC_Cleaned1.csv    (fallback dataset)
   ```

2. **Activate your virtual environment:**
   ```bash
   # Windows PowerShell
   venv\Scripts\Activate.ps1
   
   # Or if already activated, you're ready to go!
   ```

3. **Install required packages (if not already installed):**
   ```bash
   pip install streamlit plotly dash folium streamlit-folium
   ```

4. **Launch the dashboard:**
   ```bash
   # Option 1: Using the launcher script
   python run_dashboard.py
   
   # Option 2: Direct streamlit command
   streamlit run app.py
   ```

5. **Access the dashboard:**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - The dashboard will load automatically

## 📋 Dashboard Sections

### 🗺️ Geographic Analysis
- **Interactive Map**: Plotly-powered geographic visualization with location clustering
- **Borough Statistics**: Detailed breakdown by NYC borough with pricing and review data
- **Neighborhood Insights**: Top performing neighborhoods and market concentration

### 💰 Price Intelligence
- **Price Distribution**: Histogram analysis of pricing patterns
- **Room Type Pricing**: Box plots comparing different accommodation types
- **Borough Price Comparison**: Average pricing across different areas
- **Price vs. Reviews**: Correlation analysis between pricing and customer satisfaction

### 📈 Market Trends
- **Room Type Distribution**: Market share analysis by accommodation type
- **Review Performance**: Distribution of listings by review count ranges
- **Availability Patterns**: Seasonal and year-round availability analysis
- **Host Analysis**: Single vs. multiple listing host distribution

### 🏠 Property Analysis
- **Minimum Nights**: Analysis of booking requirements
- **Host Portfolio Size**: Distribution of listings per host
- **Reviews per Month**: Customer engagement patterns
- **Feature Correlations**: Statistical relationships between key metrics

### 📋 Data Insights
- **Key Statistics Cards**: Executive summary of important metrics
- **Performance Indicators**: Market activity and engagement rates
- **Data Export**: Download filtered datasets for further analysis
- **Real-time Metrics**: Live calculations based on current filters

## 🎯 Key Performance Indicators

The dashboard automatically calculates and displays:

- **Total Listings**: Count of properties matching current filters
- **Average Price**: Mean pricing with comparison to overall market
- **Average Reviews**: Customer engagement metrics
- **Market Activity**: Percentage of active listings
- **Geographic Coverage**: Number of boroughs and neighborhoods represented

## 💡 Business Intelligence Features

### Market Analysis
- Identify pricing opportunities by borough and room type
- Analyze competitor performance through review patterns
- Understand seasonal demand variations
- Track market concentration and saturation

### Investment Insights
- Compare average prices across different areas
- Analyze correlation between price and customer satisfaction
- Identify underserved markets or neighborhoods
- Evaluate host portfolio strategies

### Performance Benchmarking
- Compare individual listings against market averages
- Identify top-performing neighborhoods
- Analyze review frequency and customer engagement
- Track availability patterns and booking requirements

## 📁 Project Structure

```
📦 NYC Airbnb Dashboard
├── 📄 app.py                    # Main dashboard application
├── 📄 dashboard.py              # Alternative dashboard version
├── 📄 run_dashboard.py          # Dashboard launcher script
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                # This documentation
└── 📁 data/
    ├── 📊 AB_NYC_Featured.csv   # Enhanced dataset with engineered features
    └── 📊 AB_NYC_Cleaned1.csv   # Cleaned base dataset
```

## 🔧 Technical Details

### Built With
- **Streamlit**: Web application framework for data apps
- **Plotly**: Interactive visualization library
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Folium**: Geographic mapping (alternative option)

### Performance Features
- **Data Caching**: Streamlit caching for faster load times
- **Sampling**: Large dataset sampling for improved map performance
- **Responsive Design**: Mobile-friendly layout with professional styling
- **Error Handling**: Graceful fallbacks and user-friendly error messages

## 🎨 Customization

The dashboard can be easily customized:

1. **Styling**: Modify the CSS in the `st.markdown()` sections
2. **Color Schemes**: Update Plotly color palettes in visualization functions
3. **Metrics**: Add new KPIs by extending the metrics calculation functions
4. **Filters**: Include additional filter options in the sidebar
5. **Visualizations**: Add new chart types using Plotly or other libraries

## 📊 Data Requirements

The dashboard expects CSV files with the following core columns:
- `neighbourhood_group`: NYC borough names
- `room_type`: Type of accommodation
- `price`: Listing price
- `latitude`, `longitude`: Geographic coordinates
- `number_of_reviews`: Review count
- `name`: Listing name/title

### Enhanced Features (AB_NYC_Featured.csv)
Additional columns for advanced analytics:
- `seasonal_availability`: Seasonal demand classification
- `active_listing`: Listing activity status
- `is_entire_home`: Binary flag for entire home listings
- `price_per_night`: Calculated nightly rate
- `has_review`: Review existence flag

## 🤝 Support

For questions or issues:
1. Check that all data files are in the correct location
2. Ensure all dependencies are installed (`pip install -r requirements.txt`)
3. Verify Python version compatibility (3.8+)
4. Try the alternative dashboard file (`dashboard.py`) if needed

## 📈 Future Enhancements

Potential additions:
- Time series analysis with historical data
- Predictive pricing models
- Advanced clustering analysis
- Integration with external APIs
- Automated report generation
- Multi-language support

---

**Created for professional Airbnb market analysis and business intelligence.**