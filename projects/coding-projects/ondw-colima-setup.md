# ONDW Docker with Colima (No Docker Desktop GUI)
**Alternative**: Colima (lightweight Docker runtime for Mac)  
**Benefit**: CLI-only, faster, less RAM/CPU usage  
**Created**: March 31, 2026 10:48 AM

---

## What is Colima?

- ✅ Docker CLI without Docker Desktop GUI
- ✅ Lightweight & resource-efficient
- ✅ Uses built-in macOS virtualization (Hypervisor Framework)
- ✅ Same `docker` and `docker-compose` commands
- ✅ Fully compatible with all docker-compose files

**Key Difference**: No Docker Desktop menu bar icon = faster Mac ⚡

---

## Installation

### 1. Install Colima (via Homebrew)

```bash
# Install Colima
brew install colima

# Install Docker CLI (if not already installed)
brew install docker

# (Optional) Install Docker Compose
brew install docker-compose
```

### 2. Start Colima

```bash
# Start Colima daemon
colima start

# Default: 2 CPUs, 4GB RAM
# To customize:
colima start --cpu 4 --memory 8

# Check status
colima status

# Expected output:
# INFO: Colima is running
# INFO: arch: aarch64
# INFO: runtime: docker
# INFO: socket: unix:///Users/hakim/.colima/default/docker.sock
```

### 3. Verify Docker Works

```bash
# Test Docker
docker --version
docker run hello-world

# Should print Docker version and run hello-world image successfully
```

---

## Using with ONDW

### Step 1: Start Colima

```bash
# Terminal 1
colima start

# Keep it running (or run in background)
# colima start &
```

### Step 2: Use Docker Normally

```bash
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM

# Use the minimal docker-compose.yml we created
docker-compose up -d

# All the same commands work:
docker-compose ps
docker-compose logs
docker-compose down
```

### Step 3: Run Laravel Locally

```bash
# Terminal 2
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM

php artisan serve
```

### That's it! 🎉

---

## Useful Colima Commands

```bash
# Start Colima
colima start

# Stop Colima (graceful shutdown)
colima stop

# Restart Colima
colima restart

# Check status
colima status

# View logs
colima logs

# Stop and delete (full reset)
colima delete

# Start with custom resources
colima start --cpu 4 --memory 8

# Start with different architecture
colima start --arch arm64

# SSH into Colima VM (if needed for debugging)
colima ssh

# Inside VM:
# docker ps
# exit
```

---

## Docker Compose with Colima

Use the **minimal docker-compose.yml** (from ondw-docker-minimal.md):

```bash
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM

# Start services (same as Docker Desktop)
docker-compose up -d

# View services
docker-compose ps

# Stop services
docker-compose down

# View logs
docker-compose logs -f mysql
docker-compose logs -f redis
```

---

## Workflow

### Morning: Start Development

```bash
# Terminal 1: Start Colima once
colima start

# Terminal 2: Start Docker services
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM
docker-compose up

# Terminal 3: Run Laravel
cd /Users/hakim/holeeMonth/ONDEWEI-LARAVEL-HAKIM
php artisan serve
```

### Evening: Stop Everything

```bash
# In Terminal 2
docker-compose down

# In Terminal 1
colima stop
```

---

## Comparison: Colima vs Docker Desktop

| Feature | Colima | Docker Desktop |
|---------|--------|----------------|
| Cost | FREE | FREE (for personal use) |
| RAM Usage | ~300MB idle | ~1-2GB idle |
| CPU Overhead | Minimal | High |
| CLI Only | ✅ Yes | No (GUI always running) |
| Hypervisor | Native macOS | Hyperkit |
| docker-compose | ✅ Yes | ✅ Yes |
| Kubernetes | ❌ No | ✅ Yes |
| Use Case | Development | Full suite |

**For ONDW**: Colima is perfect! 💜

---

## Troubleshooting

### Issue: "Cannot connect to Docker daemon"

```bash
# Colima not running
colima start

# Verify
colima status
```

### Issue: "Port already in use"

```bash
# Change MySQL port in docker-compose.yml
ports:
  - "3307:3306"  # Use 3307

# Or kill existing container
docker-compose down -v
```

### Issue: "Out of disk space"

```bash
# Colima uses space in ~/.colima
du -sh ~/.colima

# Clean unused images/volumes
docker system prune -a

# If needed, reset Colima
colima stop
colima delete
colima start
```

### Issue: "MySQL won't start"

```bash
# Check logs
docker-compose logs mysql

# Reset database
docker-compose down -v
docker-compose up -d
```

---

## Next Steps

1. **Install Colima** (5 min)
   ```bash
   brew install colima docker docker-compose
   ```

2. **Start Colima** (1 min)
   ```bash
   colima start
   ```

3. **Create docker-compose.yml** (2 min)
   - Use ondw-docker-minimal.md

4. **Start Docker services** (1 min)
   ```bash
   docker-compose up -d
   ```

5. **Run Laravel** (1 min)
   ```bash
   php artisan serve
   ```

6. **Test Service Worker + Push Notifications**
   - Visit http://localhost:8000
   - Test in browser

---

## Alternatives to Colima (if you prefer)

### Lima
```bash
brew install lima
limactl start
# Similar to Colima, more minimal
```

### OrbStack (Paid)
```bash
# Modern Docker alternative
# Faster than Docker Desktop
# https://orbstack.dev
```

### Native Homebrew PHP + MySQL (No Docker)
```bash
# If you prefer not to use Docker at all:
brew install php@8.1 mysql redis
# But then you need to manage services manually
```

---

**Recommendation**: Use **Colima** - best balance of simplicity and efficiency 🚀

**Status**: Ready to implement  
**Time to Setup**: ~10 minutes total  
**Benefit**: Lightweight, no GUI, same docker-compose commands
