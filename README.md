nl4dv-docker
=================================
NL4DV as a rest service served from a docker container.

### Usage
Pull the image from [Docker Hub](https://hub.docker.com/repository/docker/arpitnarechania/nl4dv)
```bash
docker pull arpitnarechania/nl4dv
```

Run / start the container.
```bash
docker-compose up
```

### API Playground
Open your browser and go to `{localhost, 127.0.0.1, HOST_IP}:8000/docs` depending on your host OS to execute different queries with different configuration settings.


### FAQ
Add your own datasets to the `app/assets/data/` and `app/assets/aliases` files and build the container for local use:
```bash
docker-compose build
docker-compose up
```

### Credits
<a target="_blank" href="https://www.cc.gatech.edu/~anarechania3">Arpit Narechania</a> and <a target="_blank" href="https://github.com/helt">@helt</a>.

### License
The software is available under the [MIT License](https://github.com/nl4dv/nl4dv-docker/blob/master/LICENSE).
