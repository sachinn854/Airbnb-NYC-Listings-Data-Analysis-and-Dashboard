# NYC Airbnb Dashboard Launcher
# Run this file to start the professional dashboard

import subprocess
import sys
import os

def main():
    """Launch the Streamlit dashboard"""
    
    # Get the current directory
    current_dir = os.getcwd()
    
    print("🚀 Starting NYC Airbnb Analytics Dashboard...")
    print(f"📁 Working directory: {current_dir}")
    
    # Check if the data files exist
    data_files = ['data/AB_NYC_Featured.csv', 'data/AB_NYC_Cleaned1.csv']
    found_files = []
    
    for file in data_files:
        if os.path.exists(file):
            found_files.append(file)
            print(f"✅ Found data file: {file}")
    
    if not found_files:
        print("❌ No data files found! Please ensure you have:")
        for file in data_files:
            print(f"   - {file}")
        return
    
    print(f"📊 Using dataset: {found_files[0]}")
    
    # Launch Streamlit
    try:
        print("\n🌐 Launching dashboard at http://localhost:8501")
        print("💡 Press Ctrl+C to stop the dashboard")
        print("=" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port=8501',
            '--server.address=localhost',
            '--browser.gatherUsageStats=false'
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

if __name__ == "__main__":
    main()
