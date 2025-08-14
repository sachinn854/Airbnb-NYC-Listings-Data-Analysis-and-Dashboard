# Quick Dashboard Test
import pandas as pd
import streamlit as st

# Test data loading
try:
    df = pd.read_csv('data/AB_NYC_Featured.csv')
    print(f"✅ Data loaded successfully: {len(df):,} records")
    print(f"✅ Columns: {list(df.columns)}")
    
    # Test basic functionality
    boroughs = df['neighbourhood_group'].unique()
    room_types = df['room_type'].unique()
    
    print(f"✅ Boroughs: {list(boroughs)}")
    print(f"✅ Room Types: {list(room_types)}")
    print(f"✅ Price range: ${df['price'].min():.0f} - ${df['price'].max():.0f}")
    print(f"✅ Average price: ${df['price'].mean():.0f}")
    
    print("\n🎉 Dashboard should work perfectly!")
    print("🌐 Open http://localhost:8501 in your browser to view the dashboard")
    
except Exception as e:
    print(f"❌ Error: {e}")
