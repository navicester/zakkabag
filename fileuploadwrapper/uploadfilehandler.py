from django.core.files.uploadhandler import FileUploadHandler
from django.core.cache import cache
import time

#https://docs.djangoproject.com/en/1.8/ref/files/uploads/#django.core.files.uploadhandler.FileUploadHandler

class UploadProgressCachedHandler(FileUploadHandler):
    """
    Tracks progress for file uploads.
    The http post request must contain a header or query parameter, we gonna use
    CSRF token generated by GET request for form in the view but you can modified
    according your considerations or parameters.

    For more info, redirect to documentation: https://docs.djangoproject.com/en/1.7/ref/files/uploads/#optional-methods
    """

    def __init__(self, request=None):
        super(UploadProgressCachedHandler, self).__init__(request)
        self.progress_id = None
        self.cache_key = None


    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):

        self.content_length = content_length
        if 'CSRF_COOKIE' in self.request.GET:
            self.cache_key = self.request.GET['CSRF_COOKIE']
        elif 'CSRF_COOKIE' in self.request.META:
            self.cache_key = self.request.META['CSRF_COOKIE']

        if self.cache_key:
            cache.set(self.cache_key, {
                'totalsize': self.content_length,
                'uploaded': 0
            })
            print "UploadProgressCachedHandler:handle_raw_input cache_key %s" % self.cache_key
        else:
            # pass
            print "UploadProgressCachedHandler:handle_raw_input cache_key not set, content_length = %d" % content_length

    def new_file(self, field_name, file_name, content_type, content_length, charset=None, content_type_extra=None):
        pass

    def receive_data_chunk(self, raw_data, start):
        if self.cache_key:
            data = cache.get(self.cache_key)
            data['uploaded'] += self.chunk_size
            cache.set(self.cache_key, data)
        return raw_data
    
    def file_complete(self, file_size):
        """
        Called when a file has finished uploading.

        The handler should return an UploadedFile object that will be stored in request.FILES. 
        Handlers may also return None to indicate that the UploadedFile object should come from subsequent upload handlers.
        """
        if self.cache_key:
            data = cache.get(self.cache_key)
            data['uploaded'] = self.content_length
            cache.set(self.cache_key, data)
            time.sleep(2) # sleep for give time to receive final response in request progress bar


    def upload_complete(self):
        """
        Callback signaling that the entire upload (all files) has completed.
        """
        if self.cache_key:            
            cache.delete(self.cache_key)  # hebinn
        # print "UploadProgressCachedHandler:upload_complete"
