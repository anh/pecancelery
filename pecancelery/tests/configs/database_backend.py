celery = {
    'CELERY_IMPORTS'                : ('package.module.tasks',),
    'CELERY_RESULT_BACKEND'         : 'database',
    'CELERY_RESULT_DBURI'           : 'postgresql+psycopg2://user:pass@localhost/table'
}
