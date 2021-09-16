import re
from sumeval.metrics.lang.base_lang import BaseLang


class LangJA(BaseLang):

    def __init__(self):
        super(LangJA, self).__init__("ja")
        self._set_tokenizer()
        self._symbol_replace = re.compile(r"[^ぁ-んァ-ン一-龥ーa-zA-Zａ-ｚＡ-Ｚ0-9０-９]")

    def load_parser(self):
        if self._PARSER is None:
            import spacy
            self._PARSER = spacy.load("ja_ginza")
        return self._PARSER

    def _set_tokenizer(self):
        try:
            import MeCab
            import ipadic

            # https://gist.github.com/polm/b305d500df28f190e346d50447682ec6
            # -Ochasen の出力フォーマットを直接指定する
            CHASEN_ARGS = r' -F "%m\t%f[7]\t%f[6]\t%F-[0,1,2,3]\t%f[4]\t%f[5]\n"'
            CHASEN_ARGS += r' -U "%m\t%m\t%m\t%F-[0,1,2,3]\t\t\n"'

            class Tokenizer():

                def __init__(self):
                    #self.tagger = MeCab.Tagger("-Ochasen")
                    self.tagger = MeCab.Tagger(ipadic.MECAB_ARGS + CHASEN_ARGS)

                def tokenize(self, text):
                    self.tagger.parse("")
                    node = self.tagger.parseToNode(text)
                    tokens = []
                    while node:
                        if node.surface:
                            tokens.append(node)
                        node = node.next
                    return tokens

            self.tokenizer = Tokenizer()

        except Exception as ex:
            from janome.tokenizer import Tokenizer
            self.tokenizer = Tokenizer()

    def tokenize(self, text):
        words = [t.surface for t in self.tokenizer.tokenize(text)]
        return words

    def tokenize_with_preprocess(self, text):
        _text = self._symbol_replace.sub(" ", text)
        words = self.tokenize(_text)
        words = [w.strip() for w in words if w.strip()]
        return words

    def join(self, words):
        return "".join(words)

    def parse_to_be(self, text):
        _text = self._symbol_replace.sub(" ", text)
        bes = super().parse_to_be(_text)
        return bes
