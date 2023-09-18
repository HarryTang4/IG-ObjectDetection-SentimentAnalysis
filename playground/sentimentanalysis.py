
from django.conf import settings
import json
import os
import shutil
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
json_dir = settings.JSON_ROOT


def comments_to_analyze(image_id):

    folder = "cardiffnlp"
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
        except BaseException:
            print(BaseException)

    with open(json_dir + "is_keyed_comments.json") as file:
        is_keyed_comments = json.load(file)

    image_id = str(image_id)

    comment_sentiments = {}

    if image_id not in is_keyed_comments.keys():
        return {}

    MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    model.save_pretrained(MODEL)

    sentiments = []
    comments = is_keyed_comments[image_id]
    for comment in comments:
        sentiments.append(
            get_sentiment(comment, model, tokenizer, config))

    for i, comment in enumerate(comments):
        comment_sentiments[comment] = {'positive': sentiments[i][1],
                                       'neutral': sentiments[i][3],
                                       'negative': sentiments[i][5]}
    return comment_sentiments


def get_sentiment(photo_comment, model, tokenizer, config):

    sentiment = []
    encoded_input = tokenizer(photo_comment, return_tensors="pt")
    output = model(**encoded_input)
    scores = softmax(output[0][0].detach().numpy())
    rankings = np.argsort(scores)[::-1]

    for i in range(scores.shape[0]):
        labels = config.id2label[rankings[i]]
        results = scores[rankings[i]]
        results = np.round(float(results), 4)
        sentiment.extend([labels, results])

    return sentiment

# sentiment_dict = dict(zip(is_keyed_comments.keys(), sentiments)) -> total scores of sentiment per post
