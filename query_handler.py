from query import Query
from irma_code import IRMA


class Handler:

    def __init__(self):
        self._query = Query()
        self._irma = IRMA()
        self.query_image = ''
        self.result_images = []

    def query(self, img_path: str, num_results=10):
        self.result_images = []
        self._image_handler(img_path, num_results)
        self._get_irma()

        return self.result_images

    def _image_handler(self, img_path, num_results):
        self._query.set_image_name(img_path)
        query_results = self._query.run(num_results)

        images_path = '/'.join(query_results[0][0].split('/')[2:-1])+'/'

        for image_path, distance in query_results:
            image_name = self._image_name(image_path)
            self.result_images.append(f'{images_path}/{image_name}')

    def _get_irma(self):
        irma_codes = self._irma.get_irma([self._image_name(x) for x in self.result_images])

        result = []

        for img, irma_code in zip(self.result_images, irma_codes):
            result.append((f'{img}', self._irma.decode_as_str(irma_code)))

        self.result_images = result

    @staticmethod
    def _image_name(img_path: str):
        return img_path.split('/')[-1]

    def ___nonzero__(self):
        return bool(self.query_image)


