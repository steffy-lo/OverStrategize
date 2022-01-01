import cv2
import tensorflow as tf
import pathlib
from pynput.keyboard import Listener
import time

import overlay
import config
import utils
import algorithm

# creating a tensorflow session (we will be using this to make our predictions later)
session = tf.compat.v1.Session(graph=tf.Graph())

# loading the model into our session created above
tf.compat.v1.saved_model.loader.load(session, ['serve'], config.model_path)


def predict(img_bytes):
    # pass the image as input to the ML model and get the result
    result = session.run(['detection_boxes:0', 'detection_multiclass_scores:0', 'detection_classes:0'], feed_dict={
        'encoded_image_string_tensor:0': [img_bytes]})

    boxes = result[0][0]
    scores = result[1][0]
    classes = result[2][0]

    final_predictions = []

    for i in range(len(scores)):
        for j in range(len(scores[i])):
            # only consider a detected object if it's probability is above 25%
            if scores[i][j] > 0.2:
                label = config.labels[classes[i]]
                # print("The box {} has probability {} of being {}".format(boxes[i], scores[i][j], label))

                found_same_box = False
                k = 0
                for data in final_predictions:
                    if utils.same_box(data["box"], boxes[i]):
                        found_same_box = True
                        if data["score"] < scores[i][j]:
                            final_predictions.pop(k)
                            final_predictions.append({"box": boxes[i], "score": scores[i][j], "label": label})
                    k += 1

                if not found_same_box:
                    final_predictions.append({"box": boxes[i], "score": scores[i][j], "label": label})

    return final_predictions


def test():
    for file in pathlib.Path(config.image_path).iterdir():
        # get the current image path
        current_image_path = r"{}".format(file.resolve())

        # image bytes since this is what the ML model needs as its input
        img_bytes = open(current_image_path, 'rb').read()

        # pass the image as input to the ML model and get the result
        predictions = predict(img_bytes)

        # read the image with opencv
        img = cv2.imread(current_image_path)

        # get the width and height of the image
        imH, imW, _ = img.shape

        print("For image {}".format(file.stem))

        heroes = {
            "ally": [],
            "enemy": []
        }

        for pred in predictions:
            hero_type = "ally" if int(max(1, (pred["box"][0] * imH))) > imH * 0.35 else "enemy"
            heroes[hero_type].append(pred["label"])
            print("The box {} has probability {} of being {}".format(pred["box"], pred["score"], pred["label"]))
            utils.draw_boxes(imH, imW, pred["box"], img, pred["label"])

        ally_hero_scores, enemy_hero_scores = algorithm.hero_scores(heroes["ally"], heroes["enemy"], "All")

        for pred in predictions:
            hero_score_map = ally_hero_scores if int(max(1, (pred["box"][0] * imH))) > pred["box"][0] * imH * 0.55 else enemy_hero_scores
            utils.draw_hero_scores(imH, imW, pred["box"], img, hero_score_map[pred["label"]])

        recommendations = algorithm.hero_recommendation_ver_b(ally_hero_scores, heroes["ally"], heroes["enemy"])
        ally_total_score, enemy_total_score = algorithm.team_scores(ally_hero_scores, heroes["ally"], enemy_hero_scores, heroes["enemy"])
        utils.draw_overall_test_results_ver_b(imH, imW, img, ally_total_score, enemy_total_score, recommendations)

        # resize the image to fit the screen
        new_img = cv2.resize(img, (1920, 1080))
        # show the image on the screen
        cv2.imshow("image", new_img)
        # as soon as any key is pressed, skip to the next line
        cv2.waitKey(0)

# ======================================== MAIN PROGRAM ===============================================================


capture = True


def show_overlay():
    with overlay.FullScreenOverlay() as fs_overlay:
        img_bytes = open("capture.jpg", 'rb').read()
        predictions = predict(img_bytes)
        while fs_overlay.loop:
            heroes = {
                "ally": [],
                "enemy": []
            }
            # read the image with opencv
            img = cv2.imread("capture.jpg")

            # get the width and height of the image
            img_height, img_width, _ = img.shape
            for pred in predictions:
                box = pred["box"]
                label = pred["label"]

                # starting coordinates of the box
                ymin = int(max(1, (box[0] * img_height)))
                xmin = int(max(1, (box[1] * img_width)))

                # last coordinates of the box
                ymax = int(min(img_height, (box[2] * img_height)))
                xmax = int(min(img_width, (box[3] * img_width)))

                hero_type = "ally" if int(max(1, (pred["box"][0] * img_height))) > img_height * 0.35 else "enemy"
                heroes[hero_type].append(label)

                overlay.Draw.outline(xmin, img_height - ymin, xmax - xmin, ymin - ymax, 2.5, overlay.Draw.green)
                overlay.Draw.text(xmin, img_height - ymin + 10, overlay.Draw.green, label)

            ally_hero_scores, enemy_hero_scores = algorithm.hero_scores(heroes["ally"], heroes["enemy"], "All")

            for pred in predictions:
                hero_score_map = ally_hero_scores if int(max(1, (pred["box"][0] * img_height))) > img_height * 0.35 else enemy_hero_scores
                box = pred["box"]
                label = pred["label"]
                ymax = int(min(img_height, (box[2] * img_height)))
                xmin = int(max(1, (box[1] * img_width)))
                score_label = str(hero_score_map[label])
                overlay.Draw.text(xmin, img_height - ymax - 25, overlay.Draw.green, score_label)

            recommendations = algorithm.hero_recommendation_ver_b(ally_hero_scores, heroes["ally"], heroes["enemy"])
            ally_total_score, enemy_total_score = algorithm.team_scores(ally_hero_scores, heroes["ally"],
                                                                        enemy_hero_scores, heroes["enemy"])

            utils.draw_results_to_overlay(img_height, img_width, ally_total_score, enemy_total_score, recommendations)
            fs_overlay.update()
    global capture
    capture = True


def run():
    # Program listens and runs on Tab Press
    def on_press(key):
        global capture
        if str(key) == "Key.tab" and capture:
            capture = False
            show_overlay()

    with Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    capture = True
    DEBUG = False
    if DEBUG:
        test()
    else:
        run()
