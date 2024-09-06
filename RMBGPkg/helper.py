import torch
from PIL import Image
from numpy import ndarray
from huggingface_hub import hf_hub_download

from RMBGPkg.briarmbg import BriaRMBG
from RMBGPkg.utilities import preprocess_image, postprocess_image


class Remover:

    __model = None
    __device = None
    def __init__(self, model = BriaRMBG.from_pretrained("briaai/RMBG-1.4")):
        self.__model = model
        to_device = "cuda" if torch.cuda.is_available() else "cpu"
        self.__device = torch.device(to_device)
        self.__model.to(self.__device)
        self.__model.eval()

    def remove_background_for(self, orig_im: ndarray) -> Image:
        # prepare input
        model_input_size = [1024, 1024]
        orig_im_size: tuple[int, ...] = orig_im.shape[0:2]
        image = preprocess_image(orig_im, model_input_size).to(self.__device)
        # inference
        result = self.__model(image)

        # post process
        result_image = postprocess_image(result[0][0], list(orig_im_size))

        # save result
        pil_im = Image.fromarray(result_image)
        no_bg_image = Image.new("RGBA", pil_im.size, (0,0,0,0))
        orig_image = Image.fromarray(orig_im)
        no_bg_image.paste(orig_image, mask=pil_im)
        return no_bg_image