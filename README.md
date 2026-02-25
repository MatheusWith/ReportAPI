# CEM - Central Execution Multi-database

**CEM** is a high-performance API built with **FastAPI**, designed to centralize and standardize access to various database instances (DBAs). It acts as an abstraction layer that allows querying sales data and generating consolidated reports in an asynchronous and strictly typed manner.

## 🚀 Technologies

- **Python 3.12+**: Utilizing the new Generics syntax (PEP 695).
- **FastAPI**: Modern web framework for building APIs.
- **Pydantic V2**: Data validation and schema transformation.
- **SQLAlchemy (Async)**: Asynchronous communication with the database.
- **Docker**: Containerization for isolated environments.

---

## ⚙️ Configuration (Environment Variables)

The application is configured via environment variables. For local execution, ensure these values are defined in your `.env` file or within the `docker-compose.local.yml`:

### 📋 App & Environment

| Variable               | Default Value | Description                                     |
| :--------------------- | :------------ | :---------------------------------------------- |
| `APP_NAME`             | `ReportApi`   | Name of the application.                        |
| `ENVIRONMENT`          | `local`       | Environment (`local`, `staging`, `production`). |
| `GLOBAL_GENERIC_LIMIT` | `60`          | Request rate limit (Slowapi).                   |

### 🗄️ Database Settings (Postgres)

| Variable               | Value          | Description                             |
| :--------------------- | :------------- | :-------------------------------------- |
| `DBAPOSTGRES_USER`     | `dba`          | Database user.                          |
| `DBAPOSTGRES_PASSWORD` | `dba`          | Database password.                      |
| `DBAPOSTGRES_SERVER`   | `dba`          | Database host/server.                   |
| `DBAPOSTGRES_PORT`     | `5432`         | Database port.                          |
| `DBAPOSTGRES_DB`       | `dba`          | Database name.                          |
| `BASE_FILE`            | `src/app/sql/` | Base path for external SQL query files. |

### 🪵 Logging & Monitoring

The API features two independent logging systems:

- **File Logger:** Detailed JSON logs with file rotation (`MAX_BYTES=10MB`).
- **Console Logger:** Human-readable formatted logs for development.
- **Middlewares:** Includes `REQUEST_ID`, `CLIENT_HOST`, and `STATUS_CODE` in every request log.

### 🔐 CORS & Compression

- **CORS:** Configured via `CORS_ORIGINS`, `CORS_METHODS`, and `CORS_HEADERS` (Default: `["*"]`).
- **GZip:** Active compression for responses larger than `1000` bytes (level `6`).

---

## 🏗️ Data Architecture (Schemas)

The application uses inherited class structures to ensure strict data contracts:

- **`ResponseData[T]`**: Contains the list of items (`datas`) and total record count (`count`).
- **`PaginatedResponse[T]`**: Extension including navigation metadata (`current_page`, `per_page`, `total_pages`).
- **`Vend` Entity**: The core model featuring **Auto-Strip** (removes whitespace from strings) and **Null-to-Zero** (converts null monetary values to `0.00`) via Pydantic validators.

---

## 🛣️ Endpoints (API Reference)

### 1. Paginated Sales List

- **Route:** `GET /dba/vend/`
- **Params:** `start_date`, `end_date`, `current_page`, `per_page`.
- **Response:** `PaginatedResponse[Vend]`
- **Usage:** Best for UI tables and grids with pagination.

### 2. Sales Report

- **Route:** `GET /dba/vend/report/`
- **Params:** `start_date`, `end_date`, `all_items`, `quantity`.
- **Response:** `ResponseData[Vend]`
- **Usage:** Management reports and volume analysis.

---

## 🐳 Running with Docker

To spin up the local development environment:

```bash
docker-compose -f docker-compose.local.yml up
```
