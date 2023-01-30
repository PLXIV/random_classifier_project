from os.path import exists
from typing import List

import torch
from torchvision.models import resnet101
from torchvision.models.resnet import ResNet
from torchvision import transforms
from PIL.Image import Image


class MyClassifier(torch.nn.Module):

    def __init__(self, model_path: str, mode='script'):
        """
        Base models in which the microservices are going be based on. It requires a file in which can be .pth or .pt.
        It allows to run on eager or script mode. On script mode, if we want to run it on GPU, the models may need to be
        saved with the cuda settings beforehand.

        :param model_path: String that indicates the path where the models is stored.
        :param mode: Mode in which the network will be loaded. In can have the values eager or script. For more
        info please visit (https://pytorch.org/tutorials/beginner/Intro_to_TorchScript_tutorial.html).
        """
        super(MyClassifier, self).__init__()
        assert(exists(model_path))

        self.cuda = False
        if torch.cuda.is_available():
            self.cuda = True

        self.model_path = model_path
        self._model = self._load_model(mode)
        self._preprocess = self._preprocess_scheme()
        self.labels = self._read_labels()

    def _load_model(self, mode: str) -> ResNet:
        """
        Loads models from the file contained in model_path. It can load models in eager or script mode. It would be
        reasonable to talk with the AI team and talk if it makes sense to can always convert the models into
         script mode before uploading to production.

        :param mode: load models in eager or script mode. Notice that the script does not convert the models into cuda
        if not done previously when the models was saved.
        :return Pytorch models with loaded weights.
        """
        assert(mode in ['eager', 'script'])
        if mode == 'eager':
            model = resnet101()
            model.load_state_dict(torch.load(self._model_path))
            model.eval()
            if self.cuda:
                model.to('cuda')
        else:
            model = torch.jit.load(self._model_path)
        return model

    @staticmethod
    def _preprocess_scheme() -> transforms.Compose:
        """
        Performs transformations to the image required to run through the network.

        :return: Transformed image ready to go through the forward step of the network.
        """
        return transforms.Compose([
            transforms.Resize(232),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def _read_labels(self) -> List:
        """
        Reads label names.
        :return: List of label names relative to the classifier IDs
        """
        return self._model.imagenet_categories

    def forward(self, img: Image) -> torch.TensorType:
        """
        Forward pass of samples. Performs the inference. Transforms and preprocesses the input image then predicts
        the class.

        :param img: 3 dimensional Image.
        :return: tensor with the result of the inference.
        """
        input_tensor = self._preprocess(img)
        input_batch = input_tensor.unsqueeze(0)
        if self.cuda:
            input_batch = input_batch.to('cuda')
        return self._model(input_batch).squeeze(0).softmax(0)
