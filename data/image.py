from PIL import Image


class OCSimpleImage:
    def __init__(self, image=None):

        self.image = image.convert(mode="RGBA") if image else None

    @staticmethod
    def _byte_encode(byte):
        if byte >= 16:
            return hex(byte)[2:]
        else:
            return f"0{hex(byte)[2:]}"

    @staticmethod
    def _byte_decode(byte):
        return int(byte, base=16)

    def serialize(self):
        data_blob = ''.join(f"{OCSimpleImage._byte_encode(r)}{OCSimpleImage._byte_encode(g)}{OCSimpleImage._byte_encode(b)}" for r,g,b,a in self.image.getdata())
        return f"{self.image.width} {data_blob}"

    def deserialize(self, str, scale=1):
        image_width_s, data_blob = str.split()
        image_width = int(image_width_s)
        image_height = (len(data_blob)//6)//image_width

        out_image = Image.new("RGB", (image_width, image_height))

        for pixel_index in range(0, len(data_blob), 6):
            pixel_data = data_blob[pixel_index:pixel_index+6]
            r = OCSimpleImage._byte_decode(pixel_data[:2])
            g = OCSimpleImage._byte_decode(pixel_data[2:4])
            b = OCSimpleImage._byte_decode(pixel_data[4:6])
            pixel_pos = ((pixel_index//6) % image_width, pixel_index//6//image_width)
            out_image.putpixel(pixel_pos, (r,g,b))
        self.image = out_image.resize((out_image.width * scale, out_image.height * scale), resample=Image.NEAREST)
        return self
    def show(self):
        self.image.show()


if __name__ == '__main__':
    x = OCSimpleImage(Image.open(r"C:\Users\dumfi\Downloads\tumblr_bb228b7f65ccf279cc3981a9de65cacd_4fa96106_540.png"))
    serialized = x.serialize()
    y = OCSimpleImage().deserialize(serialized)
    x.show()
    y.show()

