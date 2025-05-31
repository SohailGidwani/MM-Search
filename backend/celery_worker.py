from app import create_app

app, celery = create_app()

if __name__ == '__main__':
    celery.worker_main(['worker', '--loglevel=info', '--pool=solo'])