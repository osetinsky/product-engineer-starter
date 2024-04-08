# Use the official Node.js 16 image as a parent image for the build stage
FROM node:16 as builder

# Set the working directory inside the container
WORKDIR /code

# Copy package.json and package-lock.json explicitly
COPY package.json .
COPY package-lock.json .

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Build the application
RUN npm run build

# Start a new stage from node:16 for the final image
FROM node:16

# Set the working directory to /code
WORKDIR /code

# Copy package.json and package-lock.json from the build stage
COPY --from=builder /code/package.json .
COPY --from=builder /code/package-lock.json .

# Copy the build from the previous stage
COPY --from=builder /code/next.config.js ./
COPY --from=builder /code/public ./public
COPY --from=builder /code/.next ./.next
COPY --from=builder /code/node_modules ./node_modules

# Expose the port Next.js runs on
EXPOSE 3000

# Command to run the application (replace "dev" with "start" in production)
CMD ["npm", "run", "start"]
