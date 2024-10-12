# Scan&Order

Project for course Database basics in school year 2023/2024 at Faculty of Mathematics and Physics, University of Ljubljana.

Authors: Gal Zmazek and Vito Levstik

## README
- [English](./README.en.md)
- [Slovensko](./README.md)

## ER Diagram
![ER diagram](https://github.com/gzmazek/skeniraj-in-naroci/blob/main/ER_diagram.png?raw=true)

## Project description

Project "Scan&Order" is a concept of a system for order management in restaurants. Main purpose of the app is to enable simple ordering with the app by scanning the QR code, managing the restaurant menus and collecting business analytics data.

## Instructions for usage

### Setting up

1. **Cloning repository:**

   ```bash
   git clone https://github.com/gzmazek/skeniraj-in-naroci.git
   cd skeniraj-in-naroci
   ```

2. **Setting up virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Dependencies installation:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Running development server:**

   ```bash
   python manage.py runserver
   ```
   Terminal prints the address where the web app is located. Probably it will be http://127.0.0.1:8000/ or something similar.

### App usage

1. **Sign in:**
   You can sing in with the user account. If you don't have an account, you can create it in registration form. The same account can be used for the purpose of ordering food and for managing the restaurants.

2. **Adding restaurant:**
   In the menu select option to add new restaurant. After adding it, you can start managing the menus, tables and orders.

3. **Menu management:**
   By creating new items, you can add them to the menu of the restaurant, or you can remove the existing items from restaurant menu.

4. **Ordering:**
   Users can scan the QR code, that is related to specific table in the restaurant, and order within the mobile app.

5. **Analytics:**
   In the analytics tab, restaurant owners can view different data about the restaurant.

### Tools and Technologies

- **Python & Django**: Backend development and database management.
- **PostgreSQL**: Relation database used.
- **HTML, CSS, Bootstrap**: User interface.
- **Chart.js**: Visualization of data.
