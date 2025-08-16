import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to database
conn = sqlite3.connect('food_wastage_system (1).db')  
cursor = conn.cursor()

# CRUD Functions
def create_record(table, data):
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    try:
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        st.success(f"New record inserted into {table}!")
        cursor.execute(f"SELECT * FROM {table} WHERE {list(data.keys())[0]} = ?", (data[list(data.keys())[0]],))
        record = cursor.fetchone()
        if record:
            st.text(f"New Record: {tuple(record)}")
        return True
    except sqlite3.Error as e:
        st.error(f"Error creating record: {e}")
        return False

def read_records(table, condition=None):
    query = f"SELECT * FROM {table}"
    if condition:
        query += f" WHERE {condition}"
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except sqlite3.Error as e:
        st.error(f"Error reading {table}: {e}")
        return pd.DataFrame()

def update_record(table, updates, condition):
    set_clause = ', '.join([f"{col} = ?" for col in updates.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
    try:
        cursor.execute(query, tuple(updates.values()))
        conn.commit()
        st.success(f"Record(s) updated in {table}!")
        return True
    except sqlite3.Error as e:
        st.error(f"Error updating {table}: {e}")
        return False

def delete_record(table, condition):
    query = f"DELETE FROM {table} WHERE {condition}"
    try:
        cursor.execute(query)
        conn.commit()
        st.success(f"Record(s) deleted from {table}!")
        return True
    except sqlite3.Error as e:
        st.error(f"Error deleting from {table}: {e}")
        return False

# UI with navigation
st.set_page_config(layout="wide", page_title="Food Wastage Management")
st.sidebar.title("Navigation")
pages = ["Project Introduction", "View Tables", "CRUD Operations", "SQL Queries", "New Query", "Visualization", "User Introduction", "Statistics Dashboard"]
selection = st.sidebar.radio("Go to", pages)

if selection == "Project Introduction":
    st.title("Project Introduction")
    st.markdown("""
        ### Food Wastage Management System
        The Food Wastage Management System is a comprehensive web-based application designed to address the critical issue of food wastage. Built using Streamlit and powered by a SQLite database, this app aims to minimize food waste, promote sustainability, and ensure efficient distribution of surplus food.

        #### **Objectives**
        - **Reduce Food Waste**: Enable providers to list surplus food and receivers to claim it before it expires.
        - **Enhance Efficiency**: Streamline the process of food donation and claiming with real-time data management.
        - **Promote Transparency**: Provide detailed insights and visualizations to track food movement and wastage patterns.
        - **Support Decision Making**: Offer statistical dashboards and custom query tools for stakeholders to analyze data.

        #### **Key Features**
        - **CRUD Operations**: Create, read, update, and delete records for providers, receivers, food listings, and claims.
        - **Data Visualization**: Interactive charts to visualize provider distribution, claim statuses, and food quantities.
        - **SQL Queries**: Predefined and custom SQL queries with auto-generated visualizations.
        - **Statistics Dashboard**: Real-time insights into record counts and recent activities.

        #### **Database Structure**
        The system uses a SQLite database named `food_wastage_system (1).db` with the following tables:
        - **providers**: Stores details like Provider_ID, Name, Type, Address, City, and Contact.
        - **receivers**: Contains Receiver_ID, Name, Type, City, and Contact.
        - **food_listings**: Tracks Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, and other attributes.
        - **claims**: Manages Claim_ID, Food_ID, Receiver_ID, Status, and Timestamp.

    """)

elif selection == "View Tables":
    st.title("View All Tables")
    tables = ["providers", "receivers", "food_listings", "claims"]
    for table in tables:
        st.subheader(table.capitalize())
        st.write(read_records(table))

elif selection == "CRUD Operations":
    st.title("CRUD Operations")
    tables = ["providers", "receivers", "food_listings", "claims"]
    for table in tables:
        st.subheader(table.capitalize())
        if table == "providers":
            with st.form(f"{table}_create"):
                data = {
                    "Provider_ID": st.number_input("Provider ID", min_value=1),
                    "Name": st.text_input("Name"),
                    "Type": st.text_input("Type"),
                    "Address": st.text_input("Address"),
                    "City": st.text_input("City"),
                    "Contact": st.text_input("Contact")
                }
                if st.form_submit_button("Create"):
                    create_record(table, data)
            with st.form(f"{table}_update"):
                update_id = st.number_input("Provider ID to Update", min_value=1)
                new_city = st.text_input("New City")
                if st.form_submit_button("Update City"):
                    update_record(table, {"City": new_city}, f"Provider_ID={update_id}")
            with st.form(f"{table}_delete"):
                delete_id = st.number_input("Provider ID to Delete", min_value=1)
                if st.form_submit_button("Delete"):
                    delete_record(table, f"Provider_ID={delete_id}")
        elif table == "receivers":
            with st.form(f"{table}_create"):
                data = {
                    "Receiver_ID": st.number_input("Receiver ID", min_value=1),
                    "Name": st.text_input("Name"),
                    "Type": st.text_input("Type"),
                    "City": st.text_input("City"),
                    "Contact": st.text_input("Contact")
                }
                if st.form_submit_button("Create"):
                    create_record(table, data)
            with st.form(f"{table}_update"):
                update_id = st.number_input("Receiver ID to Update", min_value=1)
                new_city = st.text_input("New City")
                if st.form_submit_button("Update City"):
                    update_record(table, {"City": new_city}, f"Receiver_ID={update_id}")
            with st.form(f"{table}_delete"):
                delete_id = st.number_input("Receiver ID to Delete", min_value=1)
                if st.form_submit_button("Delete"):
                    delete_record(table, f"Receiver_ID={delete_id}")
        elif table == "food_listings":
            with st.form(f"{table}_create"):
                data = {
                    "Food_ID": st.number_input("Food ID", min_value=1),
                    "Food_Name": st.text_input("Food Name"),
                    "Quantity": st.number_input("Quantity", min_value=0),
                    "Expiry_Date": st.text_input("Expiry Date (YYYY-MM-DD)"),
                    "Provider_ID": st.number_input("Provider ID", min_value=1),
                    "Provider_Type": st.text_input("Provider Type"),
                    "Location": st.text_input("Location"),
                    "Food_Type": st.text_input("Food Type"),
                    "Meal_Type": st.text_input("Meal Type")
                }
                if st.form_submit_button("Create"):
                    create_record(table, data)
            with st.form(f"{table}_update"):
                update_id = st.number_input("Food ID to Update", min_value=1)
                new_quantity = st.number_input("New Quantity", min_value=0)
                if st.form_submit_button("Update Quantity"):
                    update_record(table, {"Quantity": new_quantity}, f"Food_ID={update_id}")
            with st.form(f"{table}_delete"):
                delete_id = st.number_input("Food ID to Delete", min_value=1)
                if st.form_submit_button("Delete"):
                    delete_record(table, f"Food_ID={delete_id}")
        elif table == "claims":
            with st.form(f"{table}_create"):
                data = {
                    "Claim_ID": st.number_input("Claim ID", min_value=1),
                    "Food_ID": st.number_input("Food ID", min_value=1),
                    "Receiver_ID": st.number_input("Receiver ID", min_value=1),
                    "Status": st.text_input("Status"),
                    "Timestamp": st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)")
                }
                if st.form_submit_button("Create"):
                    create_record(table, data)
            with st.form(f"{table}_update"):
                update_id = st.number_input("Claim ID to Update", min_value=1)
                new_status = st.text_input("New Status")
                if st.form_submit_button("Update Status"):
                    update_record(table, {"Status": new_status}, f"Claim_ID={update_id}")
            with st.form(f"{table}_delete"):
                delete_id = st.number_input("Claim ID to Delete", min_value=1)
                if st.form_submit_button("Delete"):
                    delete_record(table, f"Claim_ID={delete_id}")
        st.write(read_records(table))

elif selection == "SQL Queries":
    st.title("SQL Queries")
    # Predefined queries from notebook
    queries = {
        "Q1: Providers per city": '''
            SELECT City, COUNT(*) as Provider_Count
            FROM providers
            GROUP BY City
            ORDER BY Provider_Count DESC
        ''',
        "Q2: Receivers per city": '''
            SELECT City, COUNT(*) as Receiver_Count
            FROM receivers
            GROUP BY City
            ORDER BY Receiver_Count DESC
        ''',
        "Q3: Top 3 provider types by listings": '''
            SELECT Provider_Type, COUNT(*) as Listing_Count
            FROM food_listings
            GROUP BY Provider_Type
            ORDER BY Listing_Count DESC
            LIMIT 3
        ''',
        "Q4_1: Providers in New Jessica": '''
            SELECT Name, Contact, Address
            FROM providers
            WHERE City = 'New Jessica'
        ''',
        "Q4_2: Providers in Mendezmouth": '''
            SELECT Name, Contact, Address
            FROM providers
            WHERE City = 'Mendezmouth'
        ''',
        "Q5: Top 8 receivers by claims": '''
            SELECT r.Name, COUNT(c.Claim_ID) as Claim_Count
            FROM receivers r
            JOIN claims c ON r.Receiver_ID = c.Receiver_ID
            GROUP BY r.Receiver_ID, r.Name
            ORDER BY Claim_Count DESC
            LIMIT 8
        ''',
        "Q6: Total food quantity": '''
            SELECT SUM(Quantity) as Total_Quantity
            FROM food_listings
        ''',
        "Q7: City with most listings": '''
            SELECT Location, COUNT(*) as Listing_Count
            FROM food_listings
            GROUP BY Location
            ORDER BY Listing_Count DESC
            LIMIT 1
        ''',
        "Q8: Most common food types": '''
            SELECT Food_Type, COUNT(*) as Listing_Count
            FROM food_listings
            GROUP BY Food_Type
            ORDER BY Listing_Count DESC
        ''',
        "Q9: Claims per food item": '''
            SELECT f.Food_Name, COUNT(c.Claim_ID) as Claim_Count
            FROM food_listings f
            LEFT JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY f.Food_ID, f.Food_Name
            ORDER BY Claim_Count DESC
        ''',
        "Q10: Top provider by completed claims": '''
            SELECT p.Name, COUNT(c.Claim_ID) as Completed_Claims
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            JOIN claims c ON f.Food_ID = c.Food_ID
            WHERE c.Status = 'Completed'
            GROUP BY p.Provider_ID, p.Name
            ORDER BY Completed_Claims DESC
            LIMIT 1
        ''',
        "Q11: Claim status percentages": '''
            SELECT Status, COUNT(*) as Claim_Count, (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims)) as Percentage
            FROM claims
            GROUP BY Status
            ORDER BY Claim_Count DESC
        ''',
        "Q12: Avg quantity claimed per receiver": '''
            SELECT r.Name, AVG(f.Quantity) as Avg_Quantity_Claimed
            FROM receivers r
            JOIN claims c ON r.Receiver_ID = c.Receiver_ID
            JOIN food_listings f ON c.Food_ID = f.Food_ID
            GROUP BY r.Receiver_ID, r.Name
            ORDER BY Avg_Quantity_Claimed DESC
        ''',
        "Q13: Most claimed meal type": '''
            SELECT f.Meal_Type, COUNT(c.Claim_ID) as Claim_Count
            FROM food_listings f
            JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY f.Meal_Type
            ORDER BY Claim_Count DESC
            LIMIT 1
        ''',
        "Q14: Total quantity donated by provider": '''
            SELECT p.Name, SUM(f.Quantity) as Total_Donated
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            GROUP BY p.Provider_ID, p.Name
            ORDER BY Total_Donated DESC
        ''',
        "Q15: Providers with no claims": '''
            SELECT p.Name
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            LEFT JOIN claims c ON f.Food_ID = c.Food_ID
            WHERE c.Claim_ID IS NULL
            GROUP BY p.Provider_ID, p.Name
        ''',
        "Q16: Receivers with no claims": '''
            SELECT Name
            FROM receivers
            WHERE Receiver_ID NOT IN (SELECT Receiver_ID FROM claims)
        ''',
        "Q17: Claims by meal type and status": '''
            SELECT f.Meal_Type, c.Status, COUNT(c.Claim_ID) as Claim_Count
            FROM food_listings f
            JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY f.Meal_Type, c.Status
            ORDER BY Claim_Count DESC
        ''',
        "Q18: Unclaimed food listings": '''
            SELECT f.Food_Name, f.Quantity, f.Expiry_Date
            FROM food_listings f
            LEFT JOIN claims c ON f.Food_ID = c.Food_ID
            WHERE c.Claim_ID IS NULL
        ''',
        "Q19: Receivers per city by meal type": '''
            SELECT r.City, 
                   COUNT(DISTINCT CASE WHEN f.Meal_Type = 'Breakfast' THEN r.Receiver_ID END) as Breakfast_Receivers,
                   COUNT(DISTINCT CASE WHEN f.Meal_Type = 'Lunch' THEN r.Receiver_ID END) as Lunch_Receivers,
                   COUNT(DISTINCT CASE WHEN f.Meal_Type = 'Dinner' THEN r.Receiver_ID END) as Dinner_Receivers,
                   COUNT(DISTINCT CASE WHEN f.Meal_Type = 'Snacks' THEN r.Receiver_ID END) as Snacks_Receivers
            FROM receivers r
            JOIN claims c ON r.Receiver_ID = c.Receiver_ID
            JOIN food_listings f ON c.Food_ID = f.Food_ID
            GROUP BY r.City
            ORDER BY Breakfast_Receivers DESC, Lunch_Receivers DESC, Dinner_Receivers DESC, Snacks_Receivers DESC
        ''',
        "Q20: Receiver type with most food": '''
            SELECT r.Type, f.Food_Type, SUM(f.Quantity) as Total_Quantity
            FROM receivers r
            JOIN claims c ON r.Receiver_ID = c.Receiver_ID
            JOIN food_listings f ON c.Food_ID = f.Food_ID
            GROUP BY r.Type, f.Food_Type
            ORDER BY Total_Quantity DESC
            LIMIT 1
        ''',
        "Q21: Receivers by food and meal type": '''
            SELECT r.Name, f.Food_Type, f.Meal_Type, COUNT(c.Claim_ID) as Claim_Count
            FROM receivers r
            JOIN claims c ON r.Receiver_ID = c.Receiver_ID
            JOIN food_listings f ON c.Food_ID = f.Food_ID
            GROUP BY r.Receiver_ID, r.Name, f.Food_Type, f.Meal_Type
            ORDER BY Claim_Count DESC
        ''',
        "Q22: Claims by city": '''
            SELECT f.Location, COUNT(c.Claim_ID) as Claim_Count
            FROM food_listings f
            JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY f.Location
            ORDER BY Claim_Count DESC
        ''',
        "Q23: Providers with highest avg quantity": '''
            SELECT p.Name, AVG(f.Quantity) as Avg_Quantity
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            GROUP BY p.Provider_ID, p.Name
            ORDER BY Avg_Quantity DESC
            LIMIT 5
        ''',
        "Q24: Percentage of quantity claimed per food type": '''
            SELECT f.Food_Type,
                   SUM(f.Quantity) as Total_Quantity,
                   SUM(CASE WHEN c.Claim_ID IS NOT NULL THEN f.Quantity ELSE 0 END) * 100.0 / SUM(f.Quantity) as Claimed_Percentage
            FROM food_listings f
            LEFT JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY f.Food_Type
        '''
    }
    with st.form("sql_query_form"):
        selected_query = st.selectbox("Select a Predefined Query", list(queries.keys()))
        query = queries[selected_query]
        if st.form_submit_button("Execute"):
            try:
                df = pd.read_sql_query(query, conn)
                st.write("Query Result:", df)
                if df.empty:
                    st.warning("No data returned from query.")
            except sqlite3.Error as e:
                st.error(f"Error executing query: {e}")

elif selection == "New Query":
    st.title("New Query")
    with st.form("new_query_form"):
        custom_query = st.text_area("Enter New Custom Query", "SELECT * FROM providers")
        if st.form_submit_button("Execute"):
            try:
                df = pd.read_sql_query(custom_query, conn)
                st.write("Query Result:", df)
                if df.empty:
                    st.warning("No data returned from query.")
            except sqlite3.Error as e:
                st.error(f"Error executing query: {e}")

elif selection == "Visualization":
    st.title("Data Visualization")
    # Chart 1: Providers per City (Top 10)
    st.subheader("Providers per City (Top 10)")
    q1 = pd.read_sql('''
        SELECT City, COUNT(*) as Provider_Count
        FROM providers
        GROUP BY City
        ORDER BY Provider_Count DESC
    ''', conn)
    q1_top = q1.nlargest(10, 'Provider_Count')
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=q1_top, x='City', y='Provider_Count', palette='Blues_d', ax=ax1)
    ax1.set_title('Top 10 Cities by Number of Providers')
    ax1.set_xlabel('City')
    ax1.set_ylabel('Provider Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig1)

    # Chart 2: Claim Status Distribution
    st.subheader("Claim Status Distribution")
    q11 = pd.read_sql('''
        SELECT Status, COUNT(*) as Claim_Count, (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims)) as Percentage
        FROM claims
        GROUP BY Status
        ORDER BY Claim_Count DESC
    ''', conn)
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.pie(q11['Percentage'], labels=q11['Status'], autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'], textprops={'fontsize': 12})
    ax2.set_title('Claim Status Distribution')
    st.pyplot(fig2)

    # Chart 3: Total Quantity Donated by Provider (Top 5)
    st.subheader("Total Quantity Donated by Provider (Top 5)")
    q14 = pd.read_sql('''
        SELECT p.Name, SUM(f.Quantity) as Total_Donated
        FROM providers p
        JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        GROUP BY p.Provider_ID, p.Name
        ORDER BY Total_Donated DESC
        LIMIT 5
    ''', conn)
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=q14, x='Name', y='Total_Donated', palette='Greens_d', ax=ax3)
    ax3.set_title('Top 5 Providers by Total Quantity Donated')
    ax3.set_xlabel('Provider Name')
    ax3.set_ylabel('Total Quantity')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig3)

    # Chart 4: Avg Quantity Claimed per Receiver (Top 5)
    st.subheader("Avg Quantity Claimed per Receiver (Top 5)")
    q12 = pd.read_sql('''
        SELECT r.Name, AVG(f.Quantity) as Avg_Quantity_Claimed
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY r.Receiver_ID, r.Name
        ORDER BY Avg_Quantity_Claimed DESC
        LIMIT 5
    ''', conn)
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=q12, x='Name', y='Avg_Quantity_Claimed', palette='Reds_d', ax=ax4)
    ax4.set_title('Top 5 Receivers by Avg Quantity Claimed')
    ax4.set_xlabel('Receiver Name')
    ax4.set_ylabel('Avg Quantity')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig4)

    # Chart 5: Claims by City (Top 10)
    st.subheader("Claims by City (Top 10)")
    q22 = pd.read_sql('''
        SELECT f.Location, COUNT(c.Claim_ID) as Claim_Count
        FROM food_listings f
        JOIN claims c ON f.Food_ID = c.Food_ID
        GROUP BY f.Location
        ORDER BY Claim_Count DESC
        LIMIT 10
    ''', conn)
    fig5, ax5 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=q22, x='Location', y='Claim_Count', palette='Purples_d', ax=ax5)
    ax5.set_title('Top 10 Cities by Number of Claims')
    ax5.set_xlabel('City')
    ax5.set_ylabel('Claim Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig5)

    # Chart 6: Most Common Food Types (Top 5)
    st.subheader("Most Common Food Types (Top 5)")
    q8 = pd.read_sql('''
        SELECT Food_Type, COUNT(*) as Listing_Count
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Listing_Count DESC
        LIMIT 5
    ''', conn)
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    ax6.pie(q8['Listing_Count'], labels=q8['Food_Type'], autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#cc99ff'])
    ax6.set_title('Top 5 Most Common Food Types')
    st.pyplot(fig6)

    # Chart 7: Providers with Highest Avg Quantity (Top 5)
    st.subheader("Providers with Highest Avg Quantity (Top 5)")
    q23 = pd.read_sql('''
        SELECT p.Name, AVG(f.Quantity) as Avg_Quantity
        FROM providers p
        JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        GROUP BY p.Provider_ID, p.Name
        ORDER BY Avg_Quantity DESC
        LIMIT 5
    ''', conn)
    fig7, ax7 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=q23, x='Name', y='Avg_Quantity', palette='Oranges_d', ax=ax7)
    ax7.set_title('Top 5 Providers by Avg Quantity')
    ax7.set_xlabel('Provider Name')
    ax7.set_ylabel('Avg Quantity')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig7)

    # Chart 8: Claims by Meal Type (Top 5)
    st.subheader("Claims by Meal Type (Top 5)")
    q13 = pd.read_sql('''
        SELECT f.Meal_Type, COUNT(c.Claim_ID) as Claim_Count
        FROM food_listings f
        JOIN claims c ON f.Food_ID = c.Food_ID
        GROUP BY f.Meal_Type
        ORDER BY Claim_Count DESC
        LIMIT 5
    ''', conn)
    fig8, ax8 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=q13, x='Meal_Type', y='Claim_Count', palette='YlOrBr', ax=ax8)
    ax8.set_title('Top 5 Meal Types by Claim Count')
    ax8.set_xlabel('Meal Type')
    ax8.set_ylabel('Claim Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig8)

    # Chart 9: Unclaimed Food Listings by Quantity (Top 5)
    st.subheader("Unclaimed Food Listings by Quantity (Top 5)")
    q18 = pd.read_sql('''
        SELECT f.Food_Name, f.Quantity
        FROM food_listings f
        LEFT JOIN claims c ON f.Food_ID = c.Food_ID
        WHERE c.Claim_ID IS NULL
        ORDER BY f.Quantity DESC
        LIMIT 5
    ''', conn)
    fig9, ax9 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=q18, x='Food_Name', y='Quantity', palette='Greys_d', ax=ax9)
    ax9.set_title('Top 5 Unclaimed Food Listings by Quantity')
    ax9.set_xlabel('Food Name')
    ax9.set_ylabel('Quantity')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig9)

    # Chart 10: Receivers per City by Breakfast Claims (Top 5)
    st.subheader("Receivers per City by Breakfast Claims (Top 5)")
    q19 = pd.read_sql('''
        SELECT r.City, COUNT(DISTINCT CASE WHEN f.Meal_Type = 'Breakfast' THEN r.Receiver_ID END) as Breakfast_Receivers
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY r.City
        ORDER BY Breakfast_Receivers DESC
        LIMIT 5
    ''', conn)
    fig10, ax10 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=q19, x='City', y='Breakfast_Receivers', palette='BuPu', ax=ax10)
    ax10.set_title('Top 5 Cities by Breakfast Receivers')
    ax10.set_xlabel('City')
    ax10.set_ylabel('Breakfast Receivers')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig10)

elif selection == "User Introduction":
    st.title("User Introduction")
    st.markdown("""
        ### How to Use This App: A Step-by-Step Guide

        Welcome to the Food Wastage Management System! This app is designed to be user-friendly for both providers and receivers. Below is a detailed guide to help you navigate and utilize all features effectively:

        #### **Getting Started**
        - **Navigation**: Use the sidebar on the left to switch between sections like "Project Introduction," "View Tables," "CRUD Operations," etc.

        #### **Key Sections and Usage**
        1. **Project Introduction**
           - Explore the purpose, objectives, and database structure of the app to understand its mission.
        2. **View Tables**
           - View all records in the `providers`, `receivers`, `food_listings`, and `claims` tables.
           - No action is required; simply browse the data displayed.
        3. **CRUD Operations**
           - **Create**: Fill out the form for the respective table and click "Create" to add a new record.
           - **Update**: Enter the ID of the record to update, input the new value, and click "Update City" or similar.
           - **Delete**: Input the ID of the record to delete and click "Delete" to remove it.
           - Tip: Ensure unique IDs and valid foreign keys.
        4. **SQL Queries**
           - Select a predefined query from the dropdown and click "Execute" to see results and an auto-generated visualization.
        5. **New Query**
           - Write a custom SQL query in the text area  and click "Execute" to view results with visualization.
        6. **Visualization**
           - View pre-built charts to analyze data trends.
        7. **Statistics Dashboard**
           - Check total records per table and the latest 5 claims for quick insights.

    """)

elif selection == "Statistics Dashboard":
    st.title("Statistics Dashboard")
    st.subheader("Quick Insights")
    tables = ["providers", "receivers", "food_listings", "claims"]
    for table in tables:
        df = read_records(table)
        st.write(f"Total {table.capitalize()}: {len(df)}")
    st.subheader("Recent Claims")
    recent_claims = pd.read_sql("SELECT * FROM claims ORDER BY Timestamp DESC LIMIT 5", conn)
    st.write(recent_claims)

# Close connection
def on_app_stop():
    conn.close()
import atexit
atexit.register(on_app_stop)