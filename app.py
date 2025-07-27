import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import random
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Influencer Marketing ROI Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stMetric > label {
        color: white !important;
    }
    
    .stMetric > div {
        color: white !important;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .title-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    h1, h2, h3 {
        color: #2c3e50;
    }
    
    .title-text {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .subtitle-text {
        color: white;
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA GENERATION FUNCTIONS ---
@st.cache_data
def generate_influencers_data(n=2000):
    """Generate realistic influencer data"""
    random.seed(42)  # For reproducibility
    np.random.seed(42)
    
    # Indian names pools
    first_names_male = ['Aarav', 'Rohan', 'Vikram', 'Karan', 'Arjun', 'Rahul', 'Amit', 'Suresh', 'Raj', 'Dev', 
                        'Akash', 'Nikhil', 'Siddharth', 'Varun', 'Aditya', 'Ishaan', 'Kabir', 'Yash', 'Harsh', 'Ravi']
    first_names_female = ['Priya', 'Sneha', 'Ananya', 'Kavya', 'Riya', 'Shreya', 'Pooja', 'Neha', 'Divya', 'Sanya',
                          'Isha', 'Tanya', 'Meera', 'Aditi', 'Nisha', 'Simran', 'Kriti', 'Swati', 'Payal', 'Deepika']
    last_names = ['Sharma', 'Patel', 'Das', 'Reddy', 'Singh', 'Gupta', 'Malhotra', 'Agarwal', 'Jain', 'Kumar',
                  'Verma', 'Shah', 'Chopra', 'Sinha', 'Mishra', 'Yadav', 'Pandey', 'Nair', 'Iyer', 'Kapoor']
    
    categories = ['Fitness', 'Wellness', 'Bodybuilding', 'Yoga', 'Nutrition', 'Lifestyle', 'Sports', 'Health', 'Beauty', 'Diet']
    platforms = ['Instagram', 'YouTube', 'Twitter', 'TikTok', 'Facebook']
    
    influencers = []
    for i in range(1, n + 1):
        gender = random.choice(['Male', 'Female'])
        first_name = random.choice(first_names_male if gender == 'Male' else first_names_female)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        
        # Generate realistic follower counts with some correlation to platform
        platform = random.choice(platforms)
        if platform == 'Instagram':
            follower_count = int(np.random.lognormal(13.5, 1.2))  # Higher for Instagram
        elif platform == 'YouTube':
            follower_count = int(np.random.lognormal(12.8, 1.3))
        elif platform == 'TikTok':
            follower_count = int(np.random.lognormal(13.2, 1.4))
        else:
            follower_count = int(np.random.lognormal(12.5, 1.1))
        
        follower_count = max(10000, min(10000000, follower_count))  # Reasonable bounds
        
        influencers.append({
            'id': i,
            'name': name,
            'category': random.choice(categories),
            'gender': gender,
            'follower_count': follower_count,
            'platform': platform
        })
    
    return pd.DataFrame(influencers)

@st.cache_data
def generate_posts_data(influencers_df, posts_per_influencer_range=(1, 5)):
    """Generate posts data"""
    random.seed(42)
    np.random.seed(42)
    
    brands = ['MuscleBlaze', 'HKVitals', 'Gritzo', 'TrueBasics', 'NutraBay']
    captions = [
        'Loving my new {} protein!',
        'My daily {} routine',
        '{} for the win!',
        'Perfect workout fuel with {}',
        'Unboxing {} supplements',
        'Quick thoughts on {} nutrition',
        'Fueling my workouts with {}',
        '{} keeps me energized',
        'Amazing results with {}',
        'Check out this {} product!'
    ]
    
    posts = []
    post_id = 1
    
    start_date = datetime(2023, 8, 1)
    end_date = datetime(2023, 12, 31)
    
    for _, influencer in influencers_df.iterrows():
        num_posts = random.randint(*posts_per_influencer_range)
        
        for _ in range(num_posts):
            brand = random.choice(brands)
            caption = random.choice(captions).format(brand)
            
            # Generate realistic engagement based on follower count
            base_reach = min(influencer['follower_count'] * random.uniform(0.1, 0.8), influencer['follower_count'])
            reach = int(base_reach * random.uniform(0.5, 1.5))
            
            engagement_rate = random.uniform(0.01, 0.15)  # 1-15% engagement
            total_engagement = int(reach * engagement_rate)
            
            likes = int(total_engagement * random.uniform(0.7, 0.9))
            comments = total_engagement - likes
            
            # Random date between start and end
            random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            
            posts.append({
                'post_id': post_id,
                'influencer_id': influencer['id'],
                'platform': influencer['platform'],
                'date': random_date.strftime('%Y-%m-%d'),
                'url': f'http://{influencer["platform"].lower()}.com/p{post_id}',
                'caption': caption,
                'reach': reach,
                'likes': likes,
                'comments': comments
            })
            post_id += 1
    
    return pd.DataFrame(posts)

@st.cache_data
def generate_tracking_data(influencers_df, posts_df):
    """Generate tracking/conversion data"""
    random.seed(42)
    np.random.seed(42)
    
    campaigns = ['DiwaliSale23', 'WinterBulkUp23', 'NewYearFitness24', 'SummerShred23', 'FestiveFit23']
    brands = ['MuscleBlaze', 'HKVitals', 'Gritzo', 'TrueBasics', 'NutraBay']
    products = {
        'MuscleBlaze': ['Whey Protein', 'Creatine', 'Pre-Workout', 'BCAA', 'Mass Gainer'],
        'HKVitals': ['Multivitamin', 'Biotin', 'Omega-3', 'Vitamin D', 'Iron'],
        'Gritzo': ['SuperMilk', 'Protein Bars', 'Kids Nutrition', 'Immunity Booster', 'Growth Mix'],
        'TrueBasics': ['Collagen', 'Probiotics', 'Ashwagandha', 'Turmeric', 'Green Tea'],
        'NutraBay': ['Protein Powder', 'Fat Burner', 'Testosterone Booster', 'Joint Support', 'Recovery']
    }
    
    tracking_data = []
    tracking_id = 1
    
    # Generate tracking data for subset of influencers (not all will have conversions)
    conversion_influencers = random.sample(list(influencers_df['id']), min(1500, len(influencers_df)))
    
    for influencer_id in conversion_influencers:
        if random.random() < 0.7:  # 70% chance this influencer has conversions
            num_conversions = random.randint(1, 3)
            
            for _ in range(num_conversions):
                brand = random.choice(brands)
                product = f"{brand} {random.choice(products[brand])}"
                campaign = random.choice(campaigns)
                
                # Get influencer data for realistic conversion modeling
                influencer = influencers_df[influencers_df['id'] == influencer_id].iloc[0]
                follower_count = influencer['follower_count']
                
                # Base conversion rate based on follower count (smaller influencers often have better conversion)
                base_conversion_rate = max(0.001, 0.01 - (follower_count / 10000000) * 0.005)
                actual_conversion_rate = base_conversion_rate * random.uniform(0.5, 2.0)
                
                # Estimate reach from posts
                influencer_posts = posts_df[posts_df['influencer_id'] == influencer_id]
                if len(influencer_posts) > 0:
                    avg_reach = influencer_posts['reach'].mean()
                else:
                    avg_reach = follower_count * 0.3
                
                orders = max(1, int(avg_reach * actual_conversion_rate))
                
                # Revenue per order varies by product type
                if 'Protein' in product or 'Mass Gainer' in product:
                    avg_order_value = random.randint(1500, 4000)
                elif 'Vitamin' in product or 'Biotin' in product:
                    avg_order_value = random.randint(500, 1500)
                else:
                    avg_order_value = random.randint(800, 2500)
                
                revenue = orders * avg_order_value
                
                # Random date
                start_date = datetime(2023, 8, 1)
                end_date = datetime(2023, 12, 31)
                random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
                
                tracking_data.append({
                    'tracking_id': tracking_id,
                    'source': 'influencer',
                    'campaign': campaign,
                    'influencer_id': influencer_id,
                    'product': product,
                    'brand': brand,
                    'date': random_date.strftime('%Y-%m-%d'),
                    'orders': orders,
                    'revenue': revenue
                })
                tracking_id += 1
    
    return pd.DataFrame(tracking_data)

@st.cache_data
def generate_payouts_data(influencers_df, tracking_df):
    """Generate payout data"""
    random.seed(42)
    np.random.seed(42)
    
    payouts = []
    payout_id = 1
    
    for _, influencer in influencers_df.iterrows():
        # Not all influencers will have payouts
        if random.random() < 0.75:  # 75% have payouts
            basis = random.choice(['post', 'order', 'post', 'order'])  # More likely to be post or order based
            
            if basis == 'post':
                # Fixed rate per post based on follower count
                if influencer['follower_count'] > 2000000:
                    rate = random.randint(80000, 150000)
                elif influencer['follower_count'] > 1000000:
                    rate = random.randint(40000, 80000)
                elif influencer['follower_count'] > 500000:
                    rate = random.randint(15000, 40000)
                else:
                    rate = random.randint(5000, 15000)
                
                # Estimate number of posts (simplified)
                num_posts = random.randint(1, 3)
                total_payout = rate * num_posts
                orders = None
                
            else:  # order-based
                rate = random.randint(50, 200)  # Per order commission
                
                # Get actual orders for this influencer
                influencer_orders = tracking_df[tracking_df['influencer_id'] == influencer['id']]['orders'].sum()
                if influencer_orders == 0:
                    influencer_orders = random.randint(10, 100)  # Fallback
                
                orders = influencer_orders
                total_payout = rate * orders
            
            payouts.append({
                'payout_id': payout_id,
                'influencer_id': influencer['id'],
                'basis': basis,
                'rate': rate,
                'orders': orders,
                'total_payout': total_payout
            })
            payout_id += 1
    
    return pd.DataFrame(payouts)

# --- LOAD DATA ---
@st.cache_data
def load_all_data():
    """Load all data with caching"""
    influencers_df = generate_influencers_data(2000)
    posts_df = generate_posts_data(influencers_df)
    tracking_data_df = generate_tracking_data(influencers_df, posts_df)
    payouts_df = generate_payouts_data(influencers_df, tracking_data_df)
    
    # Convert date columns
    posts_df['date'] = pd.to_datetime(posts_df['date'])
    tracking_data_df['date'] = pd.to_datetime(tracking_data_df['date'])
    
    return influencers_df, posts_df, tracking_data_df, payouts_df

# Load data
with st.spinner('Loading dashboard data...'):
    influencers, posts, tracking_data, payouts = load_all_data()

# --- CONSTANTS ---
BASELINE_ROAS = 2.5

# --- HEADER ---
st.markdown("""
<div class="title-container">
    <h1 class="title-text">🚀 Influencer Marketing ROI Dashboard</h1>
    <p class="subtitle-text">Advanced Analytics for HealthKart Brand Campaigns</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
st.sidebar.markdown("### 🎯 Campaign Filters")
brand_filter = st.sidebar.selectbox('🏷️ Select Brand', ['All'] + sorted(list(tracking_data['brand'].unique())))
platform_filter = st.sidebar.selectbox('📱 Select Platform', ['All'] + sorted(list(influencers['platform'].unique())))
campaign_filter = st.sidebar.selectbox('📈 Select Campaign', ['All'] + sorted(list(tracking_data['campaign'].unique())))
category_filter = st.sidebar.selectbox('🎭 Select Category', ['All'] + sorted(list(influencers['category'].unique())))

# Date range filter
st.sidebar.markdown("### 📅 Date Range")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(tracking_data['date'].min(), tracking_data['date'].max()),
    min_value=tracking_data['date'].min(),
    max_value=tracking_data['date'].max()
)

# Advanced filters
st.sidebar.markdown("### ⚙️ Advanced Filters")
min_followers = st.sidebar.slider('Minimum Followers', 0, 5000000, 0, 50000)
max_followers = st.sidebar.slider('Maximum Followers', 0, 10000000, 10000000, 50000)

# --- DATA PROCESSING ---
def process_data(influencers_df, posts_df, tracking_data_df, payouts_df, brand, platform, campaign, category, date_range, min_followers, max_followers):
    """Enhanced data processing with more filters"""
    
    # Apply date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        tracking_data_df = tracking_data_df[
            (tracking_data_df['date'] >= pd.to_datetime(start_date)) & 
            (tracking_data_df['date'] <= pd.to_datetime(end_date))
        ]
    
    # Apply filters
    if brand != 'All':
        tracking_data_df = tracking_data_df[tracking_data_df['brand'] == brand]
    if platform != 'All':
        influencers_df = influencers_df[influencers_df['platform'] == platform]
    if campaign != 'All':
        tracking_data_df = tracking_data_df[tracking_data_df['campaign'] == campaign]
    if category != 'All':
        influencers_df = influencers_df[influencers_df['category'] == category]
    
    # Follower range filter
    influencers_df = influencers_df[
        (influencers_df['follower_count'] >= min_followers) & 
        (influencers_df['follower_count'] <= max_followers)
    ]

    # Aggregate tracking data
    tracking_agg = tracking_data_df.groupby('influencer_id').agg(
        total_revenue=('revenue', 'sum'),
        total_orders=('orders', 'sum')
    ).reset_index()

    # Aggregate post data
    posts_agg = posts_df.groupby('influencer_id').agg(
        total_reach=('reach', 'sum'),
        total_likes=('likes', 'sum'),
        total_comments=('comments', 'sum'),
        post_count=('post_id', 'count')
    ).reset_index()

    # Merge dataframes
    df = pd.merge(influencers_df, tracking_agg, left_on='id', right_on='influencer_id', how='left')
    df = pd.merge(df, posts_agg, left_on='id', right_on='influencer_id', how='left')
    df = pd.merge(df, payouts_df[['influencer_id', 'total_payout']], left_on='id', right_on='influencer_id', how='left')

    # Fill NaNs for calculations
    df[['total_revenue', 'total_orders', 'total_reach', 'total_likes', 'total_comments', 'post_count', 'total_payout']] = df[['total_revenue', 'total_orders', 'total_reach', 'total_likes', 'total_comments', 'post_count', 'total_payout']].fillna(0)

    # Calculate metrics
    df['roas'] = df.apply(lambda row: row['total_revenue'] / row['total_payout'] if row['total_payout'] > 0 else 0, axis=1)
    df['engagement_rate'] = df.apply(lambda row: (row['total_likes'] + row['total_comments']) / row['total_reach'] * 100 if row['total_reach'] > 0 else 0, axis=1)
    df['cpm'] = df.apply(lambda row: (row['total_payout'] / row['total_reach']) * 1000 if row['total_reach'] > 0 else 0, axis=1)
    df['conversion_rate'] = df.apply(lambda row: (row['total_orders'] / row['total_reach']) * 100 if row['total_reach'] > 0 else 0, axis=1)

    return df.drop(columns=[col for col in df.columns if 'influencer_id' in col and col != 'id'])

# Process data
filtered_df = process_data(influencers, posts, tracking_data, payouts, brand_filter, platform_filter, campaign_filter, category_filter, date_range, min_followers, max_followers)

# --- KPIs ---
total_spend = filtered_df['total_payout'].sum()
total_revenue = filtered_df['total_revenue'].sum()
total_orders = filtered_df['total_orders'].sum()
total_reach = filtered_df['total_reach'].sum()
overall_roas = total_revenue / total_spend if total_spend > 0 else 0
incremental_roas = overall_roas - BASELINE_ROAS
avg_cpm = filtered_df['cpm'].mean() if len(filtered_df) > 0 else 0

# KPI Display
kpi_cols = st.columns(6)
with kpi_cols[0]:
    st.metric(label="💰 Total Spend", value=f"₹{total_spend:,.0f}")
with kpi_cols[1]:
    st.metric(label="💵 Total Revenue", value=f"₹{total_revenue:,.0f}")
with kpi_cols[2]:
    st.metric(label="📊 Overall ROAS", value=f"{overall_roas:.2f}x")
with kpi_cols[3]:
    st.metric(label="🎯 Incremental ROAS", value=f"{incremental_roas:.2f}x", delta=f"{incremental_roas:.2f}")
with kpi_cols[4]:
    st.metric(label="🛒 Total Orders", value=f"{total_orders:,.0f}")
with kpi_cols[5]:
    st.metric(label="👥 Total Reach", value=f"{total_reach/1_000_000:.1f}M")

st.markdown("---")

# --- ENHANCED CHARTS ---
chart_cols = st.columns([2, 1])

with chart_cols[0]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎯 Top Performers by ROAS")
    
    # Get top 20 performers
    top_performers = filtered_df.nlargest(20, 'roas')
    
    fig_roas = px.bar(
        top_performers,
        x='roas',
        y='name',
        orientation='h',
        title='Top 20 Influencers by Return on Ad Spend',
        labels={'name': 'Influencer', 'roas': 'ROAS (x)'},
        color='roas',
        color_continuous_scale='RdYlGn',
        text='roas'
    )
    fig_roas.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
    fig_roas.update_layout(
        height=600,
        title_x=0.5,
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_roas, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with chart_cols[1]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📱 Platform Distribution")
    
    platform_stats = filtered_df.groupby('platform').agg({
        'total_revenue': 'sum',
        'id': 'count'
    }).reset_index()
    platform_stats.columns = ['platform', 'revenue', 'influencer_count']
    
    fig_platform = px.pie(
        platform_stats,
        names='platform',
        values='revenue',
        title='Revenue Share by Platform',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_platform.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>'
    )
    fig_platform.update_layout(
        title_x=0.5,
        font=dict(size=11),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_platform, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Revenue and engagement trends
trend_cols = st.columns(2)

with trend_cols[0]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 Revenue Trend Over Time")
    
    # Filter tracking data based on current filters
    filtered_tracking = tracking_data.copy()
    if brand_filter != 'All':
        filtered_tracking = filtered_tracking[filtered_tracking['brand'] == brand_filter]
    if campaign_filter != 'All':
        filtered_tracking = filtered_tracking[filtered_tracking['campaign'] == campaign_filter]
    
    daily_revenue = filtered_tracking.groupby('date')['revenue'].sum().reset_index()
    
    fig_trend = px.line(
        daily_revenue,
        x='date',
        y='revenue',
        title='Daily Revenue Trend',
        labels={'date': 'Date', 'revenue': 'Revenue (₹)'}
    )
    fig_trend.update_traces(line_color='#667eea', line_width=3)
    fig_trend.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with trend_cols[1]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎭 Performance by Category")
    
    category_performance = filtered_df.groupby('category').agg({
        'total_revenue': 'sum',
        'total_payout': 'sum',
        'roas': 'mean',
        'id': 'count'
    }).reset_index()
    category_performance.columns = ['category', 'revenue', 'spend', 'avg_roas', 'count']
    
    fig_category = px.scatter(
        category_performance,
        x='spend',
        y='revenue',
        size='count',
        color='avg_roas',
        hover_name='category',
        title='Category Performance Matrix',
        labels={'spend': 'Total Spend (₹)', 'revenue': 'Total Revenue (₹)', 'count': 'Influencer Count'},
        color_continuous_scale='Viridis'
    )
    fig_category.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_category, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Advanced Analytics Section
st.markdown("## 📊 Advanced Analytics")

analytics_cols = st.columns(3)

with analytics_cols[0]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎯 ROAS Distribution")
    
    fig_hist = px.histogram(
        filtered_df[filtered_df['roas'] > 0],
        x='roas',
        nbins=30,
        title='ROAS Distribution Across Influencers',
        labels={'roas': 'ROAS (x)', 'count': 'Number of Influencers'}
    )
    fig_hist.add_vline(x=BASELINE_ROAS, line_dash="dash", line_color="red", 
                       annotation_text=f"Baseline ROAS ({BASELINE_ROAS}x)")
    fig_hist.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with analytics_cols[1]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💡 Engagement vs Conversion")
    
    # Filter out zero values for better visualization
    scatter_data = filtered_df[(filtered_df['engagement_rate'] > 0) & (filtered_df['conversion_rate'] > 0)]
    
    fig_scatter = px.scatter(
        scatter_data,
        x='engagement_rate',
        y='conversion_rate',
        size='follower_count',
        color='roas',
        hover_name='name',
        title='Engagement vs Conversion Rate',
        labels={'engagement_rate': 'Engagement Rate (%)', 'conversion_rate': 'Conversion Rate (%)'},
        color_continuous_scale='Plasma'
    )
    fig_scatter.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with analytics_cols[2]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🏆 Brand Performance")
    
    # Filter tracking data and aggregate by brand
    filtered_tracking_brand = tracking_data.copy()
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_tracking_brand = filtered_tracking_brand[
            (filtered_tracking_brand['date'] >= pd.to_datetime(start_date)) & 
            (filtered_tracking_brand['date'] <= pd.to_datetime(end_date))
        ]
    
    brand_performance = filtered_tracking_brand.groupby('brand').agg({
        'revenue': 'sum',
        'orders': 'sum'
    }).reset_index()
    
    fig_brand = px.bar(
        brand_performance,
        x='brand',
        y='revenue',
        title='Revenue by Brand',
        labels={'brand': 'Brand', 'revenue': 'Revenue (₹)'},
        color='revenue',
        color_continuous_scale='Blues'
    )
    fig_brand.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_brand, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PERFORMANCE INSIGHTS ---
st.markdown("## 🔍 Performance Insights")

insight_cols = st.columns(2)

with insight_cols[0]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("⭐ Top Performers Table")
    
    # Get top 10 performers with key metrics
    top_10 = filtered_df.nlargest(10, 'roas')[['name', 'platform', 'category', 'follower_count', 'total_payout', 'total_revenue', 'roas', 'engagement_rate']].copy()
    
    # Format for display
    top_10['follower_count'] = top_10['follower_count'].apply(lambda x: f"{x/1_000_000:.1f}M" if x >= 1_000_000 else f"{x/1_000:.0f}K")
    top_10['total_payout'] = top_10['total_payout'].apply(lambda x: f"₹{x:,.0f}")
    top_10['total_revenue'] = top_10['total_revenue'].apply(lambda x: f"₹{x:,.0f}")
    top_10['roas'] = top_10['roas'].apply(lambda x: f"{x:.2f}x")
    top_10['engagement_rate'] = top_10['engagement_rate'].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(
        top_10.rename(columns={
            'name': 'Influencer',
            'platform': 'Platform',
            'category': 'Category',
            'follower_count': 'Followers',
            'total_payout': 'Spend',
            'total_revenue': 'Revenue',
            'roas': 'ROAS',
            'engagement_rate': 'Engagement'
        }),
        use_container_width=True,
        height=400
    )
    st.markdown('</div>', unsafe_allow_html=True)

with insight_cols[1]:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📋 Key Insights & Recommendations")
    
    # Calculate insights
    high_performers = len(filtered_df[filtered_df['roas'] >= BASELINE_ROAS])
    total_influencers = len(filtered_df[filtered_df['total_payout'] > 0])
    success_rate = (high_performers / total_influencers * 100) if total_influencers > 0 else 0
    
    best_platform = filtered_df.groupby('platform')['roas'].mean().idxmax() if len(filtered_df) > 0 else "N/A"
    best_category = filtered_df.groupby('category')['roas'].mean().idxmax() if len(filtered_df) > 0 else "N/A"
    
    avg_engagement = filtered_df['engagement_rate'].mean()
    high_engagement_threshold = avg_engagement * 1.5
    
    insights_html = f"""
    <div style="padding: 1rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 10px; color: white; margin-bottom: 1rem;">
        <h4>📈 Performance Summary</h4>
        <ul style="list-style: none; padding: 0;">
            <li>✅ <strong>{success_rate:.1f}%</strong> of influencers exceed baseline ROAS</li>
            <li>🏆 Best performing platform: <strong>{best_platform}</strong></li>
            <li>🎯 Top category: <strong>{best_category}</strong></li>
            <li>💡 Average engagement rate: <strong>{avg_engagement:.2f}%</strong></li>
        </ul>
    </div>
    
    <div style="padding: 1rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 10px; color: white;">
        <h4>🚀 Recommendations</h4>
        <ul style="list-style: none; padding: 0;">
            <li>🎯 Focus budget on influencers with ROAS > {BASELINE_ROAS:.1f}x</li>
            <li>📱 Increase investment in <strong>{best_platform}</strong> platform</li>
            <li>🔍 Target <strong>{best_category}</strong> category influencers</li>
            <li>⚡ Prioritize influencers with >3% engagement rate</li>
        </ul>
    </div>
    """
    
    st.markdown(insights_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- DETAILED PERFORMANCE TABLE ---
st.markdown("## 📊 Detailed Performance Analysis")
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

# Performance filter options
perf_cols = st.columns(4)
with perf_cols[0]:
    sort_by = st.selectbox('Sort by', ['ROAS', 'Revenue', 'Engagement Rate', 'Followers', 'Orders'])
with perf_cols[1]:
    sort_order = st.selectbox('Order', ['Descending', 'Ascending'])
with perf_cols[2]:
    min_roas_filter = st.number_input('Min ROAS', min_value=0.0, max_value=10.0, value=0.0, step=0.1)
with perf_cols[3]:
    show_rows = st.selectbox('Show rows', [20, 50, 100, 200])

# Filter and sort data
detailed_df = filtered_df[filtered_df['roas'] >= min_roas_filter].copy()

sort_mapping = {
    'ROAS': 'roas',
    'Revenue': 'total_revenue', 
    'Engagement Rate': 'engagement_rate',
    'Followers': 'follower_count',
    'Orders': 'total_orders'
}

detailed_df = detailed_df.sort_values(
    sort_mapping[sort_by], 
    ascending=(sort_order == 'Ascending')
).head(show_rows)

# Format display data
display_detailed = detailed_df[[
    'name', 'platform', 'category', 'follower_count', 'total_payout', 
    'total_revenue', 'total_orders', 'roas', 'engagement_rate', 'cpm', 'conversion_rate'
]].copy()

display_detailed['follower_count'] = display_detailed['follower_count'].apply(
    lambda x: f"{x/1_000_000:.1f}M" if x >= 1_000_000 else f"{x/1_000:.0f}K"
)
display_detailed['total_payout'] = display_detailed['total_payout'].apply(lambda x: f"₹{x:,.0f}")
display_detailed['total_revenue'] = display_detailed['total_revenue'].apply(lambda x: f"₹{x:,.0f}")
display_detailed['roas'] = display_detailed['roas'].apply(lambda x: f"{x:.2f}x")
display_detailed['engagement_rate'] = display_detailed['engagement_rate'].apply(lambda x: f"{x:.2f}%")
display_detailed['cpm'] = display_detailed['cpm'].apply(lambda x: f"₹{x:.2f}")
display_detailed['conversion_rate'] = display_detailed['conversion_rate'].apply(lambda x: f"{x:.3f}%")

st.dataframe(
    display_detailed.rename(columns={
        'name': 'Influencer',
        'platform': 'Platform', 
        'category': 'Category',
        'follower_count': 'Followers',
        'total_payout': 'Spend',
        'total_revenue': 'Revenue',
        'total_orders': 'Orders',
        'roas': 'ROAS',
        'engagement_rate': 'Engagement %',
        'cpm': 'CPM',
        'conversion_rate': 'Conversion %'
    }),
    use_container_width=True,
    height=600
)

st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
    <h3>💡 Dashboard Statistics</h3>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div><strong>{:,}</strong><br>Total Influencers</div>
        <div><strong>{:,}</strong><br>Active Campaigns</div>
        <div><strong>{:,}</strong><br>Posts Analyzed</div>
        <div><strong>{:,}</strong><br>Brands Tracked</div>
    </div>
</div>
""".format(
    len(influencers),
    len(tracking_data['campaign'].unique()),
    len(posts),
    len(tracking_data['brand'].unique())
), unsafe_allow_html=True)
