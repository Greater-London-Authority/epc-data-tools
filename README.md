## epc tools

Tools for downloading and cleaning EPC survey data for domestic and non-domestic buildings in London.

### Installation
This package uses poetry. To install poetry follow the instructions [here](https://python-poetry.org/docs/).

Once poetry is installed do:
```
git clone https://github.com/Greater-London-Authority/epc-data-tools.git
cd epc-data-tools
poetry install
```
This will create a virtual environment and install the dependencies. CLI tools will also be installed by poetry (see the pyproject.toml file for a list of CLI commands defined so far). These commands can then be run using poetry run. 

### Usage
Tools are accessed via the CLI, which currently has the following options:
1. download-epc-data

To run:
```
poetry run <command from list>
```

To check the options for a given command:
```
poetry run <command from list> --help
```