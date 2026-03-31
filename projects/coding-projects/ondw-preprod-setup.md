# ONDW Pre-Production Environment Setup Guide
**Domain**: `onewei.my`  
**Hosting**: Hostinger Shared Hosting (SSH Access)  
**Created**: March 31, 2026 9:10 AM  
**Purpose**: Safe testing for Service Worker fixes + Push Notifications before production deployment

---

## Pre-Prod Strategy

### Naming Convention
- **Production**: `onewei.my`
- **Pre-Production**: `staging.onewei.my` OR `preprod.onewei.my` (whichever you prefer)

### Key Separation
| Component | Production | Pre-Prod | Notes |
|-----------|-----------|----------|-------|
| Domain | onewei.my | staging.onewei.my | Separate but linked |
| Database | ondewei_production | ondewei_staging | Independent data |
| Files | /public_html/ | /staging/ (or similar) | Separate directories |
| `.env` | Production keys | Test/staging keys | Different credentials |
| Debug Mode | false | true (optional) | Easier debugging |

---

## Step-by-Step Setup

### PHASE 1: SSH & File Structure (Hostinger)

#### 1.1 Connect via SSH
```bash
# SSH into Hostinger
ssh your-username@onewei.my
# or
ssh your-username@your-hostinger-ip

# Verify you're in the right location
pwd  # Should show /home/your-username or /public_html
ls -la  # List current files
```

#### 1.2 Check Current Laravel Structure
```bash
# Navigate to production Laravel root
cd public_html/  # or wherever your production code is

# Verify Laravel files exist
ls -la
# Should show: app, bootstrap, config, database, public, resources, routes, storage, vendor, .env, artisan, etc.

# Check current PHP/MySQL versions
php -v
mysql -V
```

#### 1.3 Create Pre-Prod Directory
```bash
# Go to parent directory
cd ~

# Create staging directory (parallel to production)
mkdir staging
cd staging

# OR if your structure is different, create a subdirectory:
mkdir -p public_html/staging
cd public_html/staging
```

### PHASE 2: Database Setup (Hostinger/MySQL)

#### 2.1 Create Pre-Prod Database
```bash
# Connect to MySQL
mysql -u root -p
# Enter your Hostinger MySQL password

# Create new database for staging
CREATE DATABASE ondewei_staging;

# Create MySQL user for staging (with same permissions)
CREATE USER 'ondewei_staging'@'localhost' IDENTIFIED BY 'secure-password-here';

# Grant privileges
GRANT ALL PRIVILEGES ON ondewei_staging.* TO 'ondewei_staging'@'localhost';
FLUSH PRIVILEGES;

# Verify
SHOW DATABASES;
exit;
```

#### 2.2 Seed Pre-Prod Database
```bash
# Option A: Clone production database (recommended for pre-prod)
# This gives you realistic test data
mysqldump -u ondewei_production -p ondewei_production | \
  mysql -u ondewei_staging -p ondewei_staging
# Enter passwords when prompted

# Option B: Or restore from backup if you have one
# mysql -u ondewei_staging -p ondewei_staging < backup.sql
```

### PHASE 3: Deploy Code to Pre-Prod

#### 3.1 Clone/Copy Laravel Code
```bash
# Navigate to staging directory
cd ~/staging  # (adjust path based on your structure)

# Option A: Clone from GitHub (recommended)
git clone https://github.com/Mhakim38/ONDEWEI-LARAVEL-HAKIM.git .

# Option B: Copy from production (if no Git access)
# cp -r ~/public_html/* .
```

#### 3.2 Install Dependencies
```bash
# Navigate to Laravel root
cd ~/staging/ONDEWEI-LARAVEL-HAKIM  # (adjust if different)

# Install composer dependencies
composer install --no-dev

# Install npm dependencies
npm install

# Build frontend assets
npm run build
```

#### 3.3 Configure `.env` for Pre-Prod
```bash
# Copy production .env as template
cp .env.production .env

# Edit for pre-prod (use your editor - nano or vi)
nano .env

# Key changes to make:
# APP_ENV=staging (instead of production)
# APP_DEBUG=true (optional, for easier debugging)
# APP_URL=https://staging.onewei.my
# DB_DATABASE=ondewei_staging
# DB_USERNAME=ondewei_staging
# DB_PASSWORD=your-secure-password
# Leave other configs similar to production (API keys, etc.)
```

#### 3.4 Generate App Key
```bash
php artisan key:generate

# Run migrations to ensure database is fresh
php artisan migrate --force
php artisan db:seed  # if seeders exist
```

### PHASE 4: Hostinger Domain/Subdomain Setup

#### 4.1 Create Subdomain in Hostinger Control Panel
**Via Hostinger Dashboard**:
1. Go to **Domains** → **Manage** (onewei.my)
2. Click **Create Subdomain**
3. Name: `staging`
4. Root directory: `/staging` or `/public_html/staging` (match your structure from PHASE 1)
5. Save/Confirm

#### 4.2 SSL Certificate for Subdomain
1. Go to **SSL Certificates** in Hostinger
2. Ensure `staging.onewei.my` is included in your SSL (usually auto-added with wildcards)
3. If manual: **Install SSL** for subdomain
4. Verify: `https://staging.onewei.my` should work

#### 4.3 Configure Web Server (if needed)
```bash
# Check if .htaccess exists (for Apache)
cat ~/staging/ONDEWEI-LARAVEL-HAKIM/public/.htaccess

# Should redirect to Laravel. If missing, create one:
# Ask Hostinger support if .htaccess is enabled for subdomains
```

### PHASE 5: Testing Pre-Prod Environment

#### 5.1 Verify Laravel is Running
```bash
# Check Laravel logs
cd ~/staging/ONDEWEI-LARAVEL-HAKIM
tail -f storage/logs/laravel.log

# Or test via browser
# Visit: https://staging.onewei.my
# Should show login page (not error page)
```

#### 5.2 Test Database Connection
```bash
# SSH to test database
php artisan tinker
>>> DB::connection()->getPdo();
>>> // Should return connection object without error
>>> exit
```

#### 5.3 Test Service Worker (with fixes)
```bash
# Now safe to uncomment /public/sw.js
# 1. Edit public/sw.js - uncomment all code
# 2. Clear browser cache (Cmd+Shift+R on staging.onewei.my)
# 3. Check browser DevTools → Application → Service Workers
# 4. Test login/logout cycle for cache conflicts

# Monitor for errors
tail -f storage/logs/laravel.log
```

#### 5.4 Test Push Notifications
```bash
# Push notification API should be accessible:
# GET https://staging.onewei.my/api/push/vapid
# Should return VAPID public key

# Test subscription:
# POST https://staging.onewei.my/api/push/subscribe
# With subscription object in body

# Test sending notification:
# POST https://staging.onewei.my/api/push/send
# With message payload
```

---

## Phase 6: Backup & Maintenance

### Regular Pre-Prod Backups
```bash
# Daily backup of staging database
mysqldump -u ondewei_staging -p ondewei_staging > ~/backups/ondewei_staging_$(date +%Y%m%d).sql

# Or set up automated backups via Hostinger control panel
```

### Sync Pre-Prod with Production
```bash
# When you need fresh production data for testing
cd ~/staging/ONDEWEI-LARAVEL-HAKIM

# Pull latest code from GitHub
git pull origin main

# Dump production database → staging
mysqldump -u ondewei_production -p ondewei_production | \
  mysql -u ondewei_staging -p ondewei_staging

# Run any new migrations
php artisan migrate --force
```

---

## Critical Testing Checklist Before Going Live

- [ ] Service worker installs correctly (check DevTools)
- [ ] Login/logout doesn't cause HTTP 500 or cache issues
- [ ] Push notifications can be subscribed to
- [ ] Push notifications can be sent to subscribed devices
- [ ] User authentication flows work (login, register, OAuth)
- [ ] Database queries are fast (no slow queries)
- [ ] Error logs are clean (no warnings/errors)
- [ ] Verify NO hard-coded paths to onewei.my (should all be dynamic)

---

## Deployment to Production (When Ready)

```bash
# Once pre-prod testing is complete:
# 1. Commit all changes to GitHub
# 2. SSH to production
# 3. git pull origin main
# 4. php artisan migrate --force (if new migrations)
# 5. npm run build (if frontend changes)
# 6. Clear cache: php artisan cache:clear
# 7. Restart queue: php artisan queue:restart (if using queues)
```

---

## Troubleshooting

### Issue: `staging.onewei.my` shows 404
- **Solution**: Verify subdomain is created in Hostinger + root directory is correct
- **Check**: `ls -la ~/staging/` should show Laravel files

### Issue: "Artisan not found"
- **Solution**: Ensure you're in the Laravel root directory
- **Check**: `pwd` should show `.../staging/ONDEWEI-LARAVEL-HAKIM`

### Issue: Database connection error
- **Solution**: Verify `.env` has correct DB_HOST, DB_USERNAME, DB_PASSWORD
- **Check**: `php artisan tinker` → `DB::connection()->getPdo()`

### Issue: Service Worker still not activating
- **Check**: Browser DevTools → Application → Service Workers (look for errors)
- **Solution**: Hard refresh (Cmd+Shift+R) on staging subdomain
- **Note**: May need to unregister old SW first

### Issue: PHP version mismatch
- **Check**: `php -v` on Hostinger
- **Solution**: Update `.env` PHP version or ask Hostinger to update PHP

---

## Resources
- [Laravel 10 Deployment](https://laravel.com/docs/10.x/deployment)
- [Hostinger Laravel Setup](https://www.hostinger.com/tutorials/how-to-install-laravel)
- [MySQL Subdomain Setup](https://www.hostinger.com/tutorials/how-to-add-subdomain)

---

**Status**: Ready for implementation  
**Next Step**: Begin Phase 1 (SSH setup)  
**Estimated Time**: 1-2 hours total setup  
**Risk Level**: Low (separate environment, won't affect production)
