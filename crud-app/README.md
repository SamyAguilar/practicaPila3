# CRUD Application

This is a simple CRUD (Create, Read, Update, Delete) application built using Python with Flask, PostgreSQL as the database, and styled with CSS. The application is configured to run on a Linux server with Nginx.

## Project Structure

```
crud-app
├── src
│   ├── app.py          # Entry point of the application
│   ├── db.py           # Database connection handling
│   ├── models.py       # Data model definitions
│   ├── routes.py       # CRUD operation routes
│   ├── static
│   │   └── styles.css   # CSS styles for the application
│   └── templates
│       └── index.html   # Main HTML template
├── requirements.txt     # Python dependencies
├── nginx.conf           # Nginx configuration
└── README.md            # Project documentation
```

## Setup Instructions

1. **Install Dependencies**: Make sure you have Python and PostgreSQL installed. Use the following command to install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

2. **Database Configuration**: Ensure that PostgreSQL is running and create a database for the application. Update the `db.py` file with the correct database name if necessary.

3. **Nginx Configuration**: Configure Nginx to serve the application. Update the `nginx.conf` file to point to the correct application path and set it to listen on port 81.

4. **Run the Application**: Start the Flask application by running:

   ```
   python src/app.py
   ```

5. **Access the Application**: Open your web browser and navigate to `http://localhost:81` to access the application.

## Usage

- You can create new records, view existing records, update them, and delete them using the web interface.
- The application is designed to be simple and easy to use, making it a good starting point for learning about web development with Flask and PostgreSQL.

## License

This project is open-source and available for modification and distribution.