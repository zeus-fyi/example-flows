import json

from mockingbird.mockingbooks_py.analysis_tasks import create_analysis_task, get_task_id_by_name, get_task_by_name
from mockingbird.mockingbooks_py.schemas import create_or_update_schema, get_schema_by_name
from mockingbird.mockingbooks_py.workflows import create_wf


def schema_create():
    with open('mocks/schema.json', 'r') as file:
        data = json.load(file)
    create_or_update_schema(data)


def analysis_create():
    with open('mocks/analysis.json', 'r') as file:
        data = json.load(file)
    data['schemas'] = [get_schema_by_name('profile-data-extraction')]
    create_analysis_task(data)


def workflow_create():
    with open('mocks/workflow.json', 'r') as file:
        jdata = json.load(file)

    jdata['stepSize'] = 10
    jdata['stepSizeUnit'] = 'minutes'

    # Add a task to the workflow
    task_str_id = get_task_id_by_name('profile-extraction')
    jdata['models'][task_str_id] = get_task_by_name('profile-extraction')

    pretty_data = json.dumps(jdata, indent=4)
    print(pretty_data)
    create_wf(jdata)


if __name__ == '__main__':
    workflow_create()
