#!/usr/bin/env bash
set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== AI-Powered Document Intelligence Platform - Docker Setup ===${NC}\n"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Prefer the Docker Compose plugin ("docker compose") but fall back to the v1 binary
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo -e "${RED}Docker Compose plugin not found. Install Docker Compose plugin or docker-compose.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Compose CLI available (${COMPOSE_CMD})${NC}\n"

# Create .env from example if missing
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}Please update .env file with your configuration, especially:${NC}"
    echo -e "  - SECRET_KEY (generate a secure random string)"
    echo -e "  - OPENAI_API_KEY (your OpenAI API key)"
    echo -e "  - Other credentials as needed\n"
fi

# Optional: install frontend deps locally for developer convenience
echo -e "${BLUE}Frontend check (optional)...${NC}"
if [ -d "frontend" ]; then
    if [ ! -d "frontend/node_modules" ]; then
        echo -e "${YELLOW}Skipping automatic frontend npm install. To install locally run:${NC}"
        echo -e "  cd frontend && npm install"
    fi
fi

echo -e "${BLUE}Building Docker images...${NC}"
${COMPOSE_CMD} build --no-cache

echo -e "${GREEN}✓ Docker images built successfully${NC}\n"

echo -e "${BLUE}Starting services...${NC}"
${COMPOSE_CMD} up -d

echo -e "${GREEN}✓ Services started${NC}\n"

echo -e "${BLUE}Waiting briefly for services to initialize...${NC}"
sleep 8

echo -e "${BLUE}Running database migrations...${NC}"
# Use non-interactive exec; fall back to running inside the container if it's not ready yet
set +e
${COMPOSE_CMD} exec -T backend python manage.py migrate --noinput
RET=$?
set -e
if [ $RET -ne 0 ]; then
    echo -e "${YELLOW}Warning: migrations failed or backend not ready yet. You can run:${NC}"
    echo -e "  ${COMPOSE_CMD} exec backend python manage.py migrate"
fi

echo -e "\n${GREEN}✓ Setup steps completed${NC}\n"
echo -e "${BLUE}=== Access Your Services ===${NC}"
echo -e "Backend API:        ${GREEN}http://localhost:8000${NC}"
echo -e "Django Admin:       ${GREEN}http://localhost:8000/admin${NC}"
echo -e "Frontend:           ${GREEN}http://localhost:3000${NC}"
echo -e "Aistor Console:     ${GREEN}http://localhost:9001${NC}"
echo ""
echo -e "${BLUE}=== Useful Commands (using ${COMPOSE_CMD}) ===${NC}"
echo -e "View logs:          ${COMPOSE_CMD} logs -f"
echo -e "View frontend logs: ${COMPOSE_CMD} logs -f frontend"
echo -e "Stop services:      ${COMPOSE_CMD} stop"
echo -e "Restart services:   ${COMPOSE_CMD} restart"
echo -e "Django shell:       ${COMPOSE_CMD} exec backend python manage.py shell"
echo -e "Create superuser:   ${COMPOSE_CMD} exec backend python manage.py createsuperuser"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Create a superuser: ${COMPOSE_CMD} exec backend python manage.py createsuperuser"
echo "2. Visit http://localhost:8000/admin to log in"
echo "3. Visit http://localhost:3000 to access the frontend"
echo "4. Configure Aistor buckets at http://localhost:9001"
echo ""
echo -e "For detailed documentation, see DOCKER_SETUP.md"
