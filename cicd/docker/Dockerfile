FROM python:3.9-slim-bullseye as setup_env

RUN apt-get update && apt-get upgrade

ARG PERSONAL_ACCESS_TOKEN=-vhNjRftLU4s-mhYrC4F
ENV PERSONAL_ACCESS_TOKEN=$PERSONAL_ACCESS_TOKEN
RUN echo $PERSONAL_ACCESS_TOKEN

# Copy requirements
COPY cicd/requirements/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

WORKDIR /app

FROM setup_env as alembic_migration

COPY pre_start.sh pre_start_backend.py ./

COPY cicd/config/.env.sample .

RUN chmod +x pre_start.sh && ./pre_start.sh

FROM setup_env as server_run

# Copy app source code
COPY ../.. .

EXPOSE 30111

COPY cicd/config/.env.sample .

RUN chmod +x start.sh

CMD ["./start.sh"]
