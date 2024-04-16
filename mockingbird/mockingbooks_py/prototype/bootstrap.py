import json

from mockingbird.mockingbooks_py.analysis_tasks import create_analysis_task, get_task_id_by_name, get_task_by_name
from mockingbird.mockingbooks_py.evals import get_eval_id_by_name, create_or_update_eval
from mockingbird.mockingbooks_py.schemas import create_or_update_schema, get_schema_by_name
from mockingbird.mockingbooks_py.triggers import get_trigger_id_by_name
from mockingbird.mockingbooks_py.workflows import create_wf
from mockingbird.mockingbooks_py.workflows_examples import wf_model_task_template


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


def create_analysis_eval_only_wf(task_str_id, eval_str_id):
    with open('mocks/workflow.json', 'r') as file:
        jdata = json.load(file)

    jdata['workflowName'] = 'profile-extraction-with-qa-eval-wf'
    jdata['workflowGroup'] = 'extractions'

    jdata['stepSize'] = 30
    jdata['stepSizeUnit'] = 'minutes'

    # Add a task to the workflow
    wf_model_task_template['taskStrID'] = task_str_id
    jdata['models'][task_str_id] = wf_model_task_template

    # Get eval fn template
    with open('mocks/eval_fn.json', 'r') as file:
        ef_data = json.load(file)

    ef_data['evalStrID'] = eval_str_id
    # Add an eval to the workflow
    jdata['evalsMap'] = {
        eval_str_id: ef_data
    }
    jdata['evalTasksMap'] = {
        task_str_id: {
            eval_str_id: True
        }
    }
    pretty_data = json.dumps(jdata, indent=4)
    print(pretty_data)
    create_wf(jdata)


if __name__ == '__main__':
    tid = get_task_id_by_name('profile-extraction')
    eid = get_eval_id_by_name('profile-data-extraction-qa')
    create_analysis_eval_only_wf(tid, eid)
    # workflow_create()
    # profile-data-extraction


