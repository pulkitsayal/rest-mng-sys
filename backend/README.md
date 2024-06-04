# Setup Steps
Navigate to the backend folder
```sh
cd backend
```

Set up and run virtual environment
```sh
# Install virtualenv if not already installed
pip install virtualenv

# Create the virtual environment
virtualenv <virtual env name> # e.g., rms_env

# Activate the virtual environment (Unix/macOS)
source <virtual env name>/bin/activate

# Activate the virtual environment (Windows)
<virtual env name>\Scripts\activate # e.g., rms_env\Scripts\activate

# Deactivate the virtual environment (Windows)
deactivate

```
Install requirements (inside virtual env)
```sh
pip install -r requirements.txt
```

Run the server
```sh
cd src
uvicorn main:app --reload
```
