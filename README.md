
# Mimicing the concept of Social Media using FastAPI

## Features
- Account Creation
- Account Authentication (OAuth2)
- Post Create, Read, Update and Delete(CRUD)
- Post like and dislike
- Post like and dislike counter

This project is a Python-based web API application. It uses various tools and libraries to provide API functionality, likely for managing resources.

## Project Structure

- `app/` - The main application directory containing the core API logic.
- `alembic.ini` - Configuration file for Alembic, used for database migrations.
- `requirements.txt` - Lists all the dependencies and libraries required to run the project.
- `Procfile` - Specifies the commands that are executed by the app on Heroku.
- `test.py` - Contains test code for the API.

## Requirements

Install the required dependencies from `requirements.txt` before running the application:

```bash
pip install -r requirements.txt
```

## Running the Application

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   For FastAPI:
   ```bash
   uvicorn app.main:app --reload
   ```
   For Flask:
   ```bash
   flask run
   ```

3. **Heroku Deployment**:
   ```bash
   git push heroku master
   ```

## Database Migrations

The project uses Alembic for database migrations:

1. **Generate migration**:
   ```bash
   alembic revision --autogenerate -m "migration message"
   ```

2. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

## Testing

Run tests using the `test.py` file:

```bash
python test.py
```

## Deployment

This project is set up for deployment on Heroku. The `Procfile` defines the command to start the application in a Heroku environment.

1. Install the Heroku CLI.
2. Deploy to Heroku:
   ```bash
   git push heroku master
   ```

## Troubleshooting

If you encounter a `ModuleNotFoundError: No module named '_tkinter'` error:

1. Open `app/models.py`
2. Remove or comment out the line: `from turtle import title`
3. If you need a `title` function, implement a simple one:
   ```python
   def title(s):
       return s.title()
   ```
4. Remove any other `turtle` module dependencies.
5. Commit changes and redeploy.

This error occurs because Heroku's default Python environment doesn't include `tkinter`, which is typically used for GUI applications and is not necessary for web APIs.

## License

This project is licensed under the MIT License.
```

This README provides a comprehensive guide to setting up, running, testing, and deploying the API project, as well as troubleshooting a common deployment issue. It's formatted in markdown for easy reading on platforms like GitHub.
