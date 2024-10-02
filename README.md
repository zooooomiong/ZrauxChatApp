
# ZrauxChatApp

**ZrauxChatApp** is a real-time messaging application built with Django, Redis, Celery, and WebSocket. It supports real-time communication, duo chats.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)


## Features

- Real-time messaging via WebSocket
- Duo chats
- Background tasks using Celery
- Emoji support
- Responsive design

## Demo

Check out the live demo of ZrauxChatApp here: [ZrauxChatApp Live Demo](https://zraux.com)

## Installation

To run ZrauxChatApp locally, follow these steps:

### 1. Clone the repository:

```bash
git clone https://github.com/zooooomiong/ZrauxChatApp.git
```

### 2. Navigate to the project directory:

```bash
cd ZrauxChatApp
```

### 3. Install Python dependencies:

It's recommended to use a virtual environment. First, set up the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Install Docker and run Redis:

If you don't have Docker installed, follow [this guide](https://docs.docker.com/get-docker/) to install it. Once Docker is installed, run Redis on port 6379:

```bash
docker run -d -p 6379:6379 redis
```

### 5. Set up environment variables:

Create a `.env` file in the project root and add the necessary environment variables like Redis URL, secret keys, etc.

```bash
touch .env
```

You can structure the `.env` file like this:

```
SECRET_KEY=your_django_secret_key
USERNAME_=you_email_or_email_service_username
PASSWORD=you_email_dev_key_or_service_password
```

### 6. Apply Django migrations:

Run the following command to apply database migrations:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

### 7. Run Celery worker:

Start the Celery worker with the `gevent` pool:

```bash
celery -A chat_proj worker -P gevent
```

This will enable background tasks.

### 8. Run the Django development server:

Start the Django development server:

```bash
python manage.py runserver
```

The app should now be running at:

```
http://localhost:8000
```

