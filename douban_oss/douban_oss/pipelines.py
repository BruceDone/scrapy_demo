# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from PIL import Image
import oss2

from scrapy.http.request import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import NotConfigured, DropItem
from scrapy.pipelines.files import FileException
from scrapy.log import logger


class ImageException(FileException):
    """General image error exception"""


class AliOssStore(object):
    def __init__(self, host_base, access_key_id, access_key_secret, bucket_name):
        """
        auto define the store object
        for more detail please refer
        https://github.com/scrapy/scrapy/blob/0ede017d2ac057b1c3f9fb77a875e4d083e65401/scrapy/pipelines/files.py
        :param host_base: 
        :param access_key_id: 
        :param access_key_secret: 
        :param bucket_name:
        """
        self._auth = oss2.Auth(access_key_id, access_key_secret)
        self._bucket = oss2.Bucket(self._auth, host_base, bucket_name)

    def stat_file(self, path, info):
        # always return the empty result ,force the media request to download the file
        return {}

    def _check_file(self, path):
        if not os.path.exists(path):
            return False

        return True

    def persist_file(self, path, buf, info, meta=None, headers=None):
        """Upload file to Ali oss storage"""
        self._upload_file(path, buf)

    def _upload_file(self, path, buf):
        logger.warning('now i will upload the image {}'.format(path))
        self._bucket.put_object(key=path, data=buf.getvalue())


class DoubanOssStorePipeline(ImagesPipeline):
    MEDIA_NAME = 'image'

    # Uppercase attributes kept for backward compatibility with code that subclasses
    # ImagesPipeline. They may be overridden by settings.
    MIN_WIDTH = 0
    MIN_HEIGHT = 0

    DEFAULT_IMAGES_RESULT_FIELD = 'images'

    def __init__(self, ali_oss_config):
        self.ali_oss_config = ali_oss_config
        self.folder = ali_oss_config.get('folder', '')
        super(DoubanOssStorePipeline, self).__init__(ali_oss_config)

    def _get_store(self, uri):
        # get the ali oss store object
        return AliOssStore(
            self.ali_oss_config['host_base'],
            self.ali_oss_config['access_key_id'],
            self.ali_oss_config['access_key_secret'],
            self.ali_oss_config['bucket_name'],
        )

    def get_media_requests(self, item, info):
        if not item.get('url'):
            raise DropItem('item not find any url:{}'.format(json.dumps(item)))

        yield Request(url=item.get('url'))

    def get_images(self, response, request, info):
        path = self.file_path(request, response=response, info=info)
        orig_image = Image.open(BytesIO(response.body))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.min_width, self.min_height))

        image, buf = self.convert_image(orig_image)
        yield path, image, buf

    def file_path(self, request, response=None, info=None):
        img_path = super(DoubanOssStorePipeline, self).file_path(request, response, info)
        # the image path will like this full/abc.jpg ,we just need the image name
        image_name = img_path.rsplit('/', 1)[-1] if '/' in img_path else img_path
        if self.folder:
            image_name = os.path.join(self.folder, image_name)

        return image_name

    @classmethod
    def from_settings(cls, settings):

        ali_oss_config = settings.getdict('ALI_OSS_CONFIG', {})
        if not ali_oss_config:
            raise NotConfigured('You should config the ali_oss_config to enable this pipeline')

        return cls(ali_oss_config)
