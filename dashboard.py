import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import numpy as np
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="NYC Airbnb Analytics Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional dark theme with perfect text visibility
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF5A5F;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #2e2e2e;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF5A5F;
        color: #e0e0e0;
    }
    .sidebar .sidebar-content {
        background-color: #262730;
    }
    .stSelectbox label {
        font-weight: bold;
        color: #e0e0e0 !important;
    }
    
    /* Keep dark theme for main app */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Fix metric boxes - light background for readability but dark theme everywhere else */
    .stMetric {
        background-color: #f8f9fa !important;
        padding: 1.2rem !important;
        border-radius: 10px !important;
        border: 2px solid #dee2e6 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
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
    }
    .stMetric [data-testid="metric-container"] > div {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    .stMetric [data-testid="metric-container"] div {
        color: #1a1a1a !important;
    }
    
    /* Specific targeting for metric values */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 10px !important;
        padding: 1.2rem !important;
        color: #1a1a1a !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
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
    }
    
    /* Dark theme for general text */
    .css-1d391kg, .css-1y4p8pa, .css-12oz5g7 {
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
        border: 1px solid #555 !important;
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
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data():
    """Load and cache the Airbnb dataset"""
    try:
        df = pd.read_csv('data/AB_NYC_Featured.csv')
        df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure 'data/AB_NYC_Featured.csv' exists.")
        return None

# Load data
df = load_data()

if df is not None:
    # Header
    st.markdown('<h1 class="main-header">🏠 NYC Airbnb Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar filters
    st.sidebar.header("📊 Dashboard Filters")
    
    # Borough filter
    boroughs = ['All'] + sorted(df['neighbourhood_group'].unique())
    selected_borough = st.sidebar.selectbox(
        "Select Borough:",
        boroughs,
        key="borough_filter"
    )
    
    # Room type filter
    room_types = ['All'] + sorted(df['room_type'].unique())
    selected_room_type = st.sidebar.selectbox(
        "Select Room Type:",
        room_types,
        key="room_type_filter"
    )
    
    # Price range filter
    price_min, price_max = st.sidebar.slider(
        "Price Range ($):",
        min_value=int(df['price'].min()),
        max_value=int(df['price'].max()),
        value=(int(df['price'].min()), int(df['price'].max())),
        step=10,
        key="price_filter"
    )
    
    # Availability filter
    availability_options = ['All'] + sorted(df['seasonal_availability'].unique())
    selected_availability = st.sidebar.selectbox(
        "Seasonal Availability:",
        availability_options,
        key="availability_filter"
    )

    # Filter data based on selections
    filtered_df = df.copy()
    
    if selected_borough != 'All':
        filtered_df = filtered_df[filtered_df['neighbourhood_group'] == selected_borough]
    
    if selected_room_type != 'All':
        filtered_df = filtered_df[filtered_df['room_type'] == selected_room_type]
    
    filtered_df = filtered_df[
        (filtered_df['price'] >= price_min) & 
        (filtered_df['price'] <= price_max)
    ]
    
    if selected_availability != 'All':
        filtered_df = filtered_df[filtered_df['seasonal_availability'] == selected_availability]

    # Key Metrics Row
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_listings = len(filtered_df)
        st.metric(
            label="Total Listings",
            value=f"{total_listings:,}",
            delta=f"{((total_listings/len(df))*100):.1f}% of total"
        )
    
    with col2:
        avg_price = filtered_df['price'].mean()
        st.metric(
            label="Average Price",
            value=f"${avg_price:.0f}",
            delta=f"${avg_price - df['price'].mean():.0f} vs overall"
        )
    
    with col3:
        avg_reviews = filtered_df['number_of_reviews'].mean()
        st.metric(
            label="Avg Reviews",
            value=f"{avg_reviews:.1f}",
            delta=f"{avg_reviews - df['number_of_reviews'].mean():.1f} vs overall"
        )
    
    with col4:
        active_listings = len(filtered_df[filtered_df['active_listing'] == 1])
        st.metric(
            label="Active Listings",
            value=f"{active_listings:,}",
            delta=f"{(active_listings/total_listings*100):.1f}% active"
        )
    
    with col5:
        entire_home_pct = (filtered_df['is_entire_home'].sum() / len(filtered_df)) * 100
        st.metric(
            label="Entire Homes",
            value=f"{entire_home_pct:.1f}%",
            delta=f"{entire_home_pct - (df['is_entire_home'].sum()/len(df)*100):.1f}% vs overall"
        )

    st.markdown("---")

    # Main Dashboard Layout
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Geographic Analysis", 
        "💰 Price Analytics", 
        "📊 Market Analysis", 
        "📈 Performance Metrics"
    ])

    with tab1:
        st.subheader("Geographic Distribution of Listings")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Interactive map
            if len(filtered_df) > 0:
                # Sample data for better performance if dataset is too large
                map_df = filtered_df.sample(min(2000, len(filtered_df))) if len(filtered_df) > 2000 else filtered_df
                
                # Create folium map
                center_lat = map_df['latitude'].mean()
                center_lon = map_df['longitude'].mean()
                
                m = folium.Map(
                    location=[center_lat, center_lon],
                    zoom_start=10,
                    tiles='OpenStreetMap'
                )
                
                # Add markers with color coding by room type
                colors = {'Entire home/apt': 'red', 'Private room': 'blue', 'Shared room': 'green'}
                
                for idx, row in map_df.iterrows():
                    folium.CircleMarker(
                        [row['latitude'], row['longitude']],
                        radius=3,
                        popup=f"""
                        <b>{row['name'][:30]}...</b><br>
                        Room Type: {row['room_type']}<br>
                        Price: ${row['price']}<br>
                        Borough: {row['neighbourhood_group']}<br>
                        Reviews: {row['number_of_reviews']}
                        """,
                        color=colors.get(row['room_type'], 'gray'),
                        fill=True,
                        opacity=0.7
                    ).add_to(m)
                
                # Display map
                map_data = st_folium(m, width=700, height=500)
            else:
                st.warning("No data available for the selected filters.")
        
        with col2:
            # Borough distribution
            if len(filtered_df) > 0:
                borough_counts = filtered_df['neighbourhood_group'].value_counts()
                
                fig_borough = px.pie(
                    values=borough_counts.values,
                    names=borough_counts.index,
                    title="Listings by Borough",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_borough.update_layout(height=300)
                st.plotly_chart(fig_borough, use_container_width=True)
                
                # Top neighborhoods
                st.subheader("Top 10 Neighborhoods")
                top_neighborhoods = filtered_df['neighbourhood'].value_counts().head(10)
                
                fig_neighborhoods = px.bar(
                    x=top_neighborhoods.values,
                    y=top_neighborhoods.index,
                    orientation='h',
                    title="Most Popular Neighborhoods",
                    labels={'x': 'Number of Listings', 'y': 'Neighborhood'}
                )
                fig_neighborhoods.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_neighborhoods, use_container_width=True)

    with tab2:
        st.subheader("Price Analysis & Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Price distribution by room type
            fig_price_dist = px.box(
                filtered_df,
                x='room_type',
                y='price',
                title='Price Distribution by Room Type',
                color='room_type',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_price_dist.update_layout(height=400)
            st.plotly_chart(fig_price_dist, use_container_width=True)
            
            # Price vs Reviews scatter
            fig_price_reviews = px.scatter(
                filtered_df.sample(min(1000, len(filtered_df))),
                x='number_of_reviews',
                y='price',
                color='room_type',
                size='availability_365',
                title='Price vs Number of Reviews',
                labels={'number_of_reviews': 'Number of Reviews', 'price': 'Price ($)'},
                hover_data=['neighbourhood_group']
            )
            fig_price_reviews.update_layout(height=400)
            st.plotly_chart(fig_price_reviews, use_container_width=True)
        
        with col2:
            # Average price by borough
            avg_price_borough = filtered_df.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)
            
            fig_avg_price = px.bar(
                x=avg_price_borough.index,
                y=avg_price_borough.values,
                title='Average Price by Borough',
                labels={'x': 'Borough', 'y': 'Average Price ($)'},
                color=avg_price_borough.values,
                color_continuous_scale='Viridis'
            )
            fig_avg_price.update_layout(height=400)
            st.plotly_chart(fig_avg_price, use_container_width=True)
            
            # Price range analysis
            price_ranges = pd.cut(filtered_df['price'], 
                                bins=[0, 100, 200, 300, 500, float('inf')], 
                                labels=['$0-100', '$100-200', '$200-300', '$300-500', '$500+'])
            price_range_counts = price_ranges.value_counts()
            
            fig_price_ranges = px.pie(
                values=price_range_counts.values,
                names=price_range_counts.index,
                title="Price Range Distribution",
                color_discrete_sequence=px.colors.sequential.RdYlBu
            )
            fig_price_ranges.update_layout(height=400)
            st.plotly_chart(fig_price_ranges, use_container_width=True)

    with tab3:
        st.subheader("Market Analysis & Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Room type distribution
            room_type_counts = filtered_df['room_type'].value_counts()
            
            fig_room_type = px.bar(
                x=room_type_counts.index,
                y=room_type_counts.values,
                title='Listings by Room Type',
                labels={'x': 'Room Type', 'y': 'Number of Listings'},
                color=room_type_counts.values,
                color_continuous_scale='Blues'
            )
            fig_room_type.update_layout(height=400)
            st.plotly_chart(fig_room_type, use_container_width=True)
            
            # Seasonal availability analysis
            seasonal_counts = filtered_df['seasonal_availability'].value_counts()
            
            fig_seasonal = px.donut(
                values=seasonal_counts.values,
                names=seasonal_counts.index,
                title="Seasonal Availability Distribution",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_seasonal.update_layout(height=400)
            st.plotly_chart(fig_seasonal, use_container_width=True)
        
        with col2:
            # Host analysis
            host_listings = filtered_df.groupby('host_id').size().sort_values(ascending=False)
            
            # Multiple listings hosts
            multi_listing_hosts = len(host_listings[host_listings > 1])
            single_listing_hosts = len(host_listings[host_listings == 1])
            
            fig_host_type = px.bar(
                x=['Single Listing', 'Multiple Listings'],
                y=[single_listing_hosts, multi_listing_hosts],
                title='Host Types Distribution',
                labels={'x': 'Host Type', 'y': 'Number of Hosts'},
                color=['Single Listing', 'Multiple Listings'],
                color_discrete_sequence=['#FF6B6B', '#4ECDC4']
            )
            fig_host_type.update_layout(height=400)
            st.plotly_chart(fig_host_type, use_container_width=True)
            
            # Top hosts by number of listings
            top_hosts = host_listings.head(10)
            host_names = []
            for host_id in top_hosts.index:
                host_name = filtered_df[filtered_df['host_id'] == host_id]['host_name'].iloc[0]
                host_names.append(f"{host_name} (ID: {host_id})")
            
            fig_top_hosts = px.bar(
                x=top_hosts.values,
                y=host_names,
                orientation='h',
                title='Top 10 Hosts by Listings Count',
                labels={'x': 'Number of Listings', 'y': 'Host'},
                color=top_hosts.values,
                color_continuous_scale='Oranges'
            )
            fig_top_hosts.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_top_hosts, use_container_width=True)

    with tab4:
        st.subheader("Performance Metrics & Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Review performance
            review_bins = pd.cut(filtered_df['number_of_reviews'], 
                               bins=[0, 5, 20, 50, 100, float('inf')], 
                               labels=['0-5', '6-20', '21-50', '51-100', '100+'])
            review_dist = review_bins.value_counts()
            
            fig_reviews = px.bar(
                x=review_dist.index,
                y=review_dist.values,
                title='Listings by Review Count Range',
                labels={'x': 'Review Range', 'y': 'Number of Listings'},
                color=review_dist.values,
                color_continuous_scale='Greens'
            )
            fig_reviews.update_layout(height=400)
            st.plotly_chart(fig_reviews, use_container_width=True)
            
            # Availability analysis
            availability_analysis = filtered_df.groupby('neighbourhood_group')['availability_365'].mean().sort_values(ascending=False)
            
            fig_availability = px.bar(
                x=availability_analysis.index,
                y=availability_analysis.values,
                title='Average Availability by Borough',
                labels={'x': 'Borough', 'y': 'Average Days Available'},
                color=availability_analysis.values,
                color_continuous_scale='RdYlGn'
            )
            fig_availability.update_layout(height=400)
            st.plotly_chart(fig_availability, use_container_width=True)
        
        with col2:
            # Correlation heatmap
            numeric_cols = ['price', 'minimum_nights', 'number_of_reviews', 
                          'reviews_per_month', 'availability_365', 'calculated_host_listings_count']
            correlation_matrix = filtered_df[numeric_cols].corr()
            
            fig_corr = px.imshow(
                correlation_matrix,
                title='Feature Correlation Matrix',
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Price per night vs standard price
            fig_price_comparison = px.scatter(
                filtered_df.sample(min(1000, len(filtered_df))),
                x='price',
                y='price_per_night',
                color='room_type',
                title='Price vs Price Per Night',
                labels={'price': 'Listed Price ($)', 'price_per_night': 'Price Per Night ($)'},
                hover_data=['neighbourhood_group', 'minimum_nights']
            )
            fig_price_comparison.update_layout(height=400)
            st.plotly_chart(fig_price_comparison, use_container_width=True)

    # Footer with insights
    st.markdown("---")
    st.subheader("📊 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **Market Overview**
        - Total listings in selection: {len(filtered_df):,}
        - Most popular borough: {filtered_df['neighbourhood_group'].value_counts().index[0] if len(filtered_df) > 0 else 'N/A'}
        - Dominant room type: {filtered_df['room_type'].value_counts().index[0] if len(filtered_df) > 0 else 'N/A'}
        """)
    
    with col2:
        st.success(f"""
        **Pricing Intelligence**
        - Average price: ${filtered_df['price'].mean():.0f}
        - Price range: ${filtered_df['price'].min():.0f} - ${filtered_df['price'].max():.0f}
        - Median price: ${filtered_df['price'].median():.0f}
        """)
    
    with col3:
        st.warning(f"""
        **Performance Metrics**
        - Average reviews: {filtered_df['number_of_reviews'].mean():.1f}
        - Active listings: {(filtered_df['active_listing'].sum()/len(filtered_df)*100):.1f}%
        - Avg availability: {filtered_df['availability_365'].mean():.0f} days/year
        """)

    # Data export option
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Export Data")
    
    if st.sidebar.button("Download Filtered Data as CSV"):
        csv = filtered_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"airbnb_filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

else:
    st.error("Unable to load the dataset. Please check if the data file exists.")
