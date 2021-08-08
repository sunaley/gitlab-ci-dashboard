# Gitlab-CI-Dashboard

Yes, this is another dashboard for Gitlab CI but it's simple and less configuration.

The project can only be deployed under docker/docker-compose for now.


## Start a instance

### ...via docker-compose

Environment variables:
  - **GITLAB_API_TOKEN** : Access token with read permission from gitlab.
  - **GITLAB_GROUP** : Group name. For now, it can only show the proejcts belong to a specific group.


Create your own **docker-compose.yml**:

```yaml

version: '3.7'

services:
  app:
    image: stanleeley/gitlab-ci-dashboard:0.1.1
    ports:
      - "80:80"
    init: true
    environment:
      GITLAB_API_TOKEN: your_gitlab_token
      GITLAB_GROUP: your_group_name
      GITLAB_API_URL: https://gitlab.com/api/v4/
    volumes:
      - ./config.json:/app/config.json
```

and **config.json**
```json
{
  "hosts": {
    "staging": "http://staging.example.com:{port}" // the port will be replace by `pattern` attribute
  },
  "projects": {
      "example_project": {
        "host": "staging", // host name defined in hosts
        "pattern": {
          "port": 8888 // the value to replace the host url
        }
      }
    }
  }
}
```
then...start the service

```shell
$ docker-compose up
```
or daemonize...
```
$ docker-compose up -d
```
