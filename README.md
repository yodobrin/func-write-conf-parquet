# func-write-conf-parquet

Creating parquet conf table from a given csv file.

## Getting started

Clone the repo
Modify the ```local.setting.json``` pointing to the storage account connection string and the container used.

### Project Structure

The main project folder (<project_root>) can contain the following files:

* **local.settings.json** - Used to store app settings and connection strings when running locally. This file doesn't get published to Azure. To learn more, see [local.settings.file](https://aka.ms/azure-functions/python/local-settings).
* **requirements.txt** - Contains the list of Python packages the system installs when publishing to Azure.
* **host.json** - Contains global configuration options that affect all functions in a function app. This file does get published to Azure. Not all options are supported when running locally. To learn more, see [host.json](https://aka.ms/azure-functions/python/host.json).
* **.vscode/** - (Optional) Contains store VSCode configuration. To learn more, see [VSCode setting](https://aka.ms/azure-functions/python/vscode-getting-started).
* **.venv/** - (Optional) Contains a Python virtual environment used by local development.
* **Dockerfile** - (Optional) Used when publishing your project in a [custom container](https://aka.ms/azure-functions/python/custom-container).
* **tests/** - (Optional) Contains the test cases of your function app. For more information, see [Unit Testing](https://aka.ms/azure-functions/python/unit-testing).
* **.funcignore** - (Optional) Declares files that shouldn't get published to Azure. Usually, this file contains .vscode/ to ignore your editor setting, .venv/ to ignore local Python virtual environment, tests/ to ignore test cases, and local.settings.json to prevent local app settings being published.

Each function has its own code file and binding configuration file ([**function.json**](https://aka.ms/azure-functions/python/function.json)).

### Running the function locally

Run the function locally by opening a terminal and running ```func host start```

This is the URL:

```bash
Functions:

        write_conf: [POST] http://localhost:7071/api/write_conf

```

Use your preffered plugin or application to POST a call:

```rest
POST http://localhost:7071/api/write_conf

{
    "file_name": "my.parquet",
    "file_partition": "d=4",
    "config_file": "config_sample.csv"    
}
```

The code will try and read the ```config_file``` from the location specified in ```local.sttings.json``` ```CONF_CONTAINER``` and write it as parquet to the ```CONF_PARQUET/file_partition/file_name``` under the same storage account.

## Next Steps

* To learn more about developing Azure Functions, please visit [Azure Functions Developer Guide](https://aka.ms/azure-functions/python/developer-guide).

* To learn more specific guidance on developing Azure Functions with Python, please visit [Azure Functions Developer Python Guide](https://aka.ms/azure-functions/python/python-developer-guide).