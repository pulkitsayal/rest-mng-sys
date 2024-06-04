# Setup Steps
- Pre-requisites
Install Python

- Navigate to the backend folder
```sh
cd ../backend
```

- Set up your virtual environment
```sh
# Install virtualenv if not already installed
pip install virtualenv

# Create the virtual environment
virtualenv < virtual env name > # rms_env

# Activate the virtual environment (Unix/macOS)
source < virtual env name >/bin/activate

# Activate the virtual environment (Windows)
.\< virtual env name >\Scripts\activate # rms_env\Scripts\activate

# Deactivate the virtual environment (Windows)
.\< virtual env name >\Scripts\deactivate

```
- Install requirements (inside virtual env)
```sh
pip install -r requirements.txt
```

- Run the server
```sh
uvicorn main:app --reload
```
