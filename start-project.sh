# Create the 'core' project
django-admin startproject core .

# Create a folder to host the future App with the name 'simple-app'
mkdir -p app/simple_app

# Create the 'simple-app' App
django-admin startapp simple_app app/simple_app
