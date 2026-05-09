"""
Streamlit demo UI for Jeevn MVP
"""
import streamlit as st
import requests
import json
import pandas as pd
from typing import Optional, Dict, Any

try:
    import folium
    from streamlit_folium import st_folium
    from folium.plugins import Draw, Geocoder
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Jeevn - AOI Analysis",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Jeevn - Agricultural AOI Analysis")
st.markdown("Submit an Area of Interest (AOI) for remote-sensing analysis")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    api_url = st.text_input(
        "API URL",
        value="http://localhost:8000",
        help="Base URL for the Jeevn API"
    )
    
    st.markdown("---")
    
    # Check health
    if st.button("Check API Health"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ API is healthy")
            else:
                st.error(f"❌ API returned status {response.status_code}")
        except Exception as e:
            st.error(f"❌ API connection failed: {e}")

# Main form
st.header("Submit AOI")

col1, col2 = st.columns(2)

with col1:
    aoi_name = st.text_input(
        "AOI Name",
        value="My AOI",
        help="Descriptive name for this AOI"
    )
    
    start_date = st.date_input("Start Date", help="Analysis start date (YYYY-MM-DD)")
    end_date = st.date_input("End Date", help="Analysis end date (YYYY-MM-DD)")

with col2:
    st.markdown("**Select Area on Map**")
    
    drawn_geojson = None
    
    if FOLIUM_AVAILABLE:
        # Default center (e.g., somewhere in Kansas, USA, or anywhere)
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
        
        # Add search bar
        Geocoder().add_to(m)
        
        # Add drawing tools (only allow polygons and rectangles for AOI)
        draw = Draw(
            draw_options={
                'polyline': False,
                'polygon': True,
                'rectangle': True,
                'circle': False,
                'marker': False,
                'circlemarker': False
            },
            edit_options={'edit': False}
        )
        draw.add_to(m)
        
        # Render map in streamlit
        output = st_folium(m, height=300, use_container_width=True)
        
        # Extract drawn geometry
        if output and output.get("last_active_drawing"):
            # Folium returns the geometry. Wrap it in a FeatureCollection
            geom = output["last_active_drawing"]["geometry"]
            drawn_geojson = {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "geometry": geom
                }]
            }
            st.success("✅ AOI drawn successfully!")
        else:
            st.info("Draw a polygon on the map to define your AOI.")
            
    else:
        st.warning("folium and streamlit-folium not installed. Please run `pip install folium streamlit-folium`")
    
    # Fallback/Manual text area if map fails or user prefers it
    st.markdown("**Or Paste GeoJSON Manually**")
    default_val = json.dumps(drawn_geojson, indent=2) if drawn_geojson else json.dumps({
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0,0], [1,0], [1,1], [0,1], [0,0]]]}}]
    }, indent=2)
    
    geojson_text = st.text_area(
        "GeoJSON Code",
        height=100,
        value=default_val,
        help="Map drawing automatically populates this"
    )

# Submit button
if st.button("Submit AOI", type="primary", use_container_width=True):
    try:
        # Parse GeoJSON
        geojson = json.loads(geojson_text)
        
        # Prepare request
        payload = {
            "name": aoi_name,
            "geojson": geojson,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        }
        
        # Submit to API
        with st.spinner("Submitting AOI..."):
            response = requests.post(
                f"{api_url}/aoi",
                json=payload,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            aoi_id = result.get("aoi_id")
            
            st.success(f"✅ AOI created: `{aoi_id}`")
            
            # Store in query params for persistence
            st.query_params["aoi_id"] = aoi_id
            
            # Display results
            st.subheader("Analysis Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("AOI ID", aoi_id[:8] + "...")
                st.metric("Metadata Path", result.get("metadata_path", "N/A")[:40] + "...")
            
            with col2:
                ndvi_csv = result.get("ndvi_csv")
                ndvi_raster = result.get("ndvi_raster")
                st.metric("NDVI CSV", "✓" if ndvi_csv else "✗")
                st.metric("NDVI Raster", "✓" if ndvi_raster else "✗")
            
            # Timeseries Chart
            if result.get("ndvi_timeseries"):
                st.subheader("Vegetation & Moisture Indices Over Time")
                df = pd.DataFrame(result["ndvi_timeseries"])
                if not df.empty:
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.set_index('date')
                    cols_to_plot = [col for col in ['ndvi', 'ndwi', 'ndre'] if col in df.columns]
                    st.line_chart(df[cols_to_plot])
            
            # Parcel confidence
            if result.get("parcel_confidence"):
                st.subheader("Parcel Confidence")
                confidence = result["parcel_confidence"]
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Mean NDVI", f"{confidence.get('mean_ndvi', 0):.3f}")
                col2.metric("Std Dev", f"{confidence.get('std_ndvi', 0):.3f}")
                col3.metric("Confidence", f"{confidence.get('confidence_score', 0):.2%}")
                
            # Anomalies and Signals
            if result.get("anomalies"):
                st.subheader("Advanced Signals & Stress Detection")
                anom = result["anomalies"]
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Water Stress", f"{anom.get('water_stress', 0):.2f}/1.0")
                c2.metric("Nutrient Stress", f"{anom.get('nutrient_stress', 0):.2f}/1.0")
                
                disease = anom.get("disease_patch", {}).get("risk_score", 0.0)
                c3.metric("Disease Risk", f"{disease:.2f}/1.0")
                
                fert = anom.get("fertilizer_issue", {}).get("issue_score", 0.0)
                c4.metric("Fertilizer Need", f"{fert:.2f}/1.0")
                
                st.markdown("---")
                w_guidance = anom.get("weeds_guidance", {})
                if isinstance(w_guidance, dict):
                    wp_score = w_guidance.get('weed_pressure_score', 0)
                    wp_msg = w_guidance.get('guidance', '')
                    st.info(f"🌿 **Weed Pressure Score:** `{wp_score:.2f}/1.00` — {wp_msg}")
                else:
                    st.info(f"🌿 **Weeds Guidance:** {w_guidance}")
                
                yp = anom.get("yield_proxy", {})
                if yp:
                    y_val = yp.get('estimated_yield_t_ha', yp.get('estimated_yield', 0))
                    conf = yp.get('confidence', 0)
                    st.success(f"🌾 **Estimated Yield:** `{y_val:.2f} t/ha` (Prediction Confidence: `{conf:.1%}`)")
            
            # Full response
            with st.expander("Full API Response"):
                st.json(result)
        
        else:
            st.error(f"API error: {response.status_code}")
            st.error(response.text)
    
    except json.JSONDecodeError:
        st.error("❌ Invalid GeoJSON format")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Report viewer
st.markdown("---")
st.header("View Existing Report")

aoi_id_input = st.text_input("Enter AOI ID to view report", value="")

if st.button("Fetch Report"):
    if aoi_id_input:
        try:
            with st.spinner("Fetching report..."):
                response = requests.get(
                    f"{api_url}/aoi/{aoi_id_input}/report",
                    timeout=10
                )
            
            if response.status_code == 200:
                report = response.json()
                
                st.success(f"✅ Report for `{aoi_id_input}`")
                
                st.json(report)
            
            else:
                st.error(f"Report not found (status {response.status_code})")
        
        except Exception as e:
            st.error(f"Error fetching report: {e}")
    else:
        st.warning("Please enter an AOI ID")

# Footer
st.markdown("---")
st.markdown("""
**Jeevn MVP** - Agricultural Remote-Sensing Analysis

Submit an AOI and we'll analyze it using Sentinel-2 imagery.
""")
