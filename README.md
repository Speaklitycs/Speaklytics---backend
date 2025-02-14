# Speaklytics Backend

Welcome to the backend repository of Speaklytics, a powerful analytics platform designed to provide insightful data about your own speeches.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Speaklitycs/Speaklytics---backend.git
   cd Speaklytics---backend
   ```

2. **Set Up a Virtual Environment** (Recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:

   ```bash
   python manage.py migrate
   ```


## Running the Application

To start the Django development server on port 8080:

```bash
python manage.py runserver localhost:8080
```

The application will be accessible at `http://localhost:8080/`.

## Contributing

We welcome contributions! Please fork the repository and submit a pull request with your changes. Ensure your code adheres to our coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
