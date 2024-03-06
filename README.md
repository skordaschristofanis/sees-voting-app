# SEES-Voting-App

![License](https://img.shields.io/badge/license-MIT-orange.svg) ![Python](https://img.shields.io/badge/python-v3.11-22558a.svg?logo=python&color=22558a) ![Flask](https://img.shields.io/badge/Flask-v3.0.2-3b9388.svg?logo=fastapi&color=3b9388)

A simple Flask web application to help with the voting for the SEES user representative elections. 

------------
## Table of Contents

- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

------------
## Installation

To install and use the project clone the repository and navigate into the project directory:

```bash
git clone https://github.com/skordaschristofanis/sees-voting-app.git && cd sees-voting-app
```

### Requirements

Before you begin, ensure you have met the following requirements:

>  Python >= 3.11  
>
> You can install the packages below using the requirements file!  
> flask=>3.0.2  
> flask-mailman=>1.0.0  
> flask-wtf=>1.2.1  
> email-validator=>2.1.1  
> python-dotenv=>1.0.1  
> gunicorn=>21.2.0

Run the below command to install the package requirements
```python
pip install -r requirements.txt
```

### Configuration

Before starting the web server, there is some configuration steps that are needed.

1. Rename the data-example forlder to data and move in to that folder.
2. Rename the .env-example to .env and fill in the correct values for the variables.
3. Edit the candidates.csv file and put the desired names with their bio link. Make sure to keep the same format for the csv file.

### Running the Server
After setting up and configuring the project, you can start the Gunicorn server by running the [voting_app.py](voting_app.py) file:

#### Production
```bash
python voting_app.py
```

#### Debug mode
For debug mode you can use the --debug or -d flag:
```bash
python voting_app.py --debug
```

[back to top](#table-of-contents)


### Vote results
To combine the results to a signle file, you can use the flag --results or -r when running the [voting_app.py](voting_app.py) file.
```bash
python voting_app.py --results
```

------------
## Contributing

All contributions to SEES-Voting-App are welcome! Here are some ways you can help:
- Report a bug by opening an [issue](https://github.com/skordaschristofanis/sees-voting-app/issues).
- Add new features, fix bugs or improve documentation by submitting a [pull request](https://github.com/skordaschristofanis/sees-voting-app/pulls).

Please adhere to the [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow) model when making your contributions! This means creating a new branch for each feature or bug fix, and submitting your changes as a pull request against the main branch. If you're not sure how to contribute, please open an issue and we'll be happy to help you out.

By contributing to SEES-Voting-App, you agree that your contributions will be licensed under the MIT License.

[back to top](#table-of-contents)

------------
## License

SEES-Voting-App is distributed under the MIT license. You should have received a [copy](LICENSE) of the MIT License along with this program. If not, see https://mit-license.org/ for additional details.