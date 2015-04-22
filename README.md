# benchmarks
A playground to test the bluemix services.

## Requirements
* nltk>=3.0.0
* mplayer (for speech synthesis)
* stanford ner-tagger

### Run this to install the ner-tagger:
```
echo "Downloading stanford-ner-tagger ..."
wget http://nlp.stanford.edu/software/stanford-ner-2014-08-27.zip

echo "Unzip folders ..."
unzip stanford-ner-2014-08-27.zip

echo "Rename folders ..."
mv stanford-ner-2014-08-27 stanford-ner

echo "Removing zip files ..."
rm stanford-ner-2014-08-27.zip
```
