# # define an alias for the specific python version used in this file.
# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS python

# # Python build stage
# FROM python AS python-build-stage

# ARG APP_HOME=/app

# WORKDIR ${APP_HOME}

# # we need to move the virtualenv outside of the $APP_HOME directory because it will be overriden by the docker compose mount
# ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# # Install apt packages
# RUN apt-get update && apt-get install --no-install-recommends -y \
#     # dependencies for building Python packages
#     build-essential \
#     # psycopg dependencies
#     libpq-dev \
#     gettext \
#     wait-for-it

# # Requirements are installed here to ensure they will be cached.
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     --mount=type=bind,source=uv.lock,target=uv.lock:rw \
#     uv sync --no-install-project

# COPY . ${APP_HOME}

# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     --mount=type=bind,source=uv.lock,target=uv.lock:rw \
#     uv sync

# # devcontainer dependencies and utils
# RUN apt-get update && apt-get install --no-install-recommends -y \
#     sudo git bash-completion nano ssh

# # Create devcontainer user and add it to sudoers
# RUN groupadd --gid 1000 dev-user \
#     && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
#     && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
#     && chmod 0440 /etc/sudoers.d/dev-user

# ENV PATH="/${APP_HOME}/.venv/bin:$PATH"
# ENV PYTHONPATH="${APP_HOME}/.venv/lib/python3.13/site-packages:$PYTHONPATH"

# COPY ./compose/local/fastapi/start /start
# RUN sed -i 's/\r$//g' /start
# RUN chmod +x /start

# ENTRYPOINT [ "/start" ]

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS python

WORKDIR /app

# 1. Force the venv OUTSIDE the mount point (/app)
ENV UV_PROJECT_ENVIRONMENT=/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# Install system deps (Build + Dev tools)
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential libpq-dev gettext wait-for-it \
    sudo git bash-completion nano ssh \
    && rm -rf /var/lib/apt/lists/*

# 2. Install dependencies (Cached Layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project

# 3. Setup User
RUN groupadd --gid 1000 dev-user \
    && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
    && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
    && chmod 0440 /etc/sudoers.d/dev-user

# 4. Copy Start Script
COPY ./compose/local/fastapi/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

# Update PATH
ENV PATH="/venv/bin:$PATH"

# Copy rest of the app (though Compose will likely override this)
COPY . .

ENTRYPOINT [ "/start" ]