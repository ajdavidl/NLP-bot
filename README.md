# NLP-bot

A chatbot that performs simple nlp tasks.

<!-- ![python](https://img.shields.io/badge/Python-3776AB?style=flat&labelColor=FFD43B&logoColor=3776AB&logo=python) -->
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-3913/)
![Rasa](https://img.shields.io/badge/Rasa-6200F5?style=flat&labelColor=6200F5&logoColor=whitesmoke&logo=Rasa)
![SpaCy](https://img.shields.io/badge/SpaCy-0A84FF?style=flat&labelColor=0A84FF&logoColor=whitesmoke&logo=SpaCy)


## Installing 

Create an python enviroment. Install rasa and other dependencies with following command:

```python
pip install -r requirements.txt
```
After that you may need some SpaCy models to use the parse functionality.

```bash
python -m spacy download en_core_web_sm
python -m spacy download pt_core_news_sm
python -m spacy download es_core_news_sm
python -m spacy download it_core_news_sm
python -m spacy download fr_core_news_sm
```

Clone the repository.

```Shell
git clone https://github.com/ajdavidl/NLP-bot.git
cd NLP-bot
```

### Training Rasa

Open a terminal, and change directory to RasaServer and train the Rasa model.

```Shell
cd RasaServer
rasa train
```

## Getting started

Open three terminals on `NLP-bot` folder and run the shell 
###scripts.

### Run the action server

```Shell
./startRasaActions.sh 
```

### Run the rasa server

```Shell
./startRasaServer.sh 
```

### Run the user interface server

```Shell
./startUI.sh
```
### Open the user interface

Open your browser and access: http://localhost:3838
