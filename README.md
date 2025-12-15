# 📦 BoxBounty - Web Package Tracking Application

A modern, secure web-based package tracking application that allows you to track shipments from over 2000+ carriers worldwide using the 17Track API. Runs as a Docker container for easy deployment.

---

## 🌟 Features

### Core Functionality
- **Universal Tracking**: Track packages from 2000+ carriers including USPS, UPS, FedEx, DHL, and more
- **Automatic Carrier Detection**: No need to specify the carrier - the system detects it automatically
- **Real-Time Updates**: Get the latest tracking information with detailed event timelines
- **Complete Tracking History**: View every scan and movement of your package
- **Beautiful Modern UI**: Clean, intuitive web interface accessible from any browser
- **Containerized**: Easy to deploy and run anywhere Docker is available

### Tracking Information Displayed
- ✅ Current package status (In Transit, Delivered, etc.)
- ✅ Carrier name and service type
- ✅ Origin and destination countries
- ✅ Days in transit
- ✅ Last update timestamp
- ✅ Complete chronological timeline with locations and descriptions
- ✅ Detailed event history with timestamps

---

## 📋 Prerequisites

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **17Track API Key** - Get yours free at https://api.17track.net
- **Internet connection**

### Check Your Docker Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version
```

---

## 🚀 Quick Start

### Step 1: Get Your API Key

1. Visit https://api.17track.net
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key

### Step 2: Download the Application

Clone or download this repository:

```bash
git clone <repository-url>
cd boxbounty
```

Or create the directory structure manually (see Project Structure below).

### Step 3: Configure Your API Key

**Option A: Using docker-compose.yml (Quick)**

Edit `docker-compose.yml` and replace `YOUR_API_KEY_HERE`:

```yaml
environment:
  - TRACKING_API_KEY=your_actual_17track_api_key_here
```

**Option B: Using .env file (Recommended for Security)**

1. Create a `.env` file in the project root:

```bash
echo "TRACKING_API_KEY=your_actual_17track_api_key_here" > .env
```

2. Update `docker-compose.yml`:

```yaml
services:
  boxbounty:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    restart: unless-stopped
```

3. Add `.env` to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

### Step 4: Build and Run

```bash
# Build and start the application
sudo docker compose up --build

# Or run in detached mode (background)
sudo docker compose up -d --build
```

### Step 5: Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

**That's it!** You're ready to track packages! 🎉

---

## 📁 Project Structure

Your project directory should look like this:

```
boxbounty/
├── Dockerfile              # Docker build instructions
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── .dockerignore          # Files to exclude from Docker build
├── .env                   # API key (create this, don't commit!)
├── .gitignore            # Git ignore file
├── app.py                # Flask application
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Styles
    └── js/
        └── app.js        # Frontend JavaScript
```

---

## 📝 Required Files

### Dockerfile

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### docker-compose.yml

Create a file named `docker-compose.yml`:

```yaml
version: '3.8'

services:
  boxbounty:
    build: .
    ports:
      - "5000:5000"
    environment:
      - TRACKING_API_KEY=YOUR_API_KEY_HERE
    restart: unless-stopped
    volumes:
      - ./app.py:/app/app.py
      - ./templates:/app/templates
      - ./static:/app/static
```

### requirements.txt

Create a file named `requirements.txt`:

```
Flask==3.0.0
requests==2.31.0
Werkzeug==3.0.1
```

**Important:** This file should contain ONLY these three lines, no extra characters or markdown formatting!

### .dockerignore

Create a file named `.dockerignore`:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
.env
.git
.gitignore
*.md
.vscode
.idea
```

---

## 🎮 Docker Commands

### Basic Operations

```bash
# Start the application
sudo docker compose up

# Start in background (detached mode)
sudo docker compose up -d

# Stop the application
sudo docker compose down

# Restart the application
sudo docker compose restart

# Rebuild after code changes
sudo docker compose up --build

# Force rebuild from scratch
sudo docker compose build --no-cache
sudo docker compose up
```

### Viewing Logs

```bash
# View live logs
sudo docker compose logs -f

# View last 100 lines
sudo docker compose logs --tail=100

# View logs for specific container
sudo docker logs boxbounty-boxbounty-1 -f
```

### Managing Containers

```bash
# List running containers
sudo docker ps

# List all containers (including stopped)
sudo docker ps -a

# Stop specific container
sudo docker stop <container-id>

# Remove stopped containers
sudo docker compose rm

# Remove everything (containers, networks, volumes)
sudo docker compose down -v
```

---

## 🔧 Configuration Options

### Changing the Port

If port 5000 is already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Use port 8080 instead
```

Then access at: `http://localhost:8080`

### Production Deployment

For production environments, consider:

```yaml
version: '3.8'

services:
  boxbounty:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    restart: always
    environment:
      - FLASK_ENV=production
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Using with Reverse Proxy (Nginx/Traefik)

Example with Nginx:

```yaml
version: '3.8'

services:
  boxbounty:
    build: .
    expose:
      - "5000"
    env_file:
      - .env
    restart: always
    networks:
      - web

networks:
  web:
    external: true
```

---

## 📱 How to Use

### Track a Package

1. Open your browser to `http://localhost:5000`
2. Enter your tracking number in the search box
3. Click "Track Package" or press Enter
4. View the complete tracking information:
   - Current status and location
   - Carrier and service type
   - Route information
   - Timeline of all tracking events

### Health Check

Verify the application is running correctly:

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "api_key_configured": true
}
```

If `api_key_configured` is `false`, your API key is not set correctly.

---

## 🔧 Troubleshooting

### Issue: "401 Unauthorized" Error

**Symptoms**: Tracking fails with authentication error

**Solutions**:
1. Verify your API key is correct in `docker-compose.yml` or `.env`
2. Check for extra spaces or quotes around the API key
3. Ensure the environment variable name is exactly `TRACKING_API_KEY`
4. Restart the container after changing the API key:
   ```bash
   sudo docker compose down
   sudo docker compose up
   ```

5. Check if the API key is loaded:
   ```bash
   curl http://localhost:5000/health
   ```

### Issue: "Address already in use"

**Symptoms**: Port 5000 is already being used

**Solution**: Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"
```

### Issue: Container Won't Start

**Solutions**:

1. Check the logs:
   ```bash
   sudo docker compose logs
   ```

2. Rebuild from scratch:
   ```bash
   sudo docker compose down
   sudo docker compose build --no-cache
   sudo docker compose up
   ```

3. Check Docker is running:
   ```bash
   sudo systemctl status docker
   ```

### Issue: "No tracking information found"

**Possible Causes**:
- Tracking number is incorrect
- Package is too new (wait 24-48 hours)
- Carrier hasn't updated tracking yet

**Solutions**:
1. Double-check the tracking number
2. Try tracking on the carrier's website directly
3. Wait a few hours and try again

### Issue: Changes Not Reflected

**Symptoms**: Code changes don't appear

**Solution**: Rebuild the container:
```bash
sudo docker compose up --build
```

Or force a complete rebuild:
```bash
sudo docker compose build --no-cache
sudo docker compose up
```

### Issue: "cryptography" or "Flask" Import Errors

**Symptoms**: Python package errors in logs

**Solutions**:
1. Check `requirements.txt` has no extra formatting
2. Rebuild with no cache:
   ```bash
   sudo docker compose build --no-cache
   ```

### Issue: API Rate Limiting

**Symptoms**: Requests failing after many attempts

**Solution**: Wait before trying again, or upgrade your 17Track API plan

---

## 🔐 Security Best Practices

### Protect Your API Key

1. **Never commit `.env` files to version control**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use environment variables, not hardcoded values**
   ```yaml
   # Bad
   environment:
     - TRACKING_API_KEY=abc123xyz

   # Good
   env_file:
     - .env
   ```

3. **Set restrictive file permissions**
   ```bash
   chmod 600 .env
   ```

### Production Deployment

1. **Use Docker secrets** for sensitive data:
   ```yaml
   secrets:
     api_key:
       file: ./api_key.txt
   ```

2. **Enable HTTPS** with a reverse proxy (Nginx, Traefik)

3. **Implement rate limiting** to prevent abuse

4. **Use environment-specific configs**:
   - `.env.development`
   - `.env.production`

5. **Enable Docker health checks**:
   ```yaml
   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
     interval: 30s
     timeout: 10s
     retries: 3
   ```

---

## 📊 Performance & Scaling

### Resource Limits

Add resource constraints to prevent container from consuming too much:

```yaml
services:
  boxbounty:
    build: .
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Multiple Instances

Use Docker Swarm or Kubernetes for scaling:

```bash
# Scale with Docker Compose (simple)
docker compose up --scale boxbounty=3
```

### Caching

Consider adding Redis for caching tracking results:

```yaml
services:
  boxbounty:
    # ... existing config ...
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    restart: always
```

---

## 🌐 Supported Carriers

BoxBounty supports **2000+ carriers** worldwide including:

### North America
- USPS, UPS, FedEx, DHL, Canada Post, Purolator

### Europe
- Royal Mail, DPD, DHL, TNT, Hermes, La Poste

### Asia
- China Post, Japan Post, Singapore Post, Korea Post

### E-commerce Platforms
- Amazon Logistics, Wish, AliExpress, eBay, Shopee

### And Many More!
The 17Track API automatically detects carriers - no manual selection needed.

---

## 📈 Monitoring & Logging

### View Application Logs

```bash
# Real-time logs
sudo docker compose logs -f boxbounty

# Last 100 lines
sudo docker compose logs --tail=100 boxbounty

# Save logs to file
sudo docker compose logs boxbounty > boxbounty.log
```

### Container Stats

```bash
# View resource usage
sudo docker stats

# Specific container
sudo docker stats boxbounty-boxbounty-1
```

### Health Monitoring

Set up automated health checks:

```bash
# Simple health check script
#!/bin/bash
while true; do
  curl -f http://localhost:5000/health || echo "Health check failed!"
  sleep 60
done
```

---

## 🔄 Updates & Maintenance

### Updating the Application

```bash
# Pull latest code
git pull

# Rebuild and restart
sudo docker compose down
sudo docker compose up --build -d
```

### Database Backup (if using)

```bash
# Backup volumes
sudo docker compose down
sudo tar -czf backup.tar.gz ./data

# Restore
sudo tar -xzf backup.tar.gz
sudo docker compose up -d
```

### Cleaning Up

```bash
# Remove unused images
sudo docker image prune

# Remove unused volumes
sudo docker volume prune

# Full cleanup (careful!)
sudo docker system prune -a
```

---

## 🆘 Getting Help

### Check Application Health

```bash
curl http://localhost:5000/health
```

### Check Logs for Errors

```bash
sudo docker compose logs --tail=50
```

### Verify API Key

Check if your API key is working:
1. Visit https://api.17track.net
2. Log in to your dashboard
3. Verify your API key is active
4. Check usage limits

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check API key in .env file |
| Connection refused | Docker not running | Start Docker service |
| Port already in use | Port 5000 busy | Change port in docker-compose.yml |
| No tracking info | Invalid tracking # | Verify tracking number |
| Rate limit exceeded | Too many requests | Wait or upgrade API plan |

---

## 📞 API Information

### 17Track API

- **Documentation**: https://api.17track.net/en/doc
- **API Version**: v2.4
- **Support**: Contact through 17track.net
- **Rate Limits**: Check your plan on 17Track dashboard

### Endpoints Used

- `POST /track/v2.4/register` - Register tracking numbers
- `POST /track/v2.4/gettrackinfo` - Get tracking information

---

## 📄 Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `TRACKING_API_KEY` | Yes | Your 17Track API key | `abc123xyz...` |
| `FLASK_ENV` | No | Flask environment | `production` |
| `PORT` | No | Port to run on (default: 5000) | `8080` |

---

## 🚢 Deployment Examples

### Deploy to Cloud (DigitalOcean, AWS, etc.)

```bash
# SSH to server
ssh user@your-server.com

# Clone repository
git clone <repo-url>
cd boxbounty

# Create .env file
echo "TRACKING_API_KEY=your_key" > .env

# Start application
sudo docker compose up -d

# Check it's running
curl http://localhost:5000/health
```

### Deploy with Portainer

1. Log in to Portainer
2. Go to Stacks
3. Create new stack
4. Paste docker-compose.yml content
5. Add environment variables
6. Deploy

### Deploy to Kubernetes

```bash
# Create secret
kubectl create secret generic boxbounty-secret \
  --from-literal=api-key=your_key_here

# Apply deployment
kubectl apply -f k8s-deployment.yaml
```

---

## ✨ Tips for Best Results

1. **Use the health endpoint** to verify configuration before tracking
2. **Wait 24-48 hours** for new shipments to appear in tracking systems
3. **Copy-paste tracking numbers** to avoid typos
4. **Keep your API key secure** - never commit to version control
5. **Monitor your API usage** on the 17Track dashboard
6. **Set up automatic backups** if storing tracking history
7. **Use a reverse proxy** with HTTPS in production
8. **Enable logging** to troubleshoot issues

---

## 📚 Additional Resources

- **17Track Website**: https://www.17track.net
- **Get API Key**: https://api.17track.net
- **API Documentation**: https://api.17track.net/en/doc
- **Docker Documentation**: https://docs.docker.com
- **Docker Compose Documentation**: https://docs.docker.com/compose
- **Flask Documentation**: https://flask.palletsprojects.com

---

## 🙏 Acknowledgments

- **17Track** for providing the comprehensive tracking API
- **Flask** for the lightweight web framework
- **Docker** for containerization
- All open-source contributors

---

## 📧 Support

For issues with:
- **The API**: Contact 17Track support
- **Docker**: Check Docker documentation
- **Application bugs**: Check logs and troubleshooting section

---

**Happy Tracking! 📦✨**

```
   ___            ___                   _         
  / _ )___ __ __ / _ ) ___  __ _____  / /_ __ __ 
 / _  / _ \\\ \ // _  // _ \/ // / _ \/ __// // / 
/____/\___/_\_\//____/ \___/\_,_/_//_/\__/ \_, /  
                                          /___/   
```
