from elg import FlaskService
from elg.model import AnnotationsResponse
from elg.model import Failure, TextRequest
from elg.model.base import StandardMessages
import spacy

class SpaCyLt(FlaskService):

    nlp = spacy.load("lt_core_news_lg")

    def convert_outputs(self, outputs, content):
        endpoint = self.url_param('endpoint')
        annotations = {}
        offset = 0
        if endpoint == "tagger":
            for token in outputs:
                word = token.text
                lemma = token.lemma_
                pos  = token.pos_
                dep  = token.dep_
                morph = token.morph
                tag = token.tag_
                head = token.head

                start = content.find(word) + offset
                end = start + len(word)
                content = content[end - offset :]
                offset = end
                if pos not in annotations.keys():
                    annotations[pos] = [
                        {
                            "start": start,
                            "end": end,
                            "features": {
                                "word": str(word),
                                "lemma": str(lemma),
                                "dep": str(dep),
                                "morph": str(morph),
                                "tag": str(tag),
                                "head": str(head)
                            },
                        }
                    ]
                else:
                    annotations[pos].append(
                        {
                            "start": start,
                            "end": end,
                            "features": {
                                "word": str(word),
                                "lemma": str(lemma),
                                "dep": str(dep),
                                "morph": str(morph),
                                "tag": str(tag),
                                "head": str(head)
                            },
                        }
                    )
        elif endpoint == "ner":
            for ent in outputs.ents:
                text = ent.text
                start = ent.start_char
                end  = ent.end_char
                label  = ent.label_
                if label not in annotations.keys():
                    annotations[label] = [
                        {
                            "start": start,
                            "end": end,
                            "features": {
                                "text": str(text)
                            },
                        }
                    ]
                else:
                    annotations[label].append(
                        {
                            "start": start,
                            "end": end,
                            "features": {
                                "text": str(text)
                            },
                        }
                    )
        return AnnotationsResponse(annotations=annotations)

    def process_text(self, content):
        outputs = self.nlp(content.content)
        return self.convert_outputs(outputs, content.content)

flask_service = SpaCyLt(name="spaCyLt", path="/process/<endpoint>")
app = flask_service.app
