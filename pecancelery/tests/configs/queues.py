import sampleproj

app = {
    'modules': [sampleproj]
}

celery = {
    'CELERYD_QUEUES': 'example,testing123'
}