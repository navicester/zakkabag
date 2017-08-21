from sae import storage

class SAEBucket(object):
    def __init__(self, bucket_name='media'):
        if not SAEBucket.conn:
            SAEBucket.conn = storage.Connection()
        if not bucket_name:
            bucket_name = 'media'
        self.__bucket = conn.get_bucket(bucket_name)

    def put_object(self, name, content): 
        self.__bucket.put_object(name, content)
        return name

    def url(self, name):  
        return self.__bucket.generate_url(name)     