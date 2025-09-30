# PostgreSQL Docker Setup

This directory contains Docker configuration for running PostgreSQL database for the Meeting Scheduler API.

## 🐳 Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Quick Start

1. **Start PostgreSQL Database:**
   ```bash
   cd docker
   docker-compose up -d
   ```

2. **Check if database is running:**
   ```bash
   docker-compose ps
   ```

3. **View logs:**
   ```bash
   docker-compose logs postgres
   ```

### Database Configuration

- **Database Name:** `meeting_scheduler`
- **Username:** `meeting_user`
- **Password:** `meeting_password`
- **Port:** `5432`
- **Host:** `localhost`

### Connection String

For your FastAPI application, use this connection string:
```
postgresql+asyncpg://meeting_user:meeting_password@localhost:5432/meeting_scheduler
```

### Data Persistence

- PostgreSQL data is persisted in `./postgres/data/` directory
- Data survives container restarts and rebuilds
- To reset the database, delete the `postgres/data/` directory

### Management Commands

**Stop the database:**
```bash
docker-compose down
```

**Stop and remove volumes (⚠️ This will delete all data):**
```bash
docker-compose down -v
```

**Rebuild the database container:**
```bash
docker-compose up --build -d
```

**Connect to PostgreSQL directly:**
```bash
docker-compose exec postgres psql -U meeting_user -d meeting_scheduler
```

### Health Check

The container includes a health check that verifies PostgreSQL is ready to accept connections. You can check the health status with:

```bash
docker-compose ps
```

### Environment Variables

Copy `database.env` to `.env` and modify as needed:
```bash
cp database.env .env
```

### Troubleshooting

**Port already in use:**
- Change the port mapping in `docker-compose.yml` from `5432:5432` to `5433:5432`
- Update your application's database URL accordingly

**Permission issues with data directory:**
```bash
sudo chown -R $USER:$USER postgres/data
```

**Reset everything:**
```bash
docker-compose down -v
rm -rf postgres/data
docker-compose up -d
```
