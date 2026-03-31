# ONDW Docker Setup - Database + Cache Only
**Services**: MySQL + Redis (No app container)  
**Local App**: Run Laravel on Mac directly  
**Created**: March 31, 2026 10:45 AM

---

## Quick Start

```bash
# 1. Navigate to ONDW repo
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM

# 2. Create docker-compose.yml (see below)
# 3. Start Docker
docker-compose up -d

# 4. Access:
#    - MySQL: localhost:3306
#    - Redis: localhost:6379

# 5. Run Laravel locally on your Mac
php artisan serve
# Access at http://localhost:8000
```

---

## File: `docker-compose.yml`

Save this in `/Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM/docker-compose.yml`:

```yaml
version: '3.8'

services:
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

## Setup Local Environment

### 1. Create `.env` for Local Development

```bash
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM

# Copy from example
cp .env.example .env

# Or create/edit .env with these values:
```

**`.env` content:**
```env
APP_NAME=OnDeWei
APP_ENV=local
APP_DEBUG=true
APP_KEY=base64:YOUR_KEY_HERE

APP_URL=http://localhost:8000

DB_CONNECTION=mysql
DB_HOST=127.0.0.1        # Connect to Docker container
DB_PORT=3306
DB_DATABASE=ondewei_local
DB_USERNAME=ondewei_user
DB_PASSWORD=user_password

CACHE_DRIVER=redis
REDIS_HOST=127.0.0.1     # Connect to Docker container
REDIS_PORT=6379

QUEUE_CONNECTION=redis
SESSION_DRIVER=redis

# Mail (local testing)
MAIL_MAILER=log
MAIL_FROM_ADDRESS=test@ondw.local

# Keep Google auth keys (or use test keys)
GOOGLE_CLIENT_ID=your-test-id
GOOGLE_CLIENT_SECRET=your-test-secret
```

### 2. Install Dependencies Locally

```bash
# Install Composer dependencies
composer install

# Install NPM dependencies
npm install

# Generate app key
php artisan key:generate

# Build frontend assets
npm run build
```

### 3. Setup Database

```bash
# Start Docker first
docker-compose up -d

# Wait for MySQL to be healthy (15-30 seconds)
sleep 20

# Run migrations
php artisan migrate --force

# (Optional) Seed with test data
# php artisan db:seed
```

---

## Running the Application

### Terminal 1: Start Docker
```bash
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM

docker-compose up
# Leaves logs visible, press Ctrl+C to stop
```

### Terminal 2: Run Laravel Locally
```bash
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM

# Install dependencies (if not done)
composer install

# Serve Laravel
php artisan serve

# Starts at http://localhost:8000
```

### Access the App
- **App**: http://localhost:8000
- **Database**: localhost:3306 (via local Laravel)
- **Cache**: localhost:6379 (via local Laravel)

---

## Useful Commands

### Docker Management
```bash
# Start Docker services
docker-compose up -d

# Stop Docker services
docker-compose down

# View logs
docker-compose logs -f

# Stop and remove data
docker-compose down -v
```

### Laravel Commands (run on Mac terminal)
```bash
# Migrations
php artisan migrate
php artisan migrate:rollback
php artisan migrate:fresh

# Clear cache/config
php artisan cache:clear
php artisan config:clear

# Database
php artisan tinker
php artisan db:seed

# Test
php artisan test

# Serve
php artisan serve --port=8000
php artisan serve --port=8001  # Use different port if 8000 is taken
```

### Direct Database Access (if needed)
```bash
# Connect to MySQL from Mac terminal
mysql -h 127.0.0.1 -u ondewei_user -p ondewei_local
# Password: user_password

# Or via Docker
docker exec -it ondw-mysql mysql -u ondewei_user -p ondewei_local
```

### Direct Redis Access (if needed)
```bash
# Connect to Redis
redis-cli -h 127.0.0.1 -p 6379

# Or via Docker
docker exec -it ondw-redis redis-cli
```

---

## Testing Service Worker + Push Notifications

### 1. Start Services
```bash
# Terminal 1
docker-compose up

# Terminal 2
php artisan serve
```

### 2. Test Service Worker
- Visit http://localhost:8000
- Open DevTools → Application → Service Workers
- Should show registered service worker
- Hard refresh: Cmd+Shift+R
- Check console for messages

### 3. Test Push Notifications API
```bash
# In browser console or with curl
curl http://localhost:8000/api/push/vapid

# Should return:
# {"publicKey":"BC0k_B6fYU..."}
```

### 4. Test in App
- Navigate to admin section with push notification test component
- Click "Enable Notifications"
- Subscribe to push notifications
- Send test notification (if button available)
- Should appear as browser notification

---

## Debugging

### Issue: "Connection refused" on Laravel commands

**Problem**: Docker services not running
```bash
# Check status
docker-compose ps

# Expected: Both services should show "Up"
```

**Solution**:
```bash
# Make sure Docker is running
docker-compose up -d
sleep 20  # Wait for MySQL to start
```

### Issue: "Can't connect to MySQL server"

```bash
# Verify MySQL is healthy
docker-compose ps mysql

# Check logs
docker-compose logs mysql

# Test connection
docker exec ondw-mysql mysqladmin -u root -proot_password ping
# Should return: mysqld is alive
```

### Issue: Redis connection error

```bash
# Verify Redis is running
docker-compose ps redis

# Test connection
docker exec ondw-redis redis-cli ping
# Should return: PONG
```

### Issue: Port already in use

```bash
# Change ports in docker-compose.yml:
ports:
  - "3307:3306"  # Use 3307 instead of 3306
  - "6380:6379"  # Use 6380 instead of 6379

# Then update .env to match:
DB_PORT=3307
REDIS_PORT=6380
```

---

## Workflow: Local Dev → Hostinger Staging → Production

### Phase 1: Local Docker (NOW)
✅ MySQL + Redis in Docker  
✅ Laravel app runs locally on Mac  
✅ Test service worker fixes  
✅ Test push notifications  

### Phase 2: Hostinger Staging (WHEN READY)
- SSH to Hostinger
- Create staging.onewei.my subdomain
- Deploy code with same fixes
- Test on real server (HTTPS, real domain)
- Verify service worker works on production-like environment

### Phase 3: Production (FINAL)
- Deploy to onewei.my
- Monitor for any issues
- All tests passed ✅

---

## Stopping & Cleanup

```bash
# Stop everything
docker-compose down

# Stop and remove data (fresh start next time)
docker-compose down -v

# Stop just Laravel server (Ctrl+C in Terminal 2)
# Keep Docker running

# Stop just Docker (keep Laravel code)
docker-compose stop
```

---

**Status**: Ready to use  
**Next Step**: Create docker-compose.yml and run `docker-compose up -d`  
**Benefit**: Lightweight local development with isolated database/cache  
**No Bloat**: Laravel app runs natively on Mac (fastest development) 💜
