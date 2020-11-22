nl4dv-docker
=================================
A docker container for [NL4DV](https://nl4dv.github.io/nl4dv/), an open-source python toolkit that converts a natural language query into data visualizations.

## Pre-requisite
Install Docker by following the instructions on the [official website](https://docs.docker.com/get-docker/). Start the Docker environment.

### Usage
From the command-line OR the GUI, pull the **nl4dv** image from [Docker Hub](https://hub.docker.com/r/arpitnarechania/nl4dv)
```bash
docker pull arpitnarechania/nl4dv
```

Run / start the container.
```bash
docker run -p 8000:80 arpitnarechania/nl4dv:latest
```

### API Playground
Open your browser and go to `{localhost, 127.0.0.1, HOST_IP}:8000/docs` depending on your host OS to execute different queries with different configuration settings.


### FAQ
For developing locally, eventually do the following:
```bash
docker-compose build
docker-compose up
```

### Credits
<a target="_blank" href="https://www.cc.gatech.edu/~anarechania3">Arpit Narechania</a> and <a target="_blank" href="https://github.com/helt">@helt</a>.

### License
The software is available under the [MIT License](https://github.com/nl4dv/nl4dv-docker/blob/master/LICENSE).
