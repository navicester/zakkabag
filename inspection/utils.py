import os
from django.core.files.storage import default_storage
from django.db.models import FileField
from django.core.cache import cache

def file_cleanup(sender, **kwargs):
    """
    File cleanup callback used to emulate the old delete
    behavior using signals. Initially django deleted linked
    files when an object containing a File/ImageField was deleted.

    Usage:
    >>> from django.db.models.signals import post_delete
    >>> post_delete.connect(file_cleanup, sender=MyModel, dispatch_uid="mymodel.file_cleanup")
    """
    for fieldname in sender._meta.get_all_field_names():
        try:
            field = sender._meta.get_field(fieldname)
        except:
            field = None
        if field and isinstance(field, FileField):
            inst = kwargs['instance']
            f = getattr(inst, fieldname)
            m = inst.__class__._default_manager
            if hasattr(f, 'path') and os.path.exists(f.path)\
            and not m.filter(**{'%s__exact' % fieldname: getattr(inst, fieldname)})\
            .exclude(pk=inst._get_pk_val()):
                try:
                    if 'SERVER_SOFTWARE' in os.environ: 
                        from sae import storage
                        from saewrapper.storage.bucket import SAEBucket
                        raise RuntimeError('env setup' % f.path)
                        SAEBucket().delete(f.path)
                    else:
                        default_storage.delete(f.path)
                except:
                    pass

def file_cleanup2(sender, **kwargs):
    inst = kwargs['instance']
    cache_key = ("%s %d") % (inst.__class__.__name__ , inst._get_pk_val())
    inst_raw = cache.get(cache_key)

    if 'SERVER_SOFTWARE' in os.environ: 
        from sae import storage
        from saewrapper.storage.bucket import SAEBucket
        pass

    for fieldname in sender._meta.get_all_field_names():
        try:
            field = sender._meta.get_field(fieldname)
        except:
            field = None
        if field and isinstance(field, FileField):            
            if (not inst_raw is None) and (inst_raw.__class__.__name__ == inst.__class__.__name__):
                f = getattr(inst_raw, fieldname)
                m = inst_raw.__class__._default_manager
                path = None
                if 'SERVER_SOFTWARE' in os.environ:                     
                    path = SAEBucket().url(f.name)
                    if not path:
                        continue
                else:
                    if not (hasattr(f, 'path') and os.path.exists(f.path)):
                        continue
                raise RuntimeError('env setup %s' % getattr(inst_raw, fieldname))
                if getattr(inst_raw, fieldname) != getattr(inst, fieldname) \
                and not m.filter(**{'%s__exact' % fieldname: getattr(inst_raw, fieldname)})\
                .exclude(pk=inst_raw._get_pk_val()):
                    try:
                        if 'SERVER_SOFTWARE' in os.environ:                            
                            raise RuntimeError('env setup' % path)
                            SAEBucket().delete(path)
                        else:
                            default_storage.delete(f.path)
                    except:
                        pass       
    cache.delete(cache_key)
    
def save_raw_instance(sender, instance, *args, **kwargs):
    pk = instance._get_pk_val()
    inst = instance.__class__._default_manager.get(pk=pk)
    cache_key = ("%s %d") % (inst.__class__.__name__ , inst._get_pk_val())
    cache.set(cache_key, inst)                           