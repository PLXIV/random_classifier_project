import os
import sys
sys.path.insert(0, "/code/")

import pytest
import torch

from app_classifier.model import MyClassifier


images_list = ['images/single_channel.jpg', 'images/chairs-2.png', 'images/chairs.jpg', 'images/abstract.jpg',
               'images/coffee-1.jpg', 'images/coffee-2.jpg', 'images/hd-wallpaper.jpg', 'images/living-room.jpg',
               'images/white-wine.jpg']

@pytest.mark.parametrize("mode, model_path", [('script', os.environ['MODEL_PATH']),
                                              ('eager', os.environ['MODEL_PATH_EAGER']),
                                              pytest.param('script', os.environ['MODEL_PATH_EAGER'],
                                                           marks=pytest.mark.xfail),
                                              pytest.param('eager', os.environ['MODEL_PATH'],
                                                           marks=pytest.mark.xfail)
                                              ])
def test_load_model_script(mode, model_path) -> None:
    classifier = MyClassifier(model_path, mode=mode)
    assert classifier


@pytest.mark.parametrize("image", images_list)
def test_preprocessing(image, load_sample, classifier) -> None:
    img = load_sample(image)
    tensor = classifier.preprocess(img)
    assert type(tensor) == torch.Tensor
    assert tensor.numpy().shape == (3, 224, 224)


@pytest.mark.parametrize("image", images_list)
def test_forward(image, load_sample, classifier) -> None:
    img = load_sample(image)
    inference = classifier(img)
    print(inference.argmax().item())
    assert inference.detach().numpy().shape[0] == 1000


@pytest.mark.parametrize("image, label", [('images/living-room.jpg', 532), ('images/white-wine.jpg', 572), ('images/hd-wallpaper.jpg', 696)])
def test_forward_results(image, label, load_sample, classifier) -> None:
    img = load_sample(image)
    inference = classifier(img)
    inference_label_id = inference.argmax().item()
    assert label == inference_label_id



