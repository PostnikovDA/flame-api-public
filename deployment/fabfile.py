from fabric.api import env, run, cd

from .host import production

env.hosts = production
env.user = 'root'


def deploy(branch='master'):
    path = '/opt/flame-api'
    with cd(path):
        run("git pull origin {0}".format(branch))

    with cd(path):
        run("docker-compose up -d --build flame-api")
