# Co:Helm Exploration

Hi Co:Helm team! I appreciate you giving me the chance to demo my work. It's an interesting problem.

I've focused most of my time on the backend aspects of the specs your team provided [here](https://co-helm.notion.site/Senior-Product-Engineer-Take-Home-6e82ec45cc2a46b59a0d9ee3aeb9449c).

Thanks for checking it out! Please don't hesitate to reach out with questions.

## Table of Contents

- [Usage](#usage)
- [Notes for the Reviewer](#notes-for-the-reviewer)
- [Next Steps](#next-steps)

## Usage

### Loom Demo
Watch this screencast to see the steps below in action.
[todo: add link]

### Prerequisites

Along with a terminal, you'll just need the following tools to install the software and get the app running:

- git
- docker
- docker-compose

Instructions for installing these [here](https://chat.openai.com/share/afae801d-7caf-42f7-985a-7220c1963c87).

### Quickstart
```
git clone https://github.com/osetinsky/product-engineer-starter.git
cd product-engineer-starter
make start
```

Note that `make start` wraps up most of the detailed steps below into one helper.

### Detailed Steps
#### Setup & Build

To get your development environment up and running:

1. Clone the repository to a directory of your choosing:
    ```bash
    git clone https://github.com/osetinsky/product-engineer-starter.git
    ```
    <br>

2. Navigate to the project directory:
    ```bash
    cd product-engineer-starter
    ```
    <br>

3. Copy the sample development environment variables into usable .env files. 

    ```bash
    make copy-dev-env-vars
    ```

    You should see something like this output on your command line, showing you what it did:
    ```
    $ make copy-dev-env-vars
    cp .env.sample .env
    cp ./frontend/.env.local.sample ./frontend/.env.local
    ```

    You should also see two new files...
    ```
    .env
    ./frontend/.env.local
    ```
    
    ...which will be identical to the `.env.sample` and `./frontend/.env.local.sample` files included in the repo. The *.sample files are useful templates that indicate which environment variables are necessary to run the application, but without including sensitive secrets and other data you'd want to keep out of version control. The copied versions are files that the application will actually depend on to run.
    <br>

4. Build the Docker images for frontend and backend services. Note that we're using docker-compose to set up images for three separate services: db, backend, and frontend
    ```bash
    make build
    ```

    This will take a few minutes. You should see something like:
    ```
    $ make build
    docker-compose build backend frontend
    Sending build context to Docker daemon   10.3kB
    Step 1/13 : FROM python:3.9
    ---> c88de5b9e28e
    Step 2/13 : WORKDIR /code
    ---> Using cache
    ---> 5c81fe696a21
    Step 3/13 : RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*
    ---> Using cache
    ---> b89b2fb90712
    .....
    ```

    While the backend and frontend services each have their own Dockerfile used to construct their respective images for running custom code within containers, we're using the publicly available `postgres:13` image for our development database. For deployments, we'd want to use a different approach for the database, but the setup in `docker-compose.yml` mirrors some aspects of the distributed setup we'd want in production. If you're new to Docker, you can read more about images vs. containers [here](https://circleci.com/blog/docker-image-vs-container/).

#### Booting the Application

To run all services:

```bash
make up
```

This command starts the `db`, `backend`, and `frontend` services defined in your `docker-compose.yml` file, in that sequence. Your backend service won't start until the database service is running, and your frontend service won't start until the backend service is running. `make up` handles this for you. If something goes wrong in the chain of service initializations, the entire container ecosystem will stop (with a helpful error, I hope).

The first time you call `make up`, Docker may have to pull the remote postgres image before running all three services in separate containers:

```
$ make up
docker-compose up -d
[+] Running 15/15
 ✔ db 14 layers [⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿]      0B/0B      Pulled                                                                                                                                 27.0s 
   ✔ 59f5764b1f6d Pull complete                                                                                                                                                         20.1s 
   ✔ cf75f2172685 Pull complete                                                                                                                                                         20.2s 
   ✔ a7354aa82f25 Pull complete                                                                                                                                                         20.4s 
   ✔ 24f2f4668b6a Pull complete                                                                                                                                                         20.5s 
   ✔ ff84ef54facf Pull complete                                                                                                                                                         21.0s 
   ✔ 2047c8c12c2d Pull complete                                                                                                                                                         21.1s 
   ✔ 00a6174203e1 Pull complete                                                                                                                                                         21.1s 
   ✔ e99eea1c16ac Pull complete                                                                                                                                                         21.1s 
   ✔ 27899af34873 Pull complete                                                                                                                                                         26.1s 
   ✔ 118a52b8b426 Pull complete                                                                                                                                                         26.1s 
   ✔ 49e76b6a4749 Pull complete                                                                                                                                                         26.1s 
   ✔ a1aebd6d3023 Pull complete                                                                                                                                                         26.1s 
   ✔ 0306b31906c8 Pull complete                                                                                                                                                         26.1s 
   ✔ b0c8c6d82305 Pull complete                                                                                                                                                         26.1s 
[+] Running 5/5
 ✔ Network product-engineer-starter_default         Created                                                                                                                              0.0s 
 ✔ Volume "product-engineer-starter_postgres_data"  Created                                                                                                                              0.0s 
 ✔ Container product-engineer-starter-db-1          Started                                                                                                                              0.8s 
 ✔ Container product-engineer-starter-backend-1     Started                                                                                                                              0.7s 
 ✔ Container product-engineer-starter-frontend-1    Started  
```

### Applying Migrations

<b>Heads up!</b> You'll need to apply database migrations below in order to test the specifications for the application.

Once the services are running, you'll need to build and run database migrations, namely for the `cases` table. This is necessary for us to write, persist, and fetch `cases` to display to the end-user.

```bash
make build-migrations
make migrate
```

You should see something like:
```
$ make build-migrations
docker-compose exec backend alembic revision --autogenerate -m "generating alembic revision"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'cases'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_cases_created_at'' on '('created_at',)'
INFO  [alembic.autogenerate.compare] Detected added index ''ix_cases_id'' on '('id',)'
  Generating /code/alembic/versions/d6add7c5a754_generating_alembic_revision.py ...  done

$ make migrate         
docker-compose exec backend alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> d6add7c5a754, generating alembic revision
```

This will run Alembic migrations within the backend service's container, updating your database schema.

After this, you should be good to go!

### Accessing the Application

Once you've completed the steps above, you can now access the application in your browser with this link: <b>[http://localhost:3000](http://localhost:3000)</b>

- The frontend application will be available on localhost and whichever port you specify as `CLIENT_PORT` in `.env`
- Although it will mainly be used by the frontend application, the backend API will be available on localhost and whichever port you specify in `NEXT_PUBLIC_SERVER_PORT` in `.env`. Reviewers of the application may want to access the API directly for testing the `GET /cases` endpoint, which returns the list of cases as opposed to a single case in `GET /cases/{case_id}`. To fetch the cases index endpoint, you can run the following assuming the backend is running on port 8000:

```
curl -X GET -H 'Content-Type:application/json' http://localhost:8000/cases/ | jq .
```

If you get an error complaining about `jq`, you can remove the `| jq .` part. But [jq](https://jqlang.github.io/jq/) is helpful for formatting and manipulating JSON on your command line in a more human-readable format.

### Viewing Logs

To view logs from the backend service:

```bash
make be-logs
```

Or frontend service:

```bash
make fe-logs
```

Or containerized database:

```bash
make db-logs
```

### Stopping the Application

To stop all running services:

```bash
make down
```

### Wiping the Database

`docker-compose.yml` makes the postgres DB data accessible to your host machine through `volumes`. This means that it will persist until you wipe your local host machine's database volume. You can do this (with some caution) using:

```bash
make remove-db-volume
```

## Notes for the Reviewer
### Commits
Although you'll see the exercises as three commits made directly to master as suggested, I opened a new branch for each exercise. I merged these as PRs into master and made the commit history more legible by rebasing and removing the merge commits. I just preferred not to push straight to master. You can view those merged PR branches [here](https://github.com/osetinsky/product-engineer-starter/pulls?q=is:pr+is:closed).

### Docker
Docker makes a few things easier, but comes with its costs. Currently, volumes are not exposed for backend and frontend services, meaning that changes made to the code on your host machine won't be reflected in the running containers until you rebuild with `make build`. This can slow down development and is something I'd want to address later, but I still think it's good practice to have my development environment mirror deployment environments and associated dependencies as much as possible. Docker containerization helps with this.

### Missing Exercise 4 (bonus)
While there isn't a dedicated commit for a "bonus" Exercise 4, I did utilize a few extra things that made my development process smoother and should help new users get up and running faster. They snuck their way into the commits for the first 3 exercises:

* Docker/docker-compose: both for orchestrating the frontend, backend, and database. Note that in production, we wouldn't want to use the postgres `db` service defined in `docker-compose.yml`, or perhaps even to use docker-compose at all (AWS had its own `Dockerrun.aws.json` file which was analogous). Instead, we'd want to use something like RDS. For local development, dockerizing the database just makes it easier to get started using a database to persist data. In addition, having separate Dockerfiles for the backend and frontend code makes deployments cleaner and less error prone (AWS ECR works well for container registry).
* Some Pydantic typing on the backend, e.g. backend/app/schemas.py
* Makefile for helper tools such as building the Docker images, running containers, preparing/migrating the database, logging, etc.

## What I'd want do next

The most glaring omissions from this assignment are likely the lack of tests, frontend polish, and something innovative around PDF pre-processing / LLMs.

### Data Processing & Analysis
I was most excited to start making sense of the PDF assets, but didn't get that far:
* Explore possible needs for OCR and other pre-LLM processing of PDFs. Tesseract-OCR looks promising, especially for scanned PDFs like the Mickey Mouse medical-record.pdf. It would be cheaper and faster to pre-process what we can before passing to any 3rd-party LLMs (and I'd think legally necessary to scrub them of any PII before doing so anyway)
* The PII scrubbing is a difficult problem by itself. I've used [scrubadub](https://scrubadub.readthedocs.io/en/stable/) for this purpose, though in the context of financial data.
* Integrate with OpenAI et al for summarizing documents into structured JSON schemas. While their Vision API came to mind, it can get expensive. Several of their other APIs/models would certainly be valuable, but any usage of OpenAI would likely require breaking down the task of summarizing specific types of PDF documents into separate, asynchronous jobs. Each job could employ a dedicated agent that is fine-tuned and carefully prompted for a highly specific task, perhaps even scoped to a particular section of a particular document. Extreme care for user/patient safety and privacy would be a priority for medically-related documents here.
* Investigate pros/cons of using [open source](https://github.com/eugeneyan/open-llms) LLMs

### User Stories, Diagramming, Prototyping, Architecture
* If this were a more open-ended project for end-users, I'd ask more questions from the team and potential users to ensure that the product was designed and architected with the end-user kept top-of-mind
* Work within FigJam/Figma to plot out user stories before making clickable prototypes without code. Then explore using Canva and other Figma plugins for exporting Figma components into modules, though I've had mixed experiences with this approach (I'm still hopeful)
* Architect the system with sequence diagrams to catch as many edge cases before implementation. Also, entity relationship diagrams to ensure we're designing the database in a way that reflects user needs and scalability
* Improve UX and beautify the frontend (a lot). Drop to upload, polling for case status updates, responsiveness, cross-device support, accessibility. CSS/animations for delight. [jitter.video](https://jitter.video/files/) is a great tool that integrates nicely with Figma.

#### Code & Deployments
* Write tests (TDD), particularly for the backend. Unit, integration (including with 3rd party API calls), and when scale might call for it, load testing.
* New kinds of tests that reliance on LLMs might necessitate. Cross-checking outputs of LLMs with professionals to catch serious errors.
* Deploy the application to AWS. Sandbox and Production environments to start. Canary deployments when appropriate. ECS (multi-docker setup), RDS (postgres), auto-scaleable web and worker instances (for API calls and job processing). There will likely be some networking headaches related to security groups and CORS depending on how the backend/frontend are hosted, but nothing too serious. Infrastructure through code with CloudFormation templates is what I'd prioritize.
* Better error handling, monitoring, alerts, and alarms (PagerDuty/CloudWatch)

#### Misc.
* Extract routes logic from main.py into resource-specific files (for example, one for a RESTful cases API)
* Implement real PDF uploads and integration with backend. Hard to say whether form data or encoded data is preferable here.
* Curious about the need for mobile interfaces. Probably low initially.
* Add a smarter "wait-for-it.sh" script that confirms the database is up and running. This could be used in docker-entrypoint.sh and Makefile's DB migration commands `build-migrations` and `migrate`, both of which require the database to be up and running before then can execute.
* Format case_ids to use dashed or underscored format: case_57a2307fe47c4e7a => case_xxxx-xxxx-xxxx-xxxx
* Get access to [Devin](https://www.cognition-labs.com/), even though it may make me irrelevant