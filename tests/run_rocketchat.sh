docker run --name rocket_db -d mongo:3.3 --smallfiles
docker run --name rocketchat --link rocket_db:secure.gravatar.com --link rocket_db:db -p 3000:3000 -d rocket.chat:0.58

docker logs -f rocketchat