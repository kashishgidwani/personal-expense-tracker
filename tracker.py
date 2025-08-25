import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from dataclasses import dataclass
from typing import List, Dict
import uuid

# Configure page
st.set_page_config(
    page_title="💸 Expense Tracker - Our Finances",
    page_icon="💰",
    layout="centered",  # Changed to centered for better mobile experience
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar on mobile
)

# Custom CSS for fun styling with lavender and pink theme
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif !important;
        color: #2e2e2e;
    }

    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #fce3f3 0%, #e9e4ff 100%) !important;
        color: #2e2e2e;
    }

    /* Headings */
    h1, h2, h3, h4 {
        font-weight: 600;
        color: #5a2d82; /* Deep lavender-purple */
    }

    /* Labels and text */
    p, div, span, label {
        font-size: 16px;
        color: #444;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff9fcf, #c7a7ff);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(200, 100, 200, 0.3);
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #e1c4ff;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #c7a7ff;
        box-shadow: 0 4px 12px rgba(200, 100, 200, 0.2);
    }
    
    .category-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 500;
        margin: 8px 0;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .food-dining { 
        background: linear-gradient(135deg, #ffe5e5, #ffcccc); 
        color: #c62828; 
        border: 1px solid #ffb3b3;
    }
    .transportation { 
        background: linear-gradient(135deg, #e3f2fd, #bbdefb); 
        color: #1565c0; 
        border: 1px solid #90caf9;
    }
    .shopping { 
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9); 
        color: #2e7d32; 
        border: 1px solid #a5d6a7;
    }
    .entertainment { 
        background: linear-gradient(135deg, #f3e5f5, #e1bee7); 
        color: #6a1b9a; 
        border: 1px solid #ce93d8;
    }
    .bills-utilities { 
        background: linear-gradient(135deg, #fffde7, #fff9c4); 
        color: #f9a825; 
        border: 1px solid #fff59d;
    }
    .healthcare { 
        background: linear-gradient(135deg, #e1f5fe, #b3e5fc); 
        color: #0277bd; 
        border: 1px solid #81d4fa;
    }
    .education { 
        background: linear-gradient(135deg, #e0f2f1, #b2dfdb); 
        color: #00695c; 
        border: 1px solid #80cbc4;
    }
    .travel { 
        background: gradient(135deg, #fff3e0, #ffe0b2); 
        color: #e65100; 
        border: 1px solid #ffcc02;
    }
    .other { 
        background: linear-gradient(135deg, #f5f5f5, #e0e0e0); 
        color: #424242; 
        border: 1px solid #bdbdbd;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.75);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 182, 193, 0.4);
        box-shadow: 0 6px 16px rgba(200, 100, 200, 0.15);
        margin: 0.5rem 0;
    }
    
    .big-number {
        font-size: 1.8rem;
        font-weight: 600;
        color: #d63384;
    }
    
    .emoji-header {
        font-size: 1.1rem;
        color: #6c3eb0;
        margin-bottom: 0.5rem;
    }
    
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #e1c4ff;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #ff9fcf;
        box-shadow: 0 0 0 3px rgba(255, 159, 207, 0.2);
    }


    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.55);
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 182, 193, 0.3);
        box-shadow: 0 4px 10px rgba(200, 100, 200, 0.1);
        margin: 0.5rem 0;
    }

    .big-number {
        font-size: 1.8rem;
        font-weight: 600;
        color: #d63384; /* Pink highlight */
    }

    .emoji-header {
        font-size: 1.1rem;
        color: #6c3eb0;
        margin-bottom: 0.5rem;
    }

    /* Radio buttons & Select boxes */
    .stRadio > div, .stSelectbox > div > div, .stMultiSelect > div > div {
        background: white;
        border: 1px solid #d8c4f4;
        border-radius: 12px;
        padding: 0.4rem 0.6rem;
        color: #333;
    }

    /* Dataframes & tables */
    .dataframe {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 12px;
        padding: 0.5rem;
    }

    /* Footer tips box */
    .footer-box {
        background: linear-gradient(135deg, #f6d9ff, #ffe1f3);
        border-radius: 16px;
        padding: 15px;
        margin-top: 25px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(200, 100, 200, 0.15);
    }
    .custom-label {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 200 !important;
    font-size: 16px !important;
    color: #2e2e2e !important;
    margin-bottom: 12px !important;
    display: block !important;
}
    
</style>
""", unsafe_allow_html=True)


@dataclass
class Expense:
    id: str
    amount: float
    description: str
    category: str
    expense_type: str  # personal, shared, work
    person: str
    date: datetime
    shared_with: List[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'category': self.category,
            'expense_type': self.expense_type,
            'person': self.person,
            'date': self.date.isoformat(),
            'shared_with': self.shared_with or []
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            amount=data['amount'],
            description=data['description'],
            category=data['category'],
            expense_type=data['expense_type'],
            person=data['person'],
            date=datetime.fromisoformat(data['date']),
            shared_with=data['shared_with']
        )

class ExpenseTracker:
    def __init__(self):
        import os
        # Set data file path - works in both local and deployed environments
        self.data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses_data.json")
        
        # Initialize session state
        if 'expenses' not in st.session_state:
            st.session_state.expenses = []
        if 'friends' not in st.session_state:
            st.session_state.friends = ['Me', 'Boyfriend']
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
            
        # Load data if not already loaded
        if not st.session_state.data_loaded:
            data = self.load_data()
            st.session_state.expenses = data.get('expenses', [])
            st.session_state.friends = data.get('friends', ['Me', 'Boyfriend'])
            st.session_state.data_loaded = True
    
    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, use default empty values
            default_data = {'expenses': [], 'friends': ['Me', 'Boyfriend']}
            # Create the file with default values
            with open(self.data_file, 'w') as file:
                json.dump(default_data, file, indent=4)
            return default_data
    
    def save_data(self):
        try:
            data = {
                'expenses': st.session_state.expenses,
                'friends': st.session_state.friends
            }
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            st.error(f"Error saving data: {str(e)}")
            return False
    
    def add_expense(self, expense: Expense):
        st.session_state.expenses.append(expense.to_dict())
        self.save_data()
    
    def get_expenses_df(self):
        if not st.session_state.expenses:
            return pd.DataFrame()
        
        df = pd.DataFrame(st.session_state.expenses)
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def add_friend(self, friend_name):
        if friend_name and friend_name not in st.session_state.friends:
            st.session_state.friends.append(friend_name)
            self.save_data()

# Initialize tracker
tracker = ExpenseTracker()

# Navigation for mobile-friendly experience
st.markdown("<h1 style='text-align: center; color: #333;'>💰 Our Expense Tracker</h1>", unsafe_allow_html=True)

# Create tabs for navigation instead of sidebar for better mobile experience
page = st.radio("📱 Navigation", 
               ["🏠 Dashboard", "➕ Add Expense", "👥 People", "📊 Reports", "🎯 Split Expenses"],
               horizontal=True)

# Show who's using the app
st.markdown("<div style='text-align: center; margin-bottom: 20px;'>Tracking expenses for:</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div style='text-align: center;'>👧🏻 {st.session_state.friends[0]}</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align: center;'>👦🏻 {st.session_state.friends[1]}</div>", unsafe_allow_html=True)

# Main content based on selected page
if page == "🏠 Dashboard":
    st.title("💸 Our Financial Dashboard")
    st.markdown("*Track our spending together!*")
    
    # Add custom CSS for dropdown styling
    st.markdown("""
    <style>
    /* Style the dropdown menus in dashboard */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #e1c4ff !important;
        border-radius: 12px !important;
        color: #2e2e2e !important;
    }
    
    div[data-baseweb="select"]:hover > div {
        border-color: #c7a7ff !important;
        box-shadow: 0 4px 12px rgba(200, 100, 200, 0.2) !important;
    }
    
    /* Style the dropdown popup menu */
    div[data-baseweb="popover"] > div {
        background-color: #ffffff !important;
        border: 2px solid #e1c4ff !important;
        border-radius: 12px !important;
        padding: 5px !important;
        box-shadow: 0 4px 12px rgba(200, 100, 200, 0.2) !important;
    }
    
    /* Style dropdown options */
    div[data-baseweb="popover"] li {
        background-color: #ffffff !important;
        color: #2e2e2e !important;
        border-radius: 8px !important;
        padding: 10px !important;
        margin: 3px 0 !important;
        transition: background 0.2s ease-in-out;
    }
    
    /* Hover effect for dropdown options */
    div[data-baseweb="popover"] li:hover {
        background-color: #f3e8ff !important;
        color: #5b21b6 !important;
        font-weight: 600 !important;
    }
    /* Custom labels styling */
    /* Select boxes (dropdowns) */
div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #e1c4ff !important;
    border-radius: 12px !important;
    color: #2e2e2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    min-height: 56px !important;
    padding: 16px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    line-height: 1.2 !important;
}

div[data-baseweb="select"]:hover > div {
    border-color: #c7a7ff !important;
    box-shadow: 0 4px 12px rgba(200, 100, 200, 0.2) !important;
}

    </style>
    """, unsafe_allow_html=True)
    
    df = tracker.get_expenses_df()
    
    if df.empty:
        st.warning("📝 No expenses yet! Add some to see your financial chaos unfold.")
        st.balloons()
    else:
        # Time filters
        col1, col2 = st.columns(2)
        with col1:
            days_filter = st.selectbox("📅 Time Period", [7, 30, 90, 365], index=1)
        with col2:
            person_filter = st.selectbox("👤 Person", ["All"] + st.session_state.friends)
        
        # Filter data
        cutoff_date = datetime.now() - timedelta(days=days_filter)
        filtered_df = df[df['date'] >= cutoff_date]
        
        if person_filter != "All":
            filtered_df = filtered_df[filtered_df['person'] == person_filter]
        
        if not filtered_df.empty:
            # Summary metrics
            total_spent = filtered_df['amount'].sum()
            avg_daily = total_spent / days_filter
            expense_count = len(filtered_df)
            avg_expense = filtered_df['amount'].mean()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                emoji = "😱" if total_spent > 1000 else "😅" if total_spent > 500 else "😊"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="emoji-header">{emoji} Total Damage</div>
                    <div class="big-number">₹{total_spent:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                emoji = "🔥" if avg_daily > 50 else "⚡" if avg_daily > 20 else "🐌"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="emoji-header">{emoji} Daily Burn</div>
                    <div class="big-number">₹{avg_daily:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                emoji = "🎯" if expense_count > 50 else "📈" if expense_count > 20 else "📊"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="emoji-header">{emoji} Transactions</div>
                    <div class="big-number">{expense_count}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                emoji = "💎" if avg_expense > 100 else "💰" if avg_expense > 50 else "🪙"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="emoji-header">{emoji} Avg Expense</div>
                    <div class="big-number">₹{avg_expense:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💸 Spending by Category")
                category_spending = filtered_df.groupby('category')['amount'].sum().reset_index()
                fig_pie = px.pie(category_spending, values='amount', names='category',
                               title="Where Did Our Money Go?",
                               color_discrete_sequence=px.colors.qualitative.Set3)
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.subheader("👥 Spending by Person")
                person_spending = filtered_df.groupby('person')['amount'].sum().reset_index()
                fig_bar = px.bar(person_spending, x='person', y='amount',
                               title="Who's the Biggest Spender?",
                               color='amount',
                               color_continuous_scale='Reds')
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Spending timeline
            st.subheader("📈 Spending Timeline")
            daily_spending = filtered_df.groupby(filtered_df['date'].dt.date)['amount'].sum().reset_index()
            fig_line = px.line(daily_spending, x='date', y='amount',
                             title="Daily Financial Damage",
                             markers=True)
            fig_line.update_traces(line_color='#ff6b6b', marker_color='#ee5a52')
            st.plotly_chart(fig_line, use_container_width=True)
            
            # Recent expenses
            st.subheader("🔥 Recent Money Disappearances")
            recent_expenses = filtered_df.nlargest(5, 'date')[['date', 'person', 'description', 'category', 'amount']]
            recent_expenses['date'] = recent_expenses['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(recent_expenses, use_container_width=True)

elif page == "➕ Add Expense":
    st.title("➕ Add New Financial Mistake")
    st.markdown("*Track another way you spent money!*")
    st.markdown("""
<style>
/* ===============================
   UNIFIED FORM INPUT STYLING
   All inputs will have the same height and appearance
   =============================== */

/* Select boxes (dropdowns) */
div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #e1c4ff !important;
    border-radius: 12px !important;
    color: #2e2e2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    min-height: 56px !important;
    padding: 16px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    line-height: 1.2 !important;
}

div[data-baseweb="select"]:hover > div {
    border-color: #c7a7ff !important;
    box-shadow: 0 4px 12px rgba(200, 100, 200, 0.2) !important;
}

/* Text and Number inputs - Match select box size */
.stNumberInput > div > div > input, 
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #e1c4ff !important;
    border-radius: 12px !important;
    color: #2e2e2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    min-height: 56px !important; /* Same as select boxes */
    padding: 16px !important; /* Same as select boxes */
    width: 100% !important;
    box-sizing: border-box !important;
    line-height: 1.2 !important;
}

.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {
    border-color: #ff9fcf !important;
    box-shadow: 0 0 0 3px rgba(255, 159, 207, 0.2) !important;
    outline: none !important;
}

.stNumberInput > div > div > input:hover,
.stTextInput > div > div > input:hover {
    border-color: #c7a7ff !important;
}

/* Date input - Match other inputs */
.stDateInput > div > div > input {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #e1c4ff !important;
    border-radius: 12px !important;
    color: #2e2e2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    min-height: 56px !important; /* Same as others */
    padding: 16px !important; /* Same as others */
    width: 100% !important;
    box-sizing: border-box !important;
    line-height: 1.2 !important;
}

.stDateInput > div > div > input:focus {
    border-color: #ff9fcf !important;
    box-shadow: 0 0 0 3px rgba(255, 159, 207, 0.2) !important;
    outline: none !important;
}

.stDateInput > div > div > input:hover {
    border-color: #c7a7ff !important;
}

/* Multi-select inputs */
.stMultiSelect > div > div {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #e1c4ff !important;
    border-radius: 12px !important;
    color: #2e2e2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    min-height: 56px !important; /* Same as others */
    padding: 16px !important; /* Same as others */
    width: 100% !important;
    box-sizing: border-box !important;
    line-height: 1.2 !important;
}

.stMultiSelect > div > div:focus {
    border-color: #ff9fcf !important;
    box-shadow: 0 0 0 3px rgba(255, 159, 207, 0.2) !important;
}

.stMultiSelect > div > div:hover {
    border-color: #c7a7ff !important;
}

/* Ensure the selected text is properly positioned in select boxes */
div[data-baseweb="select"] > div > div {
    color: #2e2e2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    line-height: 1.2 !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    height: auto !important;
    overflow: visible !important;
}

/* Fix for the selected value span */
div[data-baseweb="select"] > div span {
    color: #2e2e2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    line-height: 1.2 !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    display: inline-block !important;
    vertical-align: middle !important;
}

/* Ensure dropdown arrow doesn't interfere */
div[data-baseweb="select"] > div > div:last-child {
    flex-shrink: 0 !important;
    margin-left: 8px !important;
}

/* ===============================
   DROPDOWN MENU STYLING
   =============================== */

/* Fix dropdown menu positioning and sizing */
div[data-baseweb="popover"] {
    z-index: 1000 !important;
}

div[data-baseweb="popover"] > div {
    background-color: #ffffff !important;
    border: 2px solid #e1c4ff !important;
    border-radius: 12px !important;
    padding: 8px !important;
    box-shadow: 0 4px 12px rgba(200, 100, 200, 0.2) !important;
    min-width: 100% !important;
}

/* Dropdown options styling */
div[data-baseweb="popover"] li {
    background-color: #ffffff !important;
    color: #2e2e2e !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    margin: 4px 0 !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    line-height: 1.2 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
    overflow: visible !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #f3e8ff !important;
    color: #5b21b6 !important;
    font-weight: 600 !important;
}

/* ===============================
   CATEGORY COLORS FOR DROPDOWN OPTIONS
   =============================== */

/* Food & Dining */
div[data-baseweb="popover"] li:nth-child(1) {
    background-color: #fff4e6 !important;
    color: #d35400 !important;
}

/* Transportation */
div[data-baseweb="popover"] li:nth-child(2) {
    background-color: #e6f7ff !important;
    color: #005580 !important;
}

/* Shopping */
div[data-baseweb="popover"] li:nth-child(3) {
    background-color: #fbefff !important;
    color: #6a1b9a !important;
}

/* Entertainment */
div[data-baseweb="popover"] li:nth-child(4) {
    background-color: #fff9db !important;
    color: #b36b00 !important;
}

/* Bills & Utilities */
div[data-baseweb="popover"] li:nth-child(5) {
    background-color: #edf7ed !important;
    color: #1b5e20 !important;
}

/* Healthcare */
div[data-baseweb="popover"] li:nth-child(6) {
    background-color: #ffe6e6 !important;
    color: #b71c1c !important;
}

/* Education */
div[data-baseweb="popover"] li:nth-child(7) {
    background-color: #e8eaf6 !important;
    color: #283593 !important;
}

/* Travel */
div[data-baseweb="popover"] li:nth-child(8) {
    background-color: #e0f7fa !important;
    color: #004d40 !important;
}

/* Other */
div[data-baseweb="popover"] li:nth-child(9) {
    background-color: #f5f5f5 !important;
    color: #424242 !important;
}

/* ===============================
   ADDITIONAL STREAMLIT WRAPPER FIXES
   =============================== */

/* Additional fix for Streamlit's selectbox wrapper */
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #e1c4ff !important;
    border-radius: 12px !important;
    min-height: 56px !important; /* Match other inputs */
}

.stSelectbox > div > div > div {
    padding: 16px !important; /* Match other inputs */
    color: #2e2e2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    line-height: 1.2 !important;
    display: flex !important;
    align-items: center !important;
}

/* ===============================
   LABEL STYLING
   =============================== */

/* Style input labels */
.stNumberInput label, .stTextInput label, .stDateInput label, .stSelectbox label, .stMultiSelect label {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    color: #2e2e2e !important;
    margin-bottom: 8px !important;
}

/* Custom labels styling */
.custom-label {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    color: #2e2e2e !important;
    margin-bottom: 8px !important;
    display: block !important;
}

/* ===============================
   PLACEHOLDER TEXT STYLING
   =============================== */

/* Style placeholder text */
.stTextInput > div > div > input::placeholder {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 400 !important;
    font-size: 14px !important;
    color: #888 !important;
}

/* Ensure text visibility in all elements */
.stNumberInput > div > div > input::placeholder,
.stTextInput > div > div > input::placeholder,
.stDateInput > div > div > input::placeholder,
div[data-baseweb="select"] > div span,
.stMultiSelect > div > div span {
    color: #2e2e2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

    
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<span style='color: #2e2e2e; font-weight: 500;'>Amount (₹)</span>", unsafe_allow_html=True)
            amount = st.number_input(
                "Amount (₹)", 
                min_value=0.01, 
                step=0.01,
                label_visibility="collapsed"
            )
            
            st.markdown("<span style='color: #2e2e2e; font-weight: 500;'>What did you buy?</span>", unsafe_allow_html=True)
            description = st.text_input(
                "What did you buy?", 
                placeholder="Pizza that costs more than our monthly pocket money...",
                label_visibility="collapsed"
            )
            
            # Category mapping with emojis and CSS classes
            category_mapping = {
                "Food & Dining": {"emoji": "🍕", "class": "food-dining"},
                "Transportation": {"emoji": "🚗", "class": "transportation"},
                "Shopping": {"emoji": "🛍️", "class": "shopping"},
                "Entertainment": {"emoji": "🎬", "class": "entertainment"},
                "Bills & Utilities": {"emoji": "💡", "class": "bills-utilities"},
                "Healthcare": {"emoji": "🏥", "class": "healthcare"},
                "Education": {"emoji": "📚", "class": "education"},
                "Travel": {"emoji": "✈️", "class": "travel"},
                "Other": {"emoji": "❓", "class": "other"}
            }
            
            # Create display options with emojis
            category_options = [f"{info['emoji']} {cat}" for cat, info in category_mapping.items()]
            
            # Show the dropdown with custom styling
            st.markdown("<span style='color: #2e2e2e; font-weight: 500;'>Category</span>", unsafe_allow_html=True)
            category_full = st.selectbox(
                "Category", 
                category_options,
                label_visibility="collapsed"
            )
            
            # Extract the category name without emoji
            category = category_full.split(' ', 1)[1] if ' ' in category_full else category_full
        
        with col2:
            st.markdown("<span style='color: #2e2e2e; font-weight: 500;'>Expense Type</span>", unsafe_allow_html=True)
            expense_type = st.selectbox(
                "Expense Type", 
                ["personal", "shared", "work"],
                label_visibility="collapsed"
            )
            
            st.markdown("<span style='color: #2e2e2e; font-weight: 500;'>Who spent it?</span>", unsafe_allow_html=True)
            person = st.selectbox(
                "Who spent it?", 
                st.session_state.friends,
                label_visibility="collapsed"
            )
            
            st.markdown("<span style='color: #2e2e2e; font-weight: 500;'>When TF bitch ass?</span>", unsafe_allow_html=True)
            date = st.date_input(
                "When?", 
                datetime.now(),
                label_visibility="collapsed"
            )
            
            shared_with = []
            if expense_type == "shared":
                st.markdown("<span style='color: #2e2e2e; font-weight: 500;'>👥 Shared with whom?</span>", unsafe_allow_html=True)
                shared_with = st.multiselect(
                    "Shared with whom?", 
                    [f for f in st.session_state.friends if f != person],
                    label_visibility="collapsed"
                )
        
        # Add the submit button
        submitted = st.form_submit_button("💸 Record This Financial Decision", use_container_width=True)
        
        if submitted:
            if amount > 0 and description:
                expense = Expense(
                    id=str(uuid.uuid4()),
                    amount=amount,
                    description=description,
                    category=category,
                    expense_type=expense_type,
                    person=person,
                    date=datetime.combine(date, datetime.min.time()),
                    shared_with=shared_with
                )
                tracker.add_expense(expense)
                
                if amount > 100:
                    st.error(f"🚨 Whoa! ₹{amount:.2f}? That's a lot of money! 💸")
                elif amount > 50:
                    st.warning(f"⚠️ ₹{amount:.2f} - Not terrible, but still... 💰")
                else:
                    st.success(f"✅ ₹{amount:.2f} - Reasonable financial decision! 🎉")
                
                st.balloons()
            else:
                st.error("Please fill in all required fields!")

elif page == "👥 People":
    st.title("👥 People Management")
    st.markdown("*Update our names*")
    
    st.info("You can update your names here. These will be used throughout the website.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👧🏻 Your Name")
        your_name = st.text_input("Your Name", value=st.session_state.friends[0], key="your_name")
        
    with col2:
        st.subheader("👦🏻 Boyfriend's Name")
        bf_name = st.text_input("Boyfriend's Name", value=st.session_state.friends[1], key="bf_name")
    
    if st.button("💾 Save Names", use_container_width=True):
        if your_name and bf_name:
            st.session_state.friends = [your_name, bf_name]
            tracker.save_data()
            st.success("✅ Names updated successfully!")
            st.rerun()
        else:
            st.error("Please enter both names!")

elif page == "📊 Reports":
    st.title("Financial Damage Reports")
    st.markdown("*Detailed analysis of your financial decisions*")
    
    df = tracker.get_expenses_df()
    
    if df.empty:
        st.info("No data to report on yet. Add some expenses first!")
    else:
        # Weekly/Monthly toggle
        report_type = st.radio("📅 Report Type", ["Weekly", "Monthly"], horizontal=True)
        
        if report_type == "Weekly":
            # Weekly report
            st.subheader("📅 Weekly Financial Carnage")
            weeks_back = st.slider("How many weeks back?", 1, 12, 4)
            
            weekly_data = []
            for i in range(weeks_back):
                week_start = datetime.now() - timedelta(weeks=i+1)
                week_end = datetime.now() - timedelta(weeks=i)
                week_expenses = df[(df['date'] >= week_start) & (df['date'] < week_end)]
                
                weekly_data.append({
                    'Week': f"Week {i+1}",
                    'Total': week_expenses['amount'].sum(),
                    'Count': len(week_expenses),
                    'Average': week_expenses['amount'].mean() if len(week_expenses) > 0 else 0
                })
            
            weekly_df = pd.DataFrame(weekly_data)
            
            col1, col2 = st.columns(2)
            with col1:
                fig_weekly = px.bar(weekly_df, x='Week', y='Total', 
                                  title="Weekly Spending Totals",
                                  color='Total',
                                  color_continuous_scale='Reds')
                st.plotly_chart(fig_weekly, use_container_width=True)
            
            with col2:
                fig_count = px.bar(weekly_df, x='Week', y='Count',
                                 title="Number of Transactions per Week",
                                 color='Count',
                                 color_continuous_scale='Blues')
                st.plotly_chart(fig_count, use_container_width=True)
        
        else:
            # Monthly report
            st.subheader("📅 Monthly Financial Destruction")
            months_back = st.slider("How many months back?", 1, 12, 6)
            
            monthly_data = []
            for i in range(months_back):
                month_start = datetime.now().replace(day=1) - timedelta(days=32*i)
                month_start = month_start.replace(day=1)
                if i == 0:
                    month_end = datetime.now()
                else:
                    month_end = datetime.now().replace(day=1) - timedelta(days=32*(i-1))
                    month_end = month_end.replace(day=1)
                
                month_expenses = df[(df['date'] >= month_start) & (df['date'] < month_end)]
                
                monthly_data.append({
                    'Month': month_start.strftime('%B %Y'),
                    'Total': month_expenses['amount'].sum(),
                    'Count': len(month_expenses),
                    'Average': month_expenses['amount'].mean() if len(month_expenses) > 0 else 0
                })
            
            monthly_df = pd.DataFrame(monthly_data)
            
            col1, col2 = st.columns(2)
            with col1:
                fig_monthly = px.bar(monthly_df, x='Month', y='Total',
                                   title="Monthly Spending Totals",
                                   color='Total',
                                   color_continuous_scale='Reds')
                fig_monthly.update_xaxes(tickangle=45)
                st.plotly_chart(fig_monthly, use_container_width=True)
            
            with col2:
                fig_avg = px.line(monthly_df, x='Month', y='Average',
                                title="Average Expense per Transaction",
                                markers=True)
                fig_avg.update_xaxes(tickangle=45)
                st.plotly_chart(fig_avg, use_container_width=True)
        
        # Category analysis
        st.subheader("🏷️ Category Breakdown")
        category_analysis = df.groupby('category').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        category_analysis.columns = ['Total Spent', 'Number of Transactions', 'Average Amount']
        category_analysis = category_analysis.sort_values('Total Spent', ascending=False)
        st.dataframe(category_analysis, use_container_width=True)

elif page == "🎯 Split Expenses":
    st.title("🎯 Who Owes Whom?")
    st.markdown("*Track our shared expenses*")
    
    df = tracker.get_expenses_df()
    
    if df.empty:
        st.info("NO shared expenses to track yet!")
    else:
        shared_expenses = df[df['expense_type'] == 'shared']
        
        if shared_expenses.empty:
            st.info("💰 No shared expenses found. You're all good!")
        else:
            st.subheader("💸 Shared Expenses Summary")
            
            # Calculate debts
            debts = {}
            for _, expense in shared_expenses.iterrows():
                payer = expense['person']
                amount = expense['amount']
                shared_with = expense['shared_with']
                
                if shared_with:
                    split_amount = amount / (len(shared_with) + 1)  # +1 for the payer
                    
                    for person in shared_with:
                        if person not in debts:
                            debts[person] = {}
                        if payer not in debts[person]:
                            debts[person][payer] = 0
                        debts[person][payer] += split_amount
            
            # Display debts
            if debts:
                for debtor, creditors in debts.items():
                    st.subheader(f"💳 {debtor} owes:")
                    total_owed = 0
                    for creditor, amount in creditors.items():
                        st.write(f"• **₹{amount:.2f}** to {creditor}")
                        total_owed += amount
                    st.write(f"**Total owed by {debtor}: ₹{total_owed:.2f}**")
                    st.markdown("---")
            
            # Recent shared expenses
            st.subheader("🤝 Recent Shared Expenses")
            recent_shared = shared_expenses.nlargest(10, 'date')[['date', 'person', 'description', 'amount', 'shared_with']]
            recent_shared['date'] = recent_shared['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(recent_shared, use_container_width=True)

# Footer - Mobile friendly with couple context
st.markdown("---")
st.container().markdown("""
<div style='background-color: #f0e6ff; padding: 15px; border-radius: 10px; margin-top: 20px;'>
    <h4 style='text-align: center; color: #333;'>💡 Tips for US</h4>
    <ul style='margin-left: 15px;'>
        <li>Track expenses together regularly</li>
        <li>Use split expenses for shared purchases</li>
        <li>Review your spending weekly as a couple</li>
        <li>Set financial goals together</li>
        <li>Remember: It's about teamwork! and I Love you My Princess 💑</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Fun motivational message
if len(st.session_state.expenses) > 0:
    total_all_time = sum(exp['amount'] for exp in st.session_state.expenses)
    if total_all_time > 1000:
        st.error(f"🚨 You've tracked ₹{total_all_time:.2f} in expenses! Time to budget? 💸")
    elif total_all_time > 500:
        st.warning(f"⚠️ ₹{total_all_time:.2f} tracked so far. You're aware, which is good! 💰")
    else:
        st.success(f"✅ ₹{total_all_time:.2f} tracked. Nice job staying mindful! 🎉")