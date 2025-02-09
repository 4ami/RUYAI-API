
# Web Auth Micro-Service
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

```
MIT License

Copyright (c) [2025] [Khalid Mahdi Hawkash]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
A lightweight and secure authentication microservice built with FastAPI, designed for user authentication and token-based authorization.

### Features:
- ✅ User registration & login with secure password hashing
- ✅ JWT-based authentication (access & refresh tokens)
- ✅ Asymmetric key handling for token signing & verification
- ✅ Alembic migrations with SQLAlchemy ORM
- ✅ MVC architecture for scalability & maintainability
- ✅ Dockerized for easy deployment

## Setup

Setting up this microserivce is easy in few steps:
1. Clone this repo to your local machine:
```bash
git clone git@github.com:4ami/RUYAI-API.git
```

2. Install dependencies and start the service:
- Docker:
**a.** Build docker image:
```bash
docker build -t web-auth-service
```
**b.** Run docker container:
```bash
docker run -p 3001:3001 web-auth-service
```
**c.** Run migration:
```bash
docker exec -it <container_id> alembic upgrade head
```
`container_id` you can find it using docker ps.
___
- Manually:
**a.** Install *requirements.txt*:

```bash
  pip install --no-cache-dir -r requirements.txt
```
**b.** Configure .env:
`DB_URL` and `DB_ENGINE` I used postgres as database. You are free to use any relational database here, but make sure that you install their required dependencies so they can run well.
**postgres url**: `postgresql://USER:PASSWORD@DATABASE HOST:PORT/DATABASE DB_NAME}`.
**Database engine** is different because it async so the url will be slightly different `postgresql+asyncpg://USER:PASSWORD@DATABASE HOST/DATABASE NAME`.
```
DB_HOST="{Database_host: ex. localhost:5432}"
DB_NAME="{my_database}"
DB_USER="{root}"
DB_PASS="{secret_password}"
DB_URL="{url of database to be used in migration}"
DB_ENGINE="{url of database to be used in connect with database}"
ENV="{development/testing/production} default:development"
```
**c.** Run migration:
```bash
alembic upgrade head
```
**d.** Run FastAPI:
```bash
fastapi dev main.py --port 3001
```
3. You can check service docs through:
```http
http://localhost:3001/docs

or

http://localhost:3001/redoc
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

