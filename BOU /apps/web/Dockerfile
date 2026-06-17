FROM node:20-alpine

WORKDIR /app

COPY package*.json pnpm-lock.yaml ./
RUN npm install -g pnpm

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]