# Develop

RTA is a RESTful API built on top of [NestJS](https://nestjs.com/) and deployed on AWS Lambda using
the [Serverless Framework](https://www.serverless.com/).

## Prerequisites

- Node.js 14+
- Install [Docker](https://www.docker.com/products/docker-desktop)
- Install [The `mongo` Shell](https://docs.mongodb.com/manual/mongo/) optionally
- Install Redis (e.g. `brew install redis` on Mac) optionally to use `redis-cli`

## Environment variables

Copy the `.env.example` file to `.env` and set the appropriate values.

## Local resources

Use the following commands to manage local resources:

- a local redis instance at 127.0.0.1:6379
- a local mongodb instance at 127.0.0.1:5000 (used as the RTA Operations db)
- a local mongodb instance at 127.0.0.1:5001 (used as a client db)
- whatever else we'll need in the future

See [docker-compose.yml](../docker-compose.yml) for more details.

```shell
# start up the resources
npm run docker:start

# stop the resources
npm run docker:stop

# remove the resources
npm run docker:remove

```

## Connect to the local Redis

Redis is used as our caching layer.

```shell
# connect using redis-cli if available
$ redis-cli
127.0.0.1:6379>

# install the javascript version of redis client, note the command is `rdcli`.
# `rdcli` has less features than `redis-cli` but for most cases it suffices.
$ npm install -g redis-cli
$ rdcli
127.0.0.1:6379>
```

## Connect to the local MongoDB instances

For each local mongodb instance, we assign it a custom port to avoid conflicts with other/existing local mongodb
instances.

RTA Operations

```shell
$ mongo --port 5000 -u admin -p secret
```

RTA Client

```shell
$ mongo --port 5001 -u admin -p secret
```

Use the same credentials for Studio 3t, Robo 3T or any other GUI client.

## Start Coding

```shell
# install dependencies
$ npm install

# run tests
$ npm test
$ npm run test:e2e
$ npm run test:coverage

# concurrently starting the local server and watching typescript for changes
$ npm run local
```

If successful, go to http://localhost:3000

You can interact with the API documentation by following the link on the page or set up Postman using these [files](postman).

You can find 3 different envs for postman: dev, qa and local. The same as in case of the .env file, get the appropriate
values from your teammates.
