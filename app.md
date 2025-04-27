# Deployment Instructions for Shiny, WordPress, and Caddy Reverse Proxy

This document outlines the deployment process for hosting a Python Shiny application, WordPress, and Caddy reverse proxy, based on the configurations found in the `commercial-computing` repository.

## Overview of Services
1. **Python Shiny**:
   - A Python web application framework that will be hosted inside an iframe on the WordPress frontend.

2. **WordPress**:
   - A content management system (CMS) secured behind a login page.
   - Integrated with a MariaDB database for content storage.

3. **Caddy Reverse Proxy**:
   - Handles routing to the appropriate service (Shiny or WordPress).
   - Manages HTTPS using Let's Encrypt and enforces security headers.

---

## Directory Structure

The following directory structure is assumed:

```
webapp/
├── shiny/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── app.py  # Main Python Shiny app
├── wordpress/
│   ├── docker-compose.yml
│   ├── caddy/
│   │   ├── Caddyfile
│   │   └── caddy_data/  # SSL data (auto-generated)
│   ├── wordpress/
│   │   ├── html/
│   │   │   ├── wp-config-docker.php
│   │   │   ├── wp-content/  # WordPress content (plugins, themes, etc.)
│   │   └── mysql/  # Database files (auto-generated)
│   └── custom.ini  # PHP configuration (if needed)
├── api/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── api.py  # Flask API (if relevant)
```

---

## Configuration Details

### 1. **Python Shiny Service**

#### Dockerfile
The `Dockerfile` defines the Python Shiny service:

```dockerfile name=webapp/shiny/Dockerfile
FROM python:3.13.3-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

EXPOSE 8080

CMD ["shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "8080"]
```

#### Docker Compose
The `docker-compose.yml` file for Shiny:

```yaml name=webapp/shiny/docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - NAME=World
```

---

### 2. **WordPress Service**

#### Docker Compose
The `docker-compose.yml` file for WordPress, MariaDB, and Caddy:

```yaml name=webapp/wordpress/docker-compose.yml
services:
  caddy:
    image: caddy:2.8.4-alpine
    container_name: caddy
    env_file: .env
    ports:
      - 80:80
      - 443:443
    volumes:
      - ./caddy/caddy_data:/data
      - ./caddy/caddy_config:/config
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile
      - ./wordpress/html:/var/www/html

  wordpress:
    image: wordpress:fpm-alpine
    container_name: wordpress
    restart: always
    depends_on:
      - db
    volumes:
      - ./wordpress/html:/var/www/html
      - ./wordpress/custom.ini:/usr/local/etc/php/conf.d/custom.ini
    env_file: .env

  db:
    image: mariadb:10.11.6-jammy
    restart: always
    volumes:
      - ./wordpress/mysql:/var/lib/mysql
    env_file: .env
```

#### WordPress Configuration
The `wp-config-docker.php` file:

```php name=webapp/wordpress/wordpress/html/wp-config-docker.php
<?php
// Database settings
define( 'DB_NAME', getenv_docker('WORDPRESS_DB_NAME', 'wordpress') );
define( 'DB_USER', getenv_docker('WORDPRESS_DB_USER', 'example username') );
define( 'DB_PASSWORD', getenv_docker('WORDPRESS_DB_PASSWORD', 'example password') );
define( 'DB_HOST', getenv_docker('WORDPRESS_DB_HOST', 'mysql') );
?>
```

---

### 3. **Caddy Reverse Proxy**

#### Caddyfile
The `Caddyfile` defines routing for Shiny and WordPress:

```caddyfile name=webapp/wordpress/caddy/Caddyfile
{$SERVER_NAME} {
    root * /var/www/html
    encode zstd gzip

    # Serve WordPress PHP files through php-fpm:
    php_fastcgi wordpress:9000

    # Enable the static file server:
    file_server {
        precompressed gzip
    }
    header / {
        X-Frame-Options "SAMEORIGIN"
        X-Content-Type-Options "nosniff"
    }

    redir /shiny /shiny/
    handle_path /shiny/* {
        reverse_proxy shiny-web-1:8080
    }
}
```

---

## Deployment Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/bravosixgoingdark/commercial-computing.git
   cd commercial-computing
   ```

2. **Set Up Environment Variables**
   Create an `.env` file in `webapp/wordpress` with the following:
   ```env
   SERVER_NAME=your-domain.com
   WORDPRESS_DB_NAME=wordpress
   WORDPRESS_DB_USER=wordpress
   WORDPRESS_DB_PASSWORD=securepassword
   WORDPRESS_DB_HOST=db
   ```

3. **Start Services**
   Use Docker Compose to start each service:
   ```bash
   cd webapp/shiny
   docker-compose up -d

   cd ../wordpress
   docker-compose up -d
   ```

4. **Access Services**
   - WordPress: `https://your-domain.com/`
   - Shiny: `https://your-domain.com/shiny/`

5. **Secure WordPress**
   - Install security plugins (e.g., Wordfence, Loginizer).
   - Use strong passwords for the admin account.

6. **Monitor Logs**
   Use Docker logs to monitor:
   ```bash
   docker logs caddy
   docker logs shiny-web-1
   docker logs wordpress
   ```

---

## Additional Notes

- **HTTPS Configuration**: Caddy automatically generates SSL certificates via Let's Encrypt.
- **Scaling**: If traffic increases, you can scale Shiny or WordPress by adding more replicas in Docker Compose.
- **Customizations**: Modify the Caddyfile for custom routing rules or headers.

