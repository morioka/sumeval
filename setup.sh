# python 3.9.7

pip install --upgrade pip

pip install mecab-python3 ipadic
if [ ! -d /usr/share/mecab ]; then
  sudo apt install mecab libmecab-dev git make curl xz-utils file
  git clone --depth 1 https://github.com/neologd/mecab-unidic-neologd.git
  echo yes | mecab-unidic-neologd/bin/install-mecab-unidic-neologd -n
fi

pip install spacy ja-ginza ja-ginza-electra

pip install -r requirements-test.txt

#git clone https://github.com/morioka/sumeval.git
pip install --editable .

python -m spacy download en_core_web_sm
