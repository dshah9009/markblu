from .version import VERSION

def version_context(request):
    return {'APP_VERSION': VERSION}
