# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    logger.info('Suma ejecutada')
    return x + y


@shared_task
def mul(x, y):
    logger.info('Multiplicacion ejecutada')
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


