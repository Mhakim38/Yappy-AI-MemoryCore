# ONDW Full Docker Stack (PHP-FPM + Nginx + MySQL + Redis)
**Setup**: Complete containerized environment (nothing on Mac except Colima)  
**Services**: PHP 8.1 FPM, Nginx, MySQL 8.0, Redis 7  
**Created**: March 31, 2026 10:58 AM

---

## My Suggestion: YES! ✅

Running everything in Docker is **better** because:
- ✅ Same environment locally as production
- ✅ No need to install PHP/Composer on Mac
- ✅ Cleaner Mac (only Colima runs)
- ✅ Consistent across team
- ✅ Easy to scale to production

**Images you'll use:**
```
1. php:8.1-fpm           # PHP application
2. nginx:alpine          # Web server
3. mysql:8.0             # Database
4. redis:7-alpine        # Cache
```

---

## File: `docker-compose.yml`

Save in `/Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM/docker-compose.yml`:

```yaml
version: '3.8'

services:
  # PHP-FPM Application
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ondw-app
    working_dir: /app
    environment:
      - APP_ENV=local
      - APP_DEBUG=true
      - APP_KEY=base64:YOUR_KEY_HERE
      - APP_URL=http://localhost
      - DB_CONNECTION=mysql
      - DB_HOST=mysql
      - DB_PORT=3306
      - DB_DATABASE=ondewei_local
      - DB_USERNAME=ondewei_user
      - DB_PASSWORD=user_password
      - CACHE_DRIVER=redis
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - QUEUE_CONNECTION=redis
      - SESSION_DRIVER=redis
    volumes:
      - .:/app
      - ./storage:/app/storage
      - ./bootstrap/cache:/app/bootstrap/cache
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - ondw-network

  # Nginx Web Server
  nginx:
    image: nginx:alpine
    container_name: ondw-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - .:/app
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx-default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
    networks:
      - ondw-network

  # MySQL Database
  mysql:
    image: mysql:8.0
    container_name: ondw-mysql
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: ondewei_local
      MYSQL_USER: ondewei_user
      MYSQL_PASSWORD: user_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - ondw-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: ondw-redis
    ports:
      - "6379:6379"
    networks:
      - ondw-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      timeout: 10s
      retries: 5

volumes:
  mysql_data:

networks:
  ondw-network:
    driver: bridge
```

---

## File: `Dockerfile`

Save in `/Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM/Dockerfile`:

```dockerfile
FROM php:8.1-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    zip \
    unzip \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libonig-dev \
    libxml2-dev \
    libpq-dev \
    && docker-php-ext-install -j$(nproc) \
        pdo_mysql \
        mbstring \
        exif \
        pcntl \
        bcmath \
        gd \
        redis \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Install Node.js (for npm/frontend build)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install PHP dependencies
RUN composer install --no-interaction --no-ansi

# Install Node dependencies and build
RUN npm install && npm run build

# Create storage directories
RUN mkdir -p storage/logs storage/app/private \
    && chmod -R 777 storage bootstrap/cache

# Expose PHP-FPM port (for Nginx)
EXPOSE 9000

CMD ["php-fpm"]
```

---

## File: `nginx.conf`

Save in `/Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM/nginx.conf`:

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types text/plain text/css text/xml text/javascript 
               application/x-javascript application/xml+rss 
               application/javascript application/json;

    include /etc/nginx/conf.d/*.conf;
}
```

---

## File: `nginx-default.conf`

Save in `/Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM/nginx-default.conf`:

```nginx
upstream php-upstream {
    server app:9000;
}

server {
    listen 80;
    server_name localhost;
    root /app/public;

    index index.php index.html index.htm;

    # Logs
    error_log /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;

    # Client upload limit
    client_max_body_size 100M;

    # Deny access to hidden files
    location ~ /\. {
        deny all;
    }

    # Deny access to storage
    location ~ ^/storage/ {
        deny all;
    }

    # Main rewrite rule - send all to Laravel
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # PHP-FPM
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass php-upstream;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }

    # Static assets (cache)
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Status page (optional)
    location /nginx-health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

---

## Setup Instructions

### 1. Copy Files to ONDW Directory

```bash
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM

# Create the three files above:
# - docker-compose.yml
# - Dockerfile
# - nginx.conf
# - nginx-default.conf
```

### 2. Start Colima

```bash
# Terminal 1
colima start
```

### 3. Build and Start Containers

```bash
# Terminal 2
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM

# Build Docker images
docker-compose build

# Start all services
docker-compose up -d

# Wait 10-15 seconds for services to start
sleep 15
```

### 4. Setup Database & App

```bash
# Run migrations
docker-compose exec app php artisan migrate --force

# (Optional) Seed test data
docker-compose exec app php artisan db:seed

# Generate app key (if not done)
docker-compose exec app php artisan key:generate
```

### 5. Access the App

```
http://localhost
```

Done! 🎉

---

## Useful Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f app
docker-compose logs -f nginx
docker-compose logs -f mysql
docker-compose logs -f redis

# Execute commands in app container
docker-compose exec app php artisan tinker
docker-compose exec app php artisan migrate
docker-compose exec app php artisan cache:clear

# Connect to MySQL
docker-compose exec mysql mysql -u ondewei_user -p ondewei_local
# Password: user_password

# Connect to Redis
docker-compose exec redis redis-cli

# Stop all services
docker-compose down

# Stop and remove data
docker-compose down -v

# Rebuild (after code changes)
docker-compose build
docker-compose up -d
```

---

## Testing Service Worker + Push Notifications

### 1. Start Services
```bash
docker-compose up -d
```

### 2. Test App
- Visit http://localhost
- Login with test account

### 3. Test Service Worker
- DevTools → Application → Service Workers
- Should show registered SW
- Hard refresh: Cmd+Shift+R

### 4. Test Push Notifications
```bash
# Check VAPID endpoint
curl http://localhost/api/push/vapid

# Should return:
# {"publicKey":"BC0k_B6fYU..."}
```

---

## Workflow

### Daily Development

```bash
# Terminal 1: Start Colima (once)
colima start

# Terminal 2: Start Docker services (once)
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM
docker-compose up

# Now just edit code and refresh browser
# http://localhost
```

### After Code Changes

```bash
# Rebuild if Dockerfile/dependencies changed
docker-compose build

# Or just restart without rebuilding
docker-compose restart
```

### When Done

```bash
docker-compose down
colima stop
```

---

## Comparison: Full Docker vs Local PHP

| Aspect | Full Docker | Local PHP |
|--------|-----------|-----------|
| Setup Time | 5-10 min | 5-10 min |
| Mac Cleanliness | ✅ Clean | ❌ Installs on Mac |
| Production Consistency | ✅ Perfect match | ⚠️ May differ |
| Performance | Good (Colima) | Slightly faster |
| Learning Curve | Medium | Low |
| Team Consistency | ✅ Everyone same env | ❌ May vary |

**Recommendation**: Full Docker is better for team projects! 🚀

---

**Status**: Ready to implement  
**Images**: php:8.1-fpm, nginx:alpine, mysql:8.0, redis:7-alpine  
**Time to Setup**: ~10 minutes  
**Benefits**: Clean Mac, production-like environment, easy scaling  

Ready? 💜
