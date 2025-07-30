FROM node:18.20.4-alpine AS server-deps
WORKDIR /app

# 使用国内镜像源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

COPY .yarnrc package.json yarn.lock ./
RUN yarn config set registry https://registry.npmmirror.com
RUN yarn install --frozen-lockfile

FROM node:18.20.4-alpine AS server-builder
WORKDIR /app

# 使用国内镜像源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

COPY . .
COPY --from=server-deps /app/node_modules ./node_modules
RUN yarn config set registry https://registry.npmmirror.com
RUN yarn build

FROM node:18.20.4-alpine
WORKDIR /app

# 使用国内镜像源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

ENV NODE_ENV production

COPY --from=server-deps /app/node_modules ./node_modules
COPY --from=server-builder /app/dist .
COPY /migrations ./migrations

EXPOSE 3000

CMD ["node", "main.js"]