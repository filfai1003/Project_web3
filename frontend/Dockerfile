FROM node:20-bullseye-slim

WORKDIR /app

COPY frontend/package.json ./

RUN npm install --silent --no-audit --progress=false

COPY frontend/ ./

EXPOSE 5173

CMD ["npm","run","dev","--","--host","0.0.0.0","--port","5173"]
