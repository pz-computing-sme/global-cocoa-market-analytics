import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. Dashboard Architecture: High-End Analytics
st.set_page_config(page_title="Cocoa Strategic Intel | Vitor Pozza", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .report-box { background: rgba(30, 41, 59, 0.5); border-left: 4px solid #d4af37; padding: 20px; border-radius: 8px; margin: 10px 0; }
    .stMetric { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 12px; }
    h1, h2, h3 { color: #d4af37 !important; }
    
    .sidebar-footer {
        font-size: 11px;
        color: #94a3b8;
        border-top: 1px solid rgba(212, 175, 55, 0.2);
        padding-top: 15px;
        margin-top: 30px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data(ttl=3600)
def get_historical_data():
    # Tracking the massive 2024-2026 cycle
    return yf.download("CC=F", start="2024-01-01")

ny_data = get_historical_data()
fx_data = yf.download("USDBRL=X", period="1d")

# Data Point Extraction
usd_brl = float(fx_data['Close'].iloc[-1]) if not fx_data.empty else 5.25
current_price = float(ny_data['Close'].iloc[-1]) if not ny_data.empty else 4000.0
peak_2024 = float(ny_data['High'].max()) if not ny_data.empty else 12000.0

# --- SIDEBAR (THE AUTHORITY ZONE) ---
st.sidebar.title("💎 Cocoa Control Panel")
st.sidebar.metric("USD / BRL Rate", f"R$ {usd_brl:.2f}")

# Sidebar Footer: Copyright & Timestamp
st.sidebar.markdown(f"""
    <div class="sidebar-footer">
        <p><b>Executive Analytics System</b></p>
        <p>© {datetime.now().year} Vitor Pozza<br>
        All Rights Reserved.</p>
        <p><i>SME Cocoa Commodities Intelligence</i></p>
        <p style="color: #d4af37; font-weight: bold;">
            Last Update: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN INTERFACE ---
st.title("🌍 Global Cocoa Market Intelligence")
st.markdown("##### Strategic Analysis: NY/LDN Exchanges vs. Brazilian Farmgate Reality")

# Metrics Section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("2024 Historical Peak", f"${peak_2024:,.2f}")
with col2:
    st.metric("Current NY Price", f"${current_price:,.2f}", f"{((current_price/peak_2024)-1)*100:.1f}% vs Peak")
with col3:
    # Theoretical Parity for 15kg Arroba
    theoretical_parity = (current_price / 1000) * 15 * usd_brl
    st.metric("Theoretical Parity (BRL/Arr)", f"R$ {theoretical_parity:.2f}")

st.divider()

# --- ANALYTICS CHART (THE 12K TO 4K CRASH) ---
st.subheader("📊 Market Volatility: New York Exchange (2024-2026)")
if not ny_data.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ny_data.index, 
        y=ny_data['Close'].squeeze(), 
        fill='tozeroy', 
        name="NY Cocoa Futures", 
        line=dict(color='#d4af37', width=3)
    ))
    fig.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        height=450,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- SUBSTANCE & REGIONAL IMPACT ---
st.subheader("⚠️ Strategic Report: The Brazilian Producer Crisis")
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown(f"""
    <div class="report-box">
        <h4>Market Manipulation & Farmgate Suppression</h4>
        <p>The price collapse from <b>$12,000 to $4,000</b> in New York is being weaponized by domestic moageiras to compress local margins. 
        In <b>Ibirapitanga (BA)</b> and throughout the Southern Bahia region, producers have initiated massive protests, including <b>BR-101 highway blockades</b>.</p>
        <p>The core grievance is the predatory use of low-quality African cocoa imports to artificially inflate supply and drive down farmgate prices.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📰 External Intelligence & News")
    st.info("Direct Action: Producers demand federal protection against unfair import practices.")
    st.markdown("[Bahia Notícias: BR-101 Blockade](https://www.bahianoticias.com.br/municipios/noticia/49130-produtores-rurais-de-ibirapitanga-bloqueiam-br-101-em-manifestacao-contra-importacao-de-cacau-africano)")
    st.markdown("[Radio Interativa: Cocoa Price Collapse Protest](https://radiointerativa96fm.com.br/colapso-no-preco-do-cacau-leva-produtores-a-bloquear-a-br-101-no-sul-da-bahia/)")

with c2:
    st.subheader("📍 Regional Price Spread")
    regional_prices = {
        "Theoretical Parity": theoretical_parity,
        "Actual Farmgate (BA)": theoretical_parity * 0.88,
        "Industry Basis Gap": theoretical_parity * 0.12
    }
    for label, val in regional_prices.items():
        st.write(f"**{label}:** R$ {val:.2f}")

st.divider()