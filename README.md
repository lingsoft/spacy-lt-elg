# ELG API for spaCy library for Lithuanian

This git repository contains [ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html) Flask based REST API for the spaCy library for the Lithuanian language (v. 3.3.0).

[lt_core_news_lg](https://spacy.io/models/lt#lt_core_news_lg) is a large Lithuanian pipeline trained on written web text (blogs, news, comments), that includes vocabulary, syntax and entities. It has a large word vector table with 500000 keys and 500000 unique vectors (300 dimensions). The model was developed based on the following datasets: [UD Lithuanian ALKSNIS v2.8](https://github.com/UniversalDependencies/UD_Lithuanian-ALKSNIS), [TokenMill NER Corpus](https://www.tokenmill.lt/), [Explosion fastText Vectors (cbow, OSCAR Common Crawl + Wikipedia)](https://spacy.io/). The library is published under the MIT license and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company [Explosion](https://explosion.ai/).


This ELG API was developed in EU's CEF project: [Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry)

## Local development

Setup virtualenv, dependencies
```
python3 -m venv nb-ner-elg-venv
source nb-ner-elg-venv/bin/activate
python3 -m pip install -r requirements.txt
```

Install spaCy and the large Lithanian model.

```
pip install -U spacy
python -m spacy download lt_core_news_lg
```

Run the development mode flask app
```
FLASK_ENV=development flask run --host 0.0.0.0 --port 8000
```

## Building the docker image

```
docker build -t spacy-lt .
```

Or pull directly ready-made image `docker pull lingsoft/spacy-lt:tagname`.

## Deploying the service

```
docker run -d -p <port>:8000 --init --memory="2g" --restart always spacy-lt
```

## REST API

### Call pattern
