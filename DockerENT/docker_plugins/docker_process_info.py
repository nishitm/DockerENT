"""Docker running processes-info scan plugin."""
from DockerENT.utils import utils

import docker
import logging

_log = logging.getLogger(__name__)

_plugin_name_ = 'procinfo'


def scan(container, output_queue):
    """Docker running processes-info plugin scan.

    :param container: container instance.
    :type container: docker.models.containers.Container

    :param output_queue: Output holder for this plugin.
    :type output_queue: multiprocessing.managers.AutoProxy[Queue]

    :return: This plugin returns the object in this form.
    {
        _plugin_name_: {
            'test_performed': {
                'results':  []
            }
        }
    }
    """
    res = {}

    _log.info('Staring {} Plugin ...'.format(_plugin_name_))

    api_client = docker.APIClient()
    container_obj = api_client.containers(container.short_id)
    top_result = api_client.top(container_obj[0])

    running_processes = {
        "Running_Processes": {
            "msg": " Check all running processes inside container. ",
            "results": [[]]
        },

    }

    for option in running_processes.keys():
        top_result['Processes'].insert(0, top_result['Titles'])
        for result in top_result['Processes']:
            running_processes[option]['results'].append(result)

    res[container.short_id] = {
        _plugin_name_: running_processes
    }

    _log.info('Completed execution of {} Plugin.'.format(_plugin_name_))
    output_queue.put(res)
