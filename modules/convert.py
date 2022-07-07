from PIL import Image


def execute(image_path: str, to_format: str = "png", width: int = None, height: int = None):
    try:
        print("Opening image...")
        result_kwargs = {}
        try:
            img = Image.open(image_path)
        except:
            print("Unable to open image")
            return
        if width and height:
            img = img.resize((width, height))
        elif width:
            img = img.resize((width, img.size[1]))
        elif height:
            img = img.resize((img.size[0], height))

        new_image_path = ".".join(image_path.split(".")[:-1]) + "." + to_format

        if to_format == "jpeg":
            img = img.convert("RGB")
        elif to_format == "ico":
            result_kwargs["sizes"] = []
            for size in [128, 256]:
                result_kwargs["sizes"].append((size, size))

        img.save(new_image_path, format=to_format, **result_kwargs)
        print("Image converted")
    except Exception as e:
        print("An error occurred while converting image")
        print("Error", e)