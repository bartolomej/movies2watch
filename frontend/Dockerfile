FROM node:16-alpine3.11 as builder

WORKDIR /app

COPY package.json .

RUN npm i

COPY . ./

RUN npm run build

FROM builder as development

WORKDIR /app

COPY --from=builder /app /app

CMD ["npm", "run", "dev"]

FROM builder as production

WORKDIR /app

COPY --from=builder /app/.next /app/.next

CMD ["npm", "run", "start"]