# ELG API for spaCy library for Lithuanian

This git repository contains [ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html) Flask based REST API for the spaCy library for the Lithuanian language (v. 3.3.0). [spaCy](https://github.com/explosion/spaCy) is published under MIT license.

[lt_core_news_lg](https://spacy.io/models/lt#lt_core_news_lg) is a large Lithuanian pipeline trained on written web text (blogs, news, comments), that includes vocabulary, syntax and entities. It has a large word vector table with 500000 keys and 500000 unique vectors (300 dimensions). The model was developed based on the following datasets: [UD Lithuanian ALKSNIS v2.8](https://github.com/UniversalDependencies/UD_Lithuanian-ALKSNIS), [TokenMill NER Corpus](https://www.tokenmill.lt/), [Explosion fastText Vectors (cbow, OSCAR Common Crawl + Wikipedia)](https://spacy.io/). The library is published under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company [Explosion](https://explosion.ai/).

You can call two endpoints: `tagger` and `ner`. `tagger` groups tokens by their [pos](https://spacy.io/api/morphologizer) tag and also shows their starting and ending indexes, [lemma](https://spacy.io/api/lemmatizer), [dep](https://spacy.io/api/dependencyparser), [morph](https://spacy.io/api/morphologizer), [tag](https://spacy.io/api/tagger), [head](https://spacy.io/api/dependencyparser). `ner` groups entities (that can contain more than 1 token) by their [label](https://spacy.io/usage/linguistic-features#named-entities) tag and shows their starting and ending indexes.

This ELG API was developed in EU's CEF project [Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry).

## Development

Setup virtualenv, dependencies

```
python -m venv spacy-lt-elg-venv
source spacy-lt-elg-venv/bin/activate
python -m pip install -r requirements.txt
```

Install spaCy and the large Lithuanian model.

```
pip install -U spacy
python -m spacy download lt_core_news_lg
```

Run the development mode flask app

```
FLASK_ENV=development flask run --host 0.0.0.0 --port 8000
```

Tests

```
python -m unittest tests/test_integration.py -v
```


## Building the docker image

```
docker build -t spacy-lt .
```

Or pull directly ready-made image `docker pull lingsoft/spacy-lt:3.3.0-elg`.

## Deploying the service

```
docker run -d -p <port>:8000 --init spacy-lt
```

## Example call

```
curl -X POST -H 'Content-Type: application/json' http://localhost:8000/process/<endpoint> -d '{"type":"text","content":"Filipas gyvena Vilniuje."}'
```

`endpoint` can be `tagger` or `ner`. 

### Response

Tagger

```json
{
  "response": {
    "type": "annotations",
    "annotations": {
      "PROPN": [
        {
          "start": 0,
          "end": 7,
          "features": {
            "lemma": "Filipas",
            "dep": "nsubj",
            "morph": "Case=Nom|Gender=Masc|Number=Sing",
            "tag": "dkt.tikr.vyr.vns.V.",
            "head": "gyvena"
          }
        },
        {
          "start": 15,
          "end": 23,
          "features": {
            "lemma": "Vilnius",
            "dep": "obl",
            "morph": "Case=Loc|Gender=Masc|Number=Sing",
            "tag": "dkt.tikr.vyr.vns.Vt.",
            "head": "gyvena"
          }
        }
      ],
      "VERB": [
        {
          "start": 8,
          "end": 14,
          "features": {
            "lemma": "gyventi",
            "dep": "ROOT",
            "morph": "Mood=Ind|Number=Sing|Person=3|Polarity=Pos|Tense=Pres|VerbForm=Fin",
            "tag": "vksm.asm.tiesiog.es.vns.3.",
            "head": "gyvena"
          }
        }
      ],
      "PUNCT": [
        {
          "start": 23,
          "end": 24,
          "features": {
            "lemma": ".",
            "dep": "punct",
            "morph": "",
            "tag": "skyr.",
            "head": "gyvena"
          }
        }
      ]
    }
  }
}
```

NER

```json
{
  "response": {
    "type": "annotations",
    "annotations": {
      "PERSON": [
        {
          "start": 0,
          "end": 7
        }
      ],
      "LOC": [
        {
          "start": 15,
          "end": 23
        }
      ]
    }
  }
}

```

### Response structure

Tagger
- `start` and `end` (int)
  - indices of the token in the request
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
