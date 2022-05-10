FROM node:16-alpine3.11

COPY package.json .

RUN npm i

COPY . ./

CMD ["npm", "run", "dev"]