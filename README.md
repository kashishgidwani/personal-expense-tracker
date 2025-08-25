# Expense Tracker App

A beautiful, mobile-friendly expense tracker application built with Streamlit. Track your expenses, visualize spending patterns, and manage shared expenses with your partner.

## Features

- 📊 Interactive dashboard with spending visualizations
- 💰 Add and categorize expenses with a stylish interface
- 👥 Manage people and track shared expenses
- 📈 Generate reports on spending patterns
- 💸 Track who owes whom for shared expenses
- 📱 Mobile-friendly design with a beautiful lavender and pink theme
- ₹ Indian Rupee support

## Live Demo

You can access the live application at: [Expense Tracker App](https://your-github-username.github.io/expense-tracker)

## Local Setup

1. Clone this repository:
   ```
   git clone https://github.com/your-github-username/expense-tracker.git
   cd expense-tracker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run tracker.py
   ```

4. Open your browser and navigate to http://localhost:8501

## Deployment

This application is deployed using Streamlit Cloud. You can deploy your own version by:

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy the app

## Data Storage

The application stores data in a local JSON file (`expenses_data.json`). For production use, you might want to consider using a database.

## Customization

You can customize the application by modifying the `tracker.py` file:

- Change the theme colors in the CSS section
- Modify expense categories
- Add new features or reports

## License

MIT