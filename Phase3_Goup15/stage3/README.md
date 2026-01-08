# Stage 3 App

[Streamlit](https://streamlit.io/) is an open source Python framework that allows Python programmers to convert their Python data scripts into web apps quickly, without having to learn front-end development.

Stage3 is a Streamlit app that connects to the PostgreSQL database and presents a dropdown of tables in the public schema. When a table is selected, the Streamlit app connects to the database, retrieves all the data and presents it via a grid that is searchable, sortable and filterable. This app is contained within a single ```main.a

### Setup Streamlit and create the stage3 app

1. The ```uv``` tool to setup and manage Python apps and their dependencies, has been installed within the Devcontainer. To verify, click Terminal->New Terminal Window to create a new terminal and type:

```shell
$ uv --version
uv 0.9.11
```

2. To setup the ```stage3``` app, in the terminal go to the ```workspace``` folder:

```shell
$ uv init stage3
$ cd stage3
$ uv add pandas psycopg2-binary sqlalchemy streamlit
$ source .venv/bin/activate
```

3. Create the Streamlit configuration directory and setup secrets to connect to PostgreSQL database:

```shell
$ mkdir .streamlit
$ touch secrets.toml
```

Open the ```secrets.toml``` file and populate the credentials

```YAML
[database]
host = "postgres"
port = "5432"
database = "hotel_database"
username = "postgres"
password = "changethis"
```

### Run the Streamlit application

1. Open the repository in VSCode and in Devcontainers when prompted
2. Click Terminal->New Terminal to create a new command line terminal
3. Navigate to the ```stage3``` directory, activate the Python virtual environment and run Streamlit:

```shell
$ cd stage3
$ source .venv/bin/activate
$ streamlit run main.py

Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.


  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.19.0.2:8501
  External URL: http://104.48.80.228:8501
```

4. Open [http://localhost:8501] in a browser to access the Streamlit app
5. Switch back to the terminal and press Ctrl+C (Command+C on MacOS) to terminate the Streamlit app