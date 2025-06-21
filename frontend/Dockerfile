# frontend/Dockerfile

# --- FASE DI BUILD ---
FROM node:lts AS builder

WORKDIR /app

COPY package*.json yarn.lock* ./

RUN yarn install

COPY . .

RUN yarn run build


# --- FASE DI PRODUZIONE ---
FROM nginx:stable-alpine

# Copiamo solo i file statici generati dalla fase di build
# nella cartella pubblica di Nginx.
COPY --from=builder /app/dist /usr/share/nginx/html

# Rimuoviamo la configurazione di default di Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiamo la nostra configurazione custom
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Esponiamo la porta 80, quella di default per Nginx
EXPOSE 80

# Avviamo Nginx
CMD ["nginx", "-g", "daemon off;"]