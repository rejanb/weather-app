FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy application files
COPY . .

# Expose React's default port
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
