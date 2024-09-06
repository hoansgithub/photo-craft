import os

from skimage import io
from  helper import *

def example_inference():

    im_path = f"{os.path.dirname(os.path.abspath(__file__))}/sample_png.png"
    org_image = io.imread(im_path)
    remover = Remover()
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #net = BriaRMBG.from_pretrained("briaai/RMBGPkg-1.4")
    #net.to(device)
    #net.eval()

    # prepare input
    #model_input_size = [1024,1024]
    #orig_im = io.imread(im_path)
    #orig_im_size = orig_im.shape[0:2]
    #image = preprocess_image(orig_im, model_input_size).to(device)

    # inference 
    no_bg_image=remover.remove_background_for(org_image)
    #orig_im_size = org_image.shape[0:2]
    # post process
    #result_image = postprocess_image(result[0][0], orig_im_size)

    # save result
    #pil_im = Image.fromarray(result_image)
    #no_bg_image = Image.new("RGBA", pil_im.size, (0,0,0,0))
    #orig_image = Image.open(im_path)
    #no_bg_image.paste(orig_image, mask=pil_im)
    no_bg_image.save("example_image_no_bg.png")


if __name__ == "__main__":
    example_inference()