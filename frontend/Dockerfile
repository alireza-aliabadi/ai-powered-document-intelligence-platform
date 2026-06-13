# Build stage
FROM node:20-alpine AS builder

WORKDIR /app/frontend

# Copy only package manifests first for better caching
COPY package.json package-lock.json* ./

# Install dependencies (CI mode for reproducible installs)
RUN npm ci --silent

# Copy the rest of the source and build
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app/frontend

# Use a minimal static server for production
RUN npm install -g serve@14 --silent

# Copy built assets
COPY --from=builder /app/frontend/dist ./dist

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=5 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["serve", "-s", "dist", "-l", "3000"]
