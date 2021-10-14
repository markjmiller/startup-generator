# Startup Idea Generator

This web application generates ideas for your next billion dollar startup company. Ideas are generated in the form "\<idea> for \<thing>".

![](/readme_images/frontend.png)

## Why?

This is a toy web application and server that demonstrates (most of) the methodology of the [twelve-factor app](https://12factor.net/). It features:
- A simple Python Flask server for the API and Angular app for the frontend.
- Easy integration with MongoDB, but trivially extendible to other databases.
- Dev and production parity for easy development and deployment.
- Almost no custom CSS by leveaging Bootstrap and Angular Material.
- Amazon Elastic Beanstalk configurations for deployment.
- Github actions for full CI/CD.

## Topology

This application is distributed into three parts:
1. Frontend
    - Angular application that is main point of interaction for the user.
2. Admin console
    - Separate Angular application to interact with the database.
3. API
    - REST API written in Python using Flask.
    - Enforces user access control for admin API.

Here is what the service and request topology looks like in a production environment using AWS and MongoDB Atlas:

![](/readme_images/topology.jpg)

In local development, the environment is setup to work without DNS routing snd MongoDB Atlas is replaced with Docker running mongodb.

## Development Getting Started

For development you will need to install:
- Docker
- Python (>=3.9)
- Node.js
- angular/cli

Start the mongodb instance with docker. You can do this in the `infrastructure` directory:
```
> docker-compose up
```
> This is just for development. Do not use in production!

> Use a tool like Robo3T to check the mongodb instance is working. This will also be useful for inspecting data later.

> Alternatively, you could use MongoDB Atlas for your development database.

Next, install the StartupGeneratorAPI package to a virtualenv with `--editable`. Before we start the API application, we will set up some data in our mongodb instance. Create the following python script (or run it in a python console):
```
import pymongo
from StartupGeneratorAPI.utility import add_words_to_db_from_text

client = pymongo.MongoClient('mongodb://words-writer:dev@localhost:27017/app')
add_words_to_db_from_text(r'.\tests\data\word_set_1.txt', 0, client)
add_words_to_db_from_text(r'.\tests\data\word_set_2.txt', 1, client)
```
> Consider using an IDE like PyCharm for this.

After running the above, use Robo3T (or similar) to check documents were added to the `words` collection.

Let's set up the environment variables the API application needs. Use your platform's syntax for setting environment variables:
```
export admin_username=root
export admin_password=root
export mongo_reader_uri=mongodb://words-reader:dev@localhost:27017/app
export mongo_writer_uri=mongodb://words-writer:dev@localhost:27017/app
export flask_secret_key=not_safe_for_deployment_change_me
export serve_static_from=redirect
```
> Change these for production!

Start the API:
```
> startup-generator-api api
```

Go to `http://localhost:5000` and you will see it's live by rendering:
```
Startup Idea Generator API
```

Next step is to serve the admin console at `http://localhost:4200`. Run this in the `admin` directory:
```
ng serve --proxy-config src/proxy.conf.json
```

Instead of going to that url, go to `http://localhost:5000/login` where you will see the admin login:

![](/readme_images/admin_login.png)

Log in with the username and password set above (`root` and `root`), and you will be redirected to the admin console.

![](/readme_images/admin_console.png)

And now for the main event! Start the frontend app in the `frontend` directory:
```
ng serve --proxy-config src/proxy.conf.json --port 4201
```

Go to `http://localhost:4201` and you will see:

![](/readme_images/frontend.png)

## Deployment and CI/CD

Unfortunately we won't cover all that here--that would require several more tutorials! However, checkout the `.elasticbeanstalk` directories in `frontend` and `api` for example Elastic Beanstalk configurations. In an EB production environment, you can set variables from a local machine like this:
```
> eb setenv mongo_reader_uri=<db_uri>/app
```
> Did you know username and password can be encoded right into the mongo_uri? 

The `.github/workflows` show how everything can be built with GitHub's CI and deployed right to both EB and S3.

Search and replace instances of `your-url-here` in this repo to set up the configurations for a production environment.

## Extra

To increase performance of the db queries, you can run the following as an extension to the above python code:
```python
db = client['app']
db['words'].create_index([
    ('word', pymongo.ASCENDING),
    ('set_index', pymongo.ASCENDING)
], unique=True)
```
