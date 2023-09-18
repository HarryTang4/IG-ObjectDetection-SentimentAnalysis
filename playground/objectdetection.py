from django.conf import settings
import matplotlib
import json
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import tempfile
from six import BytesIO
from six.moves.urllib.request import urlopen
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps

matplotlib.use('agg')
json_dir = settings.JSON_ROOT
local_dir = settings.STATIC_ROOT + '/media/cached/'

tf.config.set_visible_devices([], "GPU")
tf.device("/cpu:0")


def adjust_image(url, width=320, height=320):
    _, filename = tempfile.mkstemp(suffix=".jpg")
    response = urlopen(url)
    image_data = response.read()
    image_data = BytesIO(image_data)
    image = Image.open(image_data)
    image = ImageOps.fit(image, (width, height), Image.BILINEAR)
    rgb_image = image.convert("RGB")
    rgb_image.save(filename, format="JPEG", quality=100)
    print("Image downloaded to %s." % filename)

    return filename


def draw_bounding_box(
    image, ymin, xmin, ymax, xmax, color, font, thickness=4, display_str_list=()
):
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (
        xmin * im_width,
        xmax * im_width,
        ymin * im_height,
        ymax * im_height,
    )
    draw.line(
        [(left, top), (left, bottom), (right, bottom), (right, top), (left, top)],
        width=thickness,
        fill=color,
    )

    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle(
            [
                (left, text_bottom - text_height - 2 * margin),
                (left + text_width, text_bottom),
            ],
            fill=color,
        )
        draw.text(
            (left + margin, text_bottom - text_height - margin),
            display_str,
            fill="black",
            font=font,
        )
        text_bottom -= text_height - 2 * margin

    return image


def draw_boxes(image, boxes, scores, class_names, max_boxes=5, min_score=0.1):
    colors = list(ImageColor.colormap.values())

    font = ImageFont.load_default()

    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}: {}%".format(
                class_names[i].decode("ascii"), int(100 * scores[i])
            )
            color = colors[hash(class_names[i]) % len(colors)]
            pil_image = Image.fromarray(np.uint8(image)).convert("RGB")
            draw_bounding_box(
                pil_image,
                ymin,
                xmin,
                ymax,
                xmax,
                color,
                font,
                display_str_list=[display_str],
            )
            np.copyto(image, np.array(pil_image))

    return image


def load_image(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=3)
    return image


def run_detection(selected_image):

    image_url = selected_image[0]

    downloaded_image_path = adjust_image(image_url, 328, 328)
    detector = hub.load(
        "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1")
    detector.signatures["default"]
    image = load_image(downloaded_image_path)
    converted_image = tf.image.convert_image_dtype(image, tf.float32)[
        tf.newaxis, ...]

    result = detector(converted_image)

    result = {key: value.numpy() for key, value in result.items()}

    detected_image = draw_boxes(
        image.numpy(),
        result["detection_boxes"],
        result["detection_scores"],
        result["detection_class_entities"],
    )

    return detected_image


def image_to_detect(image_id):

    target_id = str(image_id)
    keyed_media_urls = json.load(open(json_dir + "keyed_media_urls.json"))
    selected_image = [str(keyed_media_urls[target_id][2]), target_id]

    print("Selected image:", (selected_image))

    detected_image = run_detection(selected_image)

    fig = plt.figure(figsize=(5, 5))

    plt.grid(False)
    ax = plt.gca()
    ax.set_adjustable('box')
    plt.axis("off")
    plt.imshow(detected_image)
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)

    fig.savefig(
        "playground/static/media/cached/" + target_id + ".jpg")

    return image_id
