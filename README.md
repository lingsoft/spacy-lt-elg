# ELG API for spaCy library for Lithuanian

This git repository contains [ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html) Flask based REST API for the spaCy library for the Lithuanian language (v. 3.3.0).

[lt_core_news_lg](https://spacy.io/models/lt#lt_core_news_lg) is a large Lithuanian pipeline trained on written web text (blogs, news, comments), that includes vocabulary, syntax and entities. It has a large word vector table with 500000 keys and 500000 unique vectors (300 dimensions). The model was developed based on the following datasets: [UD Lithuanian ALKSNIS v2.8](https://github.com/UniversalDependencies/UD_Lithuanian-ALKSNIS), [TokenMill NER Corpus](https://www.tokenmill.lt/), [Explosion fastText Vectors (cbow, OSCAR Common Crawl + Wikipedia)](https://spacy.io/). The library is published under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company [Explosion](https://explosion.ai/).

You can call two endpoints: `tagger` and `ner`. `tagger` groups tokens by their [pos](https://spacy.io/api/morphologizer) tag and also shows their starting and ending indexes, [lemma](https://spacy.io/api/lemmatizer), [dep](https://spacy.io/api/dependencyparser), [morph](https://spacy.io/api/morphologizer), [tag](https://spacy.io/api/tagger), [head](https://spacy.io/api/dependencyparser). `ner` groups entities (that can contain more than 1 token) by their [label](https://spacy.io/usage/linguistic-features#named-entities) tag and shows their starting and ending indexes.

This ELG API was developed in EU's CEF project: [Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry)

## Local development

Setup virtualenv, dependencies
```
python -m venv spacy-lt-elg-venv
source spacy-lt-elg-venv/bin/activate
python -m pip install -r requirements.txt
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
docker build -t spacy-lt-elg .
```

Or pull directly ready-made image `docker pull lingsoft/spacy-lt-elg:3.3.0-elg`.

## Deploying the service

```
docker run -d -p <port>:8000 --init --memory="2g" --restart always spacy-lt-elg
```

## Example call

```
curl -H "Content-Type: application/json" -d @text-request.json -X POST http://localhost:<port>/process/<endpoint_name>
```
`endpoint_name` can be `tagger` or `ner`. 


### Text request

```
{
    "type": "text",
    "content": text to be analyzed
}
```

### Response

Tagger

```
{
  "response": {
    "type": "annotations",
    "annotations": {
      "<POS tag>": [ // list of tokens that were recognized
        {
          "start":number,
          "end":number,
          "features": {"word": str, "lemma": str, "dep": str, "morph": str, "tag": str, "head": str}
        },
      ],
    }
  }
}
```

NER

```
{
  "response": {
    "type": "annotations",
    "annotations": {
      "<NER label>": [ // list of entities that were recognized
        {
          "start":number,
          "end":number,
          "features": {"text": str}
        },
      ],
    }
  }
}
```

### Response structure

Tagger
- `start` and `end` (int)
  - indices of the token in the request
- `word` (str)
  - recognized word
- [pos](https://spacy.io/api/morphologizer)
  - UPOS part of speech
- [lemma](https://spacy.io/api/lemmatizer)
  - lemma (dictionary form)
- [dep](https://spacy.io/api/dependencyparser)
  - type of dependency relation
- [morph](https://spacy.io/api/morphologizer)
  - morphological features
- [tag](https://spacy.io/api/tagger)
  - part of speech
- [head](https://spacy.io/api/dependencyparser)
  - syntactic parent, or “governor”, of this token

 [label](https://spacy.io/usage/linguistic-features#named-entities) tag and shows their starting and ending indexes.

NER
- `start` and `end` (int)
  - indices of the entity in the request
- [label](https://spacy.io/usage/linguistic-features#named-entities)
  - NER label
- `text` (str)
  - recognized entity
