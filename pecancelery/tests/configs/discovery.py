import sampleproj

app = {
    'modules': [sampleproj]
}

celery = {
    'CELERY_ALWAYS_EAGER'                   : True,
    'CELERY_EAGER_PROPAGATES_EXCEPTIONS'    : False
}