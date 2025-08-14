import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="NYC Airbnb Analytics Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling with dark theme and perfect text visibility
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #FF5A5F;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #e0e0e0;
        margin-bottom: 1rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .insight-card {
        background-color: #2e2e2e;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF5A5F;
        margin: 1rem 0;
        color: #e0e0e0;
    }
    .stSelectbox > div > div {
        background-color: #404040;
        color: #e0e0e0;
        border: 1px solid #555;
    }
    
    /* Fix metric boxes with dark theme but visible text */
    .stMetric {
        background-color: #f8f9fa !important;
        padding: 1.2rem !important;
        border-radius: 10px !important;
        border: 2px solid #dee2e6 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15) !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Force metric text to be dark for visibility on light metric boxes */
    .stMetric > div {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    .stMetric label {
        color: #495057 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    .stMetric [data-testid="metric-container"] {
        background-color: #f8f9fa !important;
        color: #1a1a1a !important;
        border: none !important;
    }
    .stMetric [data-testid="metric-container"] > div {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    .stMetric [data-testid="metric-container"] div {
        color: #1a1a1a !important;
    }
    
    /* Specific targeting for metric values - keep light background for readability */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 10px !important;
        padding: 1.2rem !important;
        color: #1a1a1a !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.12) !important;
    }
    div[data-testid="metric-container"] > div {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    div[data-testid="metric-container"] label {
        color: #495057 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Keep dark theme for main app */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Dark theme text colors */
    .css-1d391kg, .css-1y4p8pa, .css-12oz5g7, .css-1cpxqw2 {
        color: #e0e0e0 !important;
    }
    
    /* Sidebar with dark theme */
    .css-1d391kg {
        color: #e0e0e0 !important;
        background-color: #262730 !important;
    }
    
    /* Form elements with dark theme */
    .stSelectbox > div > div {
        background-color: #404040 !important;
        color: #e0e0e0 !important;
        border: 2px solid #555 !important;
    }
    .stSlider > div > div {
        color: #e0e0e0 !important;
    }
    
    /* Alert boxes with dark theme */
    .stInfo {
        background-color: #1e3a5f !important;
        color: #cfe2ff !important;
        border: 1px solid #3d6bb3 !important;
    }
    .stSuccess {
        background-color: #1e4d2b !important;
        color: #c8e6c9 !important;
        border: 1px solid #4caf50 !important;
    }
    .stWarning {
        background-color: #5c4b00 !important;
        color: #fff3cd !important;
        border: 1px solid #ffc107 !important;
    }
    .stError {
        background-color: #5c1e1e !important;
        color: #f8d7da !important;
        border: 1px solid #dc3545 !important;
    }
    
    /* Data tables with dark theme */
    .dataframe {
        color: #e0e0e0 !important;
        background-color: #262730 !important;
    }
    
    /* General text with dark theme */
    .stMarkdown, .stText {
        color: #e0e0e0 !important;
    }
    
    /* Tab styling for dark theme */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #262730;
    }
    .stTabs [data-baseweb="tab"] {
        color: #e0e0e0;
        background-color: #404040;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF5A5F !important;
        color: white !important;
    }
    
    /* Chart/plot background adjustments */
    .js-plotly-plot {
        background-color: #1e1e1e !important;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading with error handling
@st.cache_data
def load_data():
    """Load and cache the Airbnb dataset with error handling"""
    try:
        # Try to load the featured dataset first
        df = pd.read_csv('data/AB_NYC_Featured.csv')
        df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
        return df, "Featured"
    except FileNotFoundError:
        try:
            # Fallback to cleaned dataset
            df = pd.read_csv('data/AB_NYC_Cleaned1.csv')
            df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
            return df, "Cleaned"
        except FileNotFoundError:
            return None, None

# Helper function for price analysis
def analyze_price_trends(df):
    """Analyze price trends and return insights"""
    insights = {}
    insights['avg_price'] = df['price'].mean()
    insights['median_price'] = df['price'].median()
    insights['price_std'] = df['price'].std()
    insights['most_expensive_borough'] = df.groupby('neighbourhood_group')['price'].mean().idxmax()
    insights['cheapest_borough'] = df.groupby('neighbourhood_group')['price'].mean().idxmin()
    return insights

# Helper function for market analysis
def get_market_insights(df):
    """Generate market insights"""
    total_listings = len(df)
    active_listings = len(df[df.get('active_listing', 1) == 1]) if 'active_listing' in df.columns else total_listings
    
    insights = {
        'total_listings': total_listings,
        'active_listings': active_listings,
        'activity_rate': (active_listings / total_listings) * 100,
        'avg_reviews': df['number_of_reviews'].mean(),
        'top_borough': df['neighbourhood_group'].value_counts().index[0],
        'dominant_room_type': df['room_type'].value_counts().index[0]
    }
    return insights

# Load data
df, dataset_type = load_data()

if df is not None:
    # Header
    st.markdown('<h1 class="main-header">🏙️ NYC Airbnb Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.2rem; color: #666;'>Professional Analytics Dashboard • Dataset: {dataset_type} • Last Updated: {datetime.now().strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar filters
    st.sidebar.markdown("## 🎛️ Dashboard Controls")
    st.sidebar.markdown("### Filter Options")
    
    # Borough filter
    boroughs = ['All'] + sorted(df['neighbourhood_group'].unique())
    selected_borough = st.sidebar.selectbox(
        "🏘️ Select Borough:",
        boroughs,
        help="Filter listings by New York City borough"
    )
    
    # Room type filter
    room_types = ['All'] + sorted(df['room_type'].unique())
    selected_room_type = st.sidebar.selectbox(
        "🏠 Select Room Type:",
        room_types,
        help="Filter by accommodation type"
    )
    
    # Price range filter
    price_min, price_max = st.sidebar.slider(
        "💰 Price Range (USD):",
        min_value=int(df['price'].min()),
        max_value=int(df['price'].max()),
        value=(int(df['price'].min()), int(df['price'].max())),
        step=25,
        help="Set the price range for listings"
    )
    
    # Additional filters if available in featured dataset
    if 'seasonal_availability' in df.columns:
        availability_options = ['All'] + sorted(df['seasonal_availability'].unique())
        selected_availability = st.sidebar.selectbox(
            "📅 Seasonal Availability:",
            availability_options,
            help="Filter by seasonal availability"
        )
    else:
        selected_availability = 'All'

    # Filter data
    filtered_df = df.copy()
    
    if selected_borough != 'All':
        filtered_df = filtered_df[filtered_df['neighbourhood_group'] == selected_borough]
    
    if selected_room_type != 'All':
        filtered_df = filtered_df[filtered_df['room_type'] == selected_room_type]
    
    filtered_df = filtered_df[
        (filtered_df['price'] >= price_min) & 
        (filtered_df['price'] <= price_max)
    ]
    
    if selected_availability != 'All' and 'seasonal_availability' in df.columns:
        filtered_df = filtered_df[filtered_df['seasonal_availability'] == selected_availability]

    # Get insights
    market_insights = get_market_insights(filtered_df)
    price_insights = analyze_price_trends(filtered_df)

    # Key Metrics Dashboard
    st.markdown("## 📊 Executive Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📈 Total Listings",
            value=f"{market_insights['total_listings']:,}",
            delta=f"{((market_insights['total_listings']/len(df))*100):.1f}% of dataset"
        )
    
    with col2:
        st.metric(
            label="💵 Average Price",
            value=f"${price_insights['avg_price']:.0f}",
            delta=f"${price_insights['avg_price'] - df['price'].mean():.0f} vs overall"
        )
    
    with col3:
        st.metric(
            label="⭐ Average Reviews",
            value=f"{market_insights['avg_reviews']:.1f}",
            delta=f"{market_insights['avg_reviews'] - df['number_of_reviews'].mean():.1f} vs overall"
        )
    
    with col4:
        activity_rate = market_insights.get('activity_rate', 100)
        st.metric(
            label="🎯 Market Activity",
            value=f"{activity_rate:.1f}%",
            delta="Active listings"
        )

    st.markdown("---")

    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Geographic Analysis", 
        "💰 Price Intelligence", 
        "📈 Market Trends", 
        "🏠 Property Analysis",
        "📋 Data Insights"
    ])

    with tab1:
        st.markdown("### Geographic Distribution & Mapping")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Density map using plotly
            if len(filtered_df) > 0:
                sample_size = min(2000, len(filtered_df))
                map_data = filtered_df.sample(sample_size) if len(filtered_df) > sample_size else filtered_df
                
                fig_map = px.scatter_mapbox(
                    map_data,
                    lat="latitude",
                    lon="longitude",
                    color="room_type",
                    size="price",
                    hover_name="name",
                    hover_data=["neighbourhood_group", "price", "number_of_reviews"],
                    color_discrete_sequence=px.colors.qualitative.Set1,
                    zoom=9,
                    height=500,
                    title=f"NYC Airbnb Listings Distribution ({sample_size:,} listings shown)"
                )
                
                fig_map.update_layout(
                    mapbox_style="carto-positron",
                    margin={"r":0,"t":50,"l":0,"b":0}
                )
                
                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.warning("No data available for the selected filters.")
        
        with col2:
            # Borough statistics
            st.markdown("#### Borough Breakdown")
            
            if len(filtered_df) > 0:
                borough_stats = filtered_df.groupby('neighbourhood_group').agg({
                    'price': 'mean',
                    'number_of_reviews': 'mean',
                    'id': 'count'
                }).round(2)
                borough_stats.columns = ['Avg Price', 'Avg Reviews', 'Listings']
                borough_stats = borough_stats.sort_values('Listings', ascending=False)
                
                st.dataframe(borough_stats, use_container_width=True)
                
                # Top neighborhoods
                st.markdown("#### Top Neighborhoods")
                top_neighborhoods = filtered_df['neighbourhood'].value_counts().head(8)
                
                fig_neighborhoods = px.bar(
                    y=top_neighborhoods.index,
                    x=top_neighborhoods.values,
                    orientation='h',
                    title="Most Popular Areas",
                    height=300
                )
                fig_neighborhoods.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_neighborhoods, use_container_width=True)

    with tab2:
        st.markdown("### Price Intelligence & Market Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Price distribution
            fig_price_hist = px.histogram(
                filtered_df,
                x='price',
                nbins=30,
                title='Price Distribution',
                color_discrete_sequence=['#FF5A5F']
            )
            fig_price_hist.update_layout(height=400)
            st.plotly_chart(fig_price_hist, use_container_width=True)
            
            # Price by room type
            fig_price_room = px.box(
                filtered_df,
                x='room_type',
                y='price',
                title='Price Range by Room Type',
                color='room_type'
            )
            fig_price_room.update_layout(height=400)
            st.plotly_chart(fig_price_room, use_container_width=True)
        
        with col2:
            # Borough price comparison
            borough_prices = filtered_df.groupby('neighbourhood_group')['price'].agg(['mean', 'median', 'std']).round(2)
            
            fig_borough_prices = px.bar(
                x=borough_prices.index,
                y=borough_prices['mean'],
                title='Average Price by Borough',
                color=borough_prices['mean'],
                color_continuous_scale='Viridis'
            )
            fig_borough_prices.update_layout(height=400)
            st.plotly_chart(fig_borough_prices, use_container_width=True)
            
            # Price correlation with reviews
            if len(filtered_df) > 10:
                # Add toggle for trendline
                show_trendline = st.checkbox("Show Trend Line", value=False)
                
                if show_trendline:
                    try:
                        fig_price_reviews = px.scatter(
                            filtered_df.sample(min(1000, len(filtered_df))),
                            x='number_of_reviews',
                            y='price',
                            color='room_type',
                            title='Price vs Reviews Relationship',
                            trendline='ols'
                        )
                    except ImportError:
                        st.warning("Trendline requires statsmodels package. Showing without trendline.")
                        fig_price_reviews = px.scatter(
                            filtered_df.sample(min(1000, len(filtered_df))),
                            x='number_of_reviews',
                            y='price',
                            color='room_type',
                            title='Price vs Reviews Relationship'
                        )
                else:
                    fig_price_reviews = px.scatter(
                        filtered_df.sample(min(1000, len(filtered_df))),
                        x='number_of_reviews',
                        y='price',
                        color='room_type',
                        title='Price vs Reviews Relationship'
                    )
                
                fig_price_reviews.update_layout(height=400)
                st.plotly_chart(fig_price_reviews, use_container_width=True)

    with tab3:
        st.markdown("### Market Trends & Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Room type distribution
            room_counts = filtered_df['room_type'].value_counts()
            fig_rooms = px.pie(
                values=room_counts.values,
                names=room_counts.index,
                title='Market Share by Room Type',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_rooms.update_layout(height=400)
            st.plotly_chart(fig_rooms, use_container_width=True)
            
            # Reviews distribution
            review_bins = pd.cut(filtered_df['number_of_reviews'], 
                               bins=[0, 1, 10, 50, 100, float('inf')], 
                               labels=['No Reviews', '1-10', '11-50', '51-100', '100+'])
            review_dist = review_bins.value_counts()
            
            fig_reviews = px.bar(
                x=review_dist.index,
                y=review_dist.values,
                title='Listings by Review Count',
                color=review_dist.values,
                color_continuous_scale='Blues'
            )
            fig_reviews.update_layout(height=400)
            st.plotly_chart(fig_reviews, use_container_width=True)
        
        with col2:
            # Availability analysis
            if 'availability_365' in filtered_df.columns:
                avg_availability = filtered_df.groupby('neighbourhood_group')['availability_365'].mean()
                
                fig_availability = px.bar(
                    x=avg_availability.index,
                    y=avg_availability.values,
                    title='Average Availability by Borough',
                    color=avg_availability.values,
                    color_continuous_scale='RdYlGn'
                )
                fig_availability.update_layout(height=400)
                st.plotly_chart(fig_availability, use_container_width=True)
            
            # Host analysis
            host_listings = filtered_df['host_id'].value_counts()
            multi_host = len(host_listings[host_listings > 1])
            single_host = len(host_listings[host_listings == 1])
            
            fig_hosts = px.pie(
                values=[single_host, multi_host],
                names=['Single Listing', 'Multiple Listings'],
                title='Host Distribution',
                color_discrete_sequence=['#FF6B6B', '#4ECDC4']
            )
            fig_hosts.update_layout(height=400)
            st.plotly_chart(fig_hosts, use_container_width=True)

    with tab4:
        st.markdown("### Property Analysis & Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Minimum nights analysis
            min_nights_dist = filtered_df['minimum_nights'].value_counts().head(10)
            
            fig_min_nights = px.bar(
                x=min_nights_dist.index,
                y=min_nights_dist.values,
                title='Minimum Nights Requirements',
                labels={'x': 'Minimum Nights', 'y': 'Number of Listings'}
            )
            fig_min_nights.update_layout(height=400)
            st.plotly_chart(fig_min_nights, use_container_width=True)
            
            # Host listings count
            if 'calculated_host_listings_count' in filtered_df.columns:
                host_listings_dist = filtered_df['calculated_host_listings_count'].value_counts().head(15)
                
                fig_host_count = px.bar(
                    x=host_listings_dist.index,
                    y=host_listings_dist.values,
                    title='Host Portfolio Size Distribution',
                    labels={'x': 'Number of Listings per Host', 'y': 'Number of Hosts'}
                )
                fig_host_count.update_layout(height=400)
                st.plotly_chart(fig_host_count, use_container_width=True)
        
        with col2:
            # Reviews per month analysis
            if 'reviews_per_month' in filtered_df.columns:
                filtered_reviews = filtered_df[filtered_df['reviews_per_month'].notna()]
                
                fig_reviews_month = px.histogram(
                    filtered_reviews,
                    x='reviews_per_month',
                    nbins=20,
                    title='Reviews per Month Distribution'
                )
                fig_reviews_month.update_layout(height=400)
                st.plotly_chart(fig_reviews_month, use_container_width=True)
            
            # Feature correlation (if featured dataset)
            if dataset_type == "Featured" and len(filtered_df) > 50:
                numeric_cols = ['price', 'minimum_nights', 'number_of_reviews', 'availability_365']
                if all(col in filtered_df.columns for col in numeric_cols):
                    correlation_data = filtered_df[numeric_cols].corr()
                    
                    fig_corr = px.imshow(
                        correlation_data,
                        title='Feature Correlation Matrix',
                        color_continuous_scale='RdBu',
                        aspect='auto'
                    )
                    fig_corr.update_layout(height=400)
                    st.plotly_chart(fig_corr, use_container_width=True)

    with tab5:
        st.markdown("### Data Insights & Summary")
        
        # Key insights cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            price_leader_text = "N/A"
            if 'most_expensive_borough' in price_insights and isinstance(price_insights['most_expensive_borough'], (int, float)):
                price_leader_text = f"{price_insights['most_expensive_borough']:.0f} avg"
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>🏆 Market Leaders</h4>
                <ul>
                    <li><strong>Top Borough:</strong> {market_insights['top_borough']}</li>
                    <li><strong>Dominant Room Type:</strong> {market_insights['dominant_room_type']}</li>
                    <li><strong>Price Leader:</strong> ${price_leader_text}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_price = price_insights['avg_price'] if isinstance(price_insights['avg_price'], (int, float)) else 0
            min_price = filtered_df['price'].min() if len(filtered_df) > 0 else 0
            max_price = filtered_df['price'].max() if len(filtered_df) > 0 else 0
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>💡 Key Statistics</h4>
                <ul>
                    <li><strong>Total Properties:</strong> {market_insights['total_listings']:,}</li>
                    <li><strong>Average Price:</strong> ${avg_price:.0f}</li>
                    <li><strong>Price Range:</strong> ${min_price:.0f} - ${max_price:.0f}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_reviews = market_insights['avg_reviews'] if isinstance(market_insights['avg_reviews'], (int, float)) else 0
            activity_rate = market_insights.get('activity_rate', 100)
            if not isinstance(activity_rate, (int, float)):
                activity_rate = 100
            
            st.markdown(f"""
            <div class="insight-card">
                <h4>📈 Performance Metrics</h4>
                <ul>
                    <li><strong>Avg Reviews:</strong> {avg_reviews:.1f}</li>
                    <li><strong>Active Rate:</strong> {activity_rate:.1f}%</li>
                    <li><strong>Market Coverage:</strong> {len(filtered_df['neighbourhood_group'].unique())} boroughs</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Data table
        st.markdown("#### Filtered Dataset Preview")
        
        # Display columns to show
        display_cols = ['name', 'neighbourhood_group', 'room_type', 'price', 'number_of_reviews']
        if 'seasonal_availability' in filtered_df.columns:
            display_cols.append('seasonal_availability')
            
        st.dataframe(
            filtered_df[display_cols].head(100),
            use_container_width=True,
            hide_index=True
        )
        
        # Download option
        st.markdown("#### Export Data")
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"nyc_airbnb_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download the current filtered dataset"
        )

    # Sidebar summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Current Selection")
    st.sidebar.info(f"""
    **Dataset:** {dataset_type}  
    **Listings:** {len(filtered_df):,}  
    **Avg Price:** ${filtered_df['price'].mean():.0f}  
    **Date:** {datetime.now().strftime('%m/%d/%Y')}
    """)

else:
    st.error("""
    ## ❌ Dataset Not Found
    
    Please ensure one of the following files exists:
    - `data/AB_NYC_Featured.csv` (preferred)
    - `data/AB_NYC_Cleaned1.csv` (fallback)
    
    The dashboard requires properly formatted Airbnb data to function.
    """)
    
    st.info("""
    ### Expected Data Structure:
    The dataset should contain columns like:
    - `neighbourhood_group`, `room_type`, `price`
    - `latitude`, `longitude`, `number_of_reviews`
    - Additional features in the Featured dataset enhance functionality
    """)
