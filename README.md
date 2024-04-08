
# Co:Helm Prototype

This application exemplifies the Co:Helm product.

### Prerequisites

You'll need the following to install the software:

- Docker
- docker-compose

### Setting Up

To get your development environment up and running;

1. Clone the repository:
    ```bash
    git clone https://github.com/osetinsky/product-engineer-starter.git
    ```

2. Navigate to the project directory:
    ```bash
    cd product-engineer-starter
    ```

3. Use the `Makefile` to build the Docker images for your project:
    ```bash
    make build
    ```

### Starting the Application

To start all services (including the backend and database):

```bash
make up
```

This command uses `docker-compose` to start the services defined in your `docker-compose.yml` file. Your backend service will not start until the database service is running.

### Applying Migrations

To apply database migrations:

```bash
make build-migrations
make migrate
```

This will run Alembic migrations within the backend service's container, updating your database schema.

### Stopping the Application

To stop and remove all running services:

```bash
make down
```

### Viewing Logs

To view logs from the backend service:

```bash
make be-logs

And frontend service:

```bash
make fe-logs

And containerized database:

```bash
make db-logs
```

### Accessing the Application

- The backend API will be available at `http://localhost:8000` (or whichever host/port you set with `NEXT_PUBLIC_SERVER_HOST` or `NEXT_PUBLIC_SERVER_PORT`).
- The frontend application will be available at `http://localhost:3000` (or whichever port you set with `CLIENT_PORT`).