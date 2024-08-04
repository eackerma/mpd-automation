# mpd-automation
Office automation tools for Metropolitan Public Defender

Currently the only program is a python script automates a paperwork process for Expungement Granted Orders. The automation will:

1. Download all file attachments of unread mail from a given gmail account into a configured folder. (implemented)
2. Process the downloaded files: pdf files that are recognized as expungement grant orders are parsed, extracting the name and case number of the recipient, removing blank pages, renaming the file to the format `[lastname], [firstinitial] - [casenumber] - Granted MOAS.pdf` and moving it into a new folder. Unrecognized files are moved into a different folder.
3. Upload the processed files to Legal Server as a "case note" attached to the case number found in each document.
4. ???
5. Profit

## Installation

1. Get Python 3.12
2. Install project dependencies:

in a terminal, navigate to the project's root directory and run: 

```python
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

```

3. Configure the environment:

Copy the `.env.example` file and rename it to `.env`. Populate the file with values according to your local setup.

4. Acquire the `client_secret.json` file from another developer and store it in the project root.
5. (Developers only) Create a new gmail account for testing purposes. Give the email address to Jordan who will add it as an authorized user of the OAuth app.


### Run the project 

To activate the virtualenv (required) whenever you are running the project, in the root directory run `source ./venv/bin/activate` on Unix machines or `env\Scripts\activate` on Windows.

To run the program, run: `python main.py`

To deactivate the virtualenv, close the terminal or run: `deactivate`
