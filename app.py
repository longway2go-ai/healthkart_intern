import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Influencer Marketing ROI Dashboard",
    page_icon="🚀",
    layout="wide"
)

# --- DATA SIMULATION (using Pandas DataFrames) ---
@st.cache_data
def load_data():
    """Loads and caches the data for the app."""
    influencers_df = pd.DataFrame([
        { 'id': 1, 'name': 'Aarav Sharma', 'category': 'Fitness', 'gender': 'Male', 'follower_count': 1200000, 'platform': 'Instagram' },
        { 'id': 2, 'name': 'Priya Patel', 'category': 'Wellness', 'gender': 'Female', 'follower_count': 850000, 'platform': 'YouTube' },
        { 'id': 3, 'name': 'Rohan Das', 'category': 'Bodybuilding', 'gender': 'Male', 'follower_count': 2500000, 'platform': 'Instagram' },
        { 'id': 4, 'name': 'Sneha Reddy', 'category': 'Yoga', 'gender': 'Female', 'follower_count': 500000, 'platform': 'Instagram' },
        { 'id': 5, 'name': 'Vikram Singh', 'category': 'Nutrition', 'gender': 'Male', 'follower_count': 750000, 'platform': 'YouTube' },
        { 'id': 6, 'name': 'Ananya Gupta', 'category': 'Lifestyle', 'gender': 'Female', 'follower_count': 1500000, 'platform': 'Twitter' },
        { 'id': 7, 'name': 'Karan Malhotra', 'category': 'Fitness', 'gender': 'Male', 'follower_count': 950000, 'platform': 'Twitter' },
    ])

    posts_df = pd.DataFrame([
        { 'post_id': 101, 'influencer_id': 1, 'platform': 'Instagram', 'date': '2023-10-05', 'url': 'http://insta.com/p1', 'caption': 'Loving my new MuscleBlaze protein!', 'reach': 250000, 'likes': 25000, 'comments': 1200 },
        { 'post_id': 102, 'influencer_id': 2, 'platform': 'YouTube', 'date': '2023-10-08', 'url': 'http://youtube.com/v1', 'caption': 'My daily HKVitals routine', 'reach': 150000, 'likes': 18000, 'comments': 2500 },
        { 'post_id': 103, 'influencer_id': 3, 'platform': 'Instagram', 'date': '2023-10-12', 'url': 'http://insta.com/p2', 'caption': 'Gritzo for the win!', 'reach': 800000, 'likes': 90000, 'comments': 4500 },
        { 'post_id': 104, 'influencer_id': 4, 'platform': 'Instagram', 'date': '2023-10-15', 'url': 'http://insta.com/p3', 'caption': 'Yoga + HKVitals = perfect balance', 'reach': 120000, 'likes': 15000, 'comments': 800 },
        { 'post_id': 105, 'influencer_id': 5, 'platform': 'YouTube', 'date': '2023-10-20', 'url': 'http://youtube.com/v2', 'caption': 'Unboxing MuscleBlaze supplements', 'reach': 200000, 'likes': 22000, 'comments': 1800 },
        { 'post_id': 106, 'influencer_id': 6, 'platform': 'Twitter', 'date': '2023-10-22', 'url': 'http://twitter.com/t1', 'caption': 'Quick thoughts on Gritzo nutrition for kids.', 'reach': 300000, 'likes': 5000, 'comments': 600 },
        { 'post_id': 107, 'influencer_id': 1, 'platform': 'Instagram', 'date': '2023-11-02', 'url': 'http://insta.com/p4', 'caption': 'Fueling my workouts with MuscleBlaze', 'reach': 300000, 'likes': 32000, 'comments': 1500 },
        { 'post_id': 108, 'influencer_id': 7, 'platform': 'Twitter', 'date': '2023-11-05', 'url': 'http://twitter.com/t2', 'caption': '#MuscleBlaze #ad', 'reach': 200000, 'likes': 3000, 'comments': 400 },
    ])

    tracking_data_df = pd.DataFrame([
        { 'tracking_id': 1001, 'source': 'influencer', 'campaign': 'DiwaliSale23', 'influencer_id': 1, 'product': 'MuscleBlaze Whey Protein', 'brand': 'MuscleBlaze', 'date': '2023-10-06', 'orders': 120, 'revenue': 240000 },
        { 'tracking_id': 1002, 'source': 'influencer', 'campaign': 'DiwaliSale23', 'influencer_id': 2, 'product': 'HKVitals Multivitamin', 'brand': 'HKVitals', 'date': '2023-10-09', 'orders': 250, 'revenue': 125000 },
        { 'tracking_id': 1003, 'source': 'influencer', 'campaign': 'WinterBulkUp23', 'influencer_id': 3, 'product': 'Gritzo SuperMilk', 'brand': 'Gritzo', 'date': '2023-10-13', 'orders': 80, 'revenue': 96000 },
        { 'tracking_id': 1004, 'source': 'influencer', 'campaign': 'DiwaliSale23', 'influencer_id': 4, 'product': 'HKVitals Biotin', 'brand': 'HKVitals', 'date': '2023-10-16', 'orders': 150, 'revenue': 90000 },
        { 'tracking_id': 1005, 'source': 'influencer', 'campaign': 'WinterBulkUp23', 'influencer_id': 5, 'product': 'MuscleBlaze Creatine', 'brand': 'MuscleBlaze', 'date': '2023-10-21', 'orders': 180, 'revenue': 162000 },
        { 'tracking_id': 1006, 'source': 'influencer', 'campaign': 'WinterBulkUp23', 'influencer_id': 6, 'product': 'Gritzo SuperMilk', 'brand': 'Gritzo', 'date': '2023-10-23', 'orders': 50, 'revenue': 60000 },
        { 'tracking_id': 1007, 'source': 'influencer', 'campaign': 'WinterBulkUp23', 'influencer_id': 1, 'product': 'MuscleBlaze Pre-Workout', 'brand': 'MuscleBlaze', 'date': '2023-11-03', 'orders': 150, 'revenue': 210000 },
        { 'tracking_id': 1008, 'source': 'influencer', 'campaign': 'WinterBulkUp23', 'influencer_id': 7, 'product': 'MuscleBlaze BCAA', 'brand': 'MuscleBlaze', 'date': '2023-11-06', 'orders': 70, 'revenue': 77000 },
    ])

    payouts_df = pd.DataFrame([
        { 'payout_id': 201, 'influencer_id': 1, 'basis': 'post', 'rate': 50000, 'orders': None, 'total_payout': 100000 },
        { 'payout_id': 202, 'influencer_id': 2, 'basis': 'order', 'rate': 100, 'orders': 250, 'total_payout': 25000 },
        { 'payout_id': 203, 'influencer_id': 3, 'basis': 'post', 'rate': 100000, 'orders': None, 'total_payout': 100000 },
        { 'payout_id': 204, 'influencer_id': 4, 'basis': 'order', 'rate': 80, 'orders': 150, 'total_payout': 12000 },
        { 'payout_id': 205, 'influencer_id': 5, 'basis': 'post', 'rate': 60000, 'orders': None, 'total_payout': 60000 },
        { 'payout_id': 206, 'influencer_id': 6, 'basis': 'post', 'rate': 30000, 'orders': None, 'total_payout': 30000 },
        { 'payout_id': 207, 'influencer_id': 7, 'basis': 'order', 'rate': 90, 'orders': 70, 'total_payout': 6300 },
    ])
    
    # Convert date columns to datetime objects
    posts_df['date'] = pd.to_datetime(posts_df['date'])
    tracking_data_df['date'] = pd.to_datetime(tracking_data_df['date'])
    
    return influencers_df, posts_df, tracking_data_df, payouts_df

influencers, posts, tracking_data, payouts = load_data()

# --- CONSTANTS ---
BASELINE_ROAS = 2.5

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
brand_filter = st.sidebar.selectbox('Select Brand', ['All'] + list(tracking_data['brand'].unique()))
platform_filter = st.sidebar.selectbox('Select Platform', ['All'] + list(influencers['platform'].unique()))
campaign_filter = st.sidebar.selectbox('Select Campaign', ['All'] + list(tracking_data['campaign'].unique()))

# --- DATA PROCESSING ---
def process_data(influencers_df, posts_df, tracking_data_df, payouts_df, brand, platform, campaign):
    """Filters and processes data based on user selection."""
    
    # Apply filters
    if brand != 'All':
        tracking_data_df = tracking_data_df[tracking_data_df['brand'] == brand]
    if platform != 'All':
        influencers_df = influencers_df[influencers_df['platform'] == platform]
    if campaign != 'All':
        tracking_data_df = tracking_data_df[tracking_data_df['campaign'] == campaign]

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

    return df.drop(columns=['influencer_id_x', 'influencer_id_y', 'influencer_id'])


filtered_df = process_data(influencers, posts, tracking_data, payouts, brand_filter, platform_filter, campaign_filter)

# --- DASHBOARD UI ---
st.title("Influencer Marketing ROI Dashboard")
st.markdown("Analyze campaign performance and ROI for HealthKart brands.")
st.markdown("---")

# --- KPIs ---
total_spend = filtered_df['total_payout'].sum()
total_revenue = filtered_df['total_revenue'].sum()
overall_roas = total_revenue / total_spend if total_spend > 0 else 0
incremental_roas = overall_roas - BASELINE_ROAS

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Total Spend", value=f"₹{total_spend:,.0f}")
kpi2.metric(label="Total Revenue", value=f"₹{total_revenue:,.0f}")
kpi3.metric(label="Overall ROAS", value=f"{overall_roas:.2f}x")
kpi4.metric(label="Incremental ROAS", value=f"{incremental_roas:.2f}x", delta=f"{incremental_roas:.2f} vs baseline")

st.markdown("---")

# --- CHARTS ---
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("ROAS by Influencer")
    roas_chart_df = filtered_df.sort_values('roas', ascending=False)
    roas_chart_df['color'] = roas_chart_df['roas'].apply(lambda x: 'green' if x >= BASELINE_ROAS else 'red')

    fig_roas = px.bar(
        roas_chart_df,
        x='name',
        y='roas',
        title='Return on Ad Spend per Influencer',
        labels={'name': 'Influencer', 'roas': 'ROAS (x)'},
        color='color',
        color_discrete_map={'green': '#10B981', 'red': '#EF4444'},
        text_auto='.2f'
    )
    fig_roas.update_layout(showlegend=False, title_x=0.5)
    st.plotly_chart(fig_roas, use_container_width=True)

with col2:
    st.subheader("Revenue by Platform")
    platform_revenue = filtered_df.groupby('platform')['total_revenue'].sum().reset_index()
    fig_pie = px.pie(
        platform_revenue,
        names='platform',
        values='total_revenue',
        title='Share of Revenue by Platform',
        hole=0.3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(showlegend=False, title_x=0.5)
    st.plotly_chart(fig_pie, use_container_width=True)

# Revenue Over Time Chart
st.subheader("Revenue Over Time")
time_series_df = tracking_data.groupby('date')['revenue'].sum().reset_index()
fig_line = px.line(
    time_series_df,
    x='date',
    y='revenue',
    title='Daily Revenue from Campaigns',
    labels={'date': 'Date', 'revenue': 'Revenue (₹)'}
)
fig_line.update_layout(title_x=0.5)
st.plotly_chart(fig_line, use_container_width=True)


# --- INFLUENCER PERFORMANCE TABLE ---
st.subheader("Influencer Performance Details")

# Format the dataframe for display
display_df = filtered_df[[
    'name', 'platform', 'follower_count', 'total_payout', 'total_revenue', 'roas', 'engagement_rate'
]].copy()

display_df['follower_count'] = display_df['follower_count'].apply(lambda x: f"{(x/1_000_000):.2f}M")
display_df['total_payout'] = display_df['total_payout'].apply(lambda x: f"₹{x:,.0f}")
display_df['total_revenue'] = display_df['total_revenue'].apply(lambda x: f"₹{x:,.0f}")
display_df['roas'] = display_df['roas'].apply(lambda x: f"{x:.2f}x")
display_df['engagement_rate'] = display_df['engagement_rate'].apply(lambda x: f"{x:.2f}%")

st.dataframe(
    display_df.rename(columns={
        'name': 'Influencer',
        'platform': 'Platform',
        'follower_count': 'Followers',
        'total_payout': 'Spend',
        'total_revenue': 'Revenue',
        'roas': 'ROAS',
        'engagement_rate': 'Eng. Rate'
    }).sort_values(by='ROAS', ascending=False).reset_index(drop=True),
    use_container_width=True
)
