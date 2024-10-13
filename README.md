# FastAPI RESTful API

## Overview

Provide a brief overview of the project, its purpose, and the problem it aims to solve.

## Table of Contents

- [FastAPI RESTful API](#fastapi-restful-api)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Setup and Run Instructions](#setup-and-run-instructions)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
    - [Accessing the API](#accessing-the-api)
  - [Design and Architectural Decisions](#design-and-architectural-decisions)
  - [Scaling Strategies and Trade-offs](#scaling-strategies-and-trade-offs)
    - [Potential Strategies](#potential-strategies)
    - [Trade-offs](#trade-offs)
  - [Docker Setup](#docker-setup)

## Setup and Run Instructions

### Prerequisites

- Python 3.9 or higher
- SQLite
- Virtual environment (optional but recommended)

### Installation Steps

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up Virtual Environment (optional)**:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:

   ```bash
   alembic upgrade head
   ```

5. **Start the Application**:

   ```bash
   uvicorn src.main:app --reload
   ```

6. **Connect db to a GUI**:

### Accessing the API

The API will be available at `http://127.0.0.1:8000`. Use tools like Postman or cURL to interact with the endpoints.

## Design and Architectural Decisions

- **Framework**: FastAPI was chosen for its speed and ease of use, particularly with asynchronous operations.
- **Database**: SQLAlchemy is used for ORM, allowing for easy database migrations and management.
- **Encryption**: User data is encrypted using Fernet symmetric encryption for added security.
- **Async Operations**: The use of AsyncSession for database interactions improves performance and handles concurrent requests effectively.

## Scaling Strategies and Trade-offs

### Potential Strategies

- **Database Optimization**:
  - Implement database indexing to speed up query performance.
  - Consider using read replicas for scaling read operations.
- **Load Balancing**:
  - Use load balancers to distribute incoming requests across multiple application instances.
- **Caching**:
  - Implement caching mechanisms (e.g., Redis) to store frequently accessed data and reduce database load.

### Trade-offs

- **Complexity vs. Performance**:
  - Introducing load balancing and caching increases complexity but can significantly improve performance.
- **Cost Considerations**:
  - Utilizing read replicas and caching solutions incurs additional costs, which need to be justified by performance gains.
- **Security**:
  - While encryption provides security, it adds overhead in terms of processing time and can affect performance. Consider the balance between security and speed based on user needs.

## Docker Setup

1. **Build the Docker Image**:

   ```bash
   docker build -t your_image_name .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run -p 8000:8000 your_image_name
   ```

3. **Using Docker Compose** (if needed for multiple services):
   Create a `docker-compose.yml` file:

   ```yaml
   version: "3"

   services:
     web:
       build: .
       command: sh -c "uvicorn src.main:app --reload --port=8000 --host=0.0.0.0"
       env_file:
         - .env
       ports:
         - 8000:8000
       volumes:
         - .:/app
   ```
