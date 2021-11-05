FROM node:14-alpine as build-step
RUN mkdir /app
WORKDIR /app
COPY package.json /app
RUN npm install
COPY . /app
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL $REACT_APP_API_URL
RUN npm run build

FROM nginx:1.21.3-alpine
COPY --from=build-step /app/build /usr/share/nginx/html
