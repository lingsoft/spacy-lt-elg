from elg import FlaskService
from elg.model import TextRequest, AnnotationsResponse, Failure
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
                pos  = token.pos_
                if pos != "SPACE":
                    word = token.text
                    lemma = token.lemma_
                    dep  = token.dep_
                    morph = token.morph
                    tag = token.tag_
                    head = token.head

                    start = content.find(word) + offset
                    end = start + len(word)
                    content = content[end - offset :]
                    offset = end
                    annot = {
                        "start": start,
                        "end": end,
                        "features": {
                            "lemma": str(lemma),
                            "dep": str(dep),
                            "morph": str(morph),
                            "tag": str(tag),
                            "head": str(head)
                            }
                        }
                    annotations.setdefault(pos, []).append(annot)
        elif endpoint == "ner":
            for ent in outputs.ents:
                text = ent.text
                start = ent.start_char
                end  = ent.end_char
                label  = ent.label_
                annot = {
                    "start": start,
                    "end": end,
                }
                annotations.setdefault(label, []).append(annot)
        return AnnotationsResponse(annotations=annotations)

    def process_text(self, request: TextRequest):
        try:
            content = request.content
            outputs = self.nlp(content)
            return self.convert_outputs(outputs, content)
        except Exception as err:
            error = StandardMessages.\
                    generate_elg_service_internalerror(params=[str(err)])
            return Failure(errors=[error])


flask_service = SpaCyLt(name="spaCyLt", path="/process/<endpoint>")
app = flask_service.app
