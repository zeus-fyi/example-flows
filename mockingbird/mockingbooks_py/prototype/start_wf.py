import json

from mockingbird.mockingbooks_py.entities import EntitiesFilter, search_entities
from mockingbird.mockingbooks_py.runs import get_run
from mockingbird.mockingbooks_py.workflows import start_or_schedule_wf


def read_text_file(file_path):
    """
    Reads a text file and returns its content as a string.

    Args:
    file_path (str): The path to the text file.

    Returns:
    str: The content of the file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"


def start_wf(prompt=None):
    with open('mocks/wf_exec.json', 'r') as file:
        wf_exec = json.load(file)

    # ex. use  import a csv file as inputs, and exec wf for each row
    # with open('search_entities/crm.csv', 'r') as file:
    #     inputs = json.load(file)
    # Inject override prompt, allows wf inputs to operate like function inputs

    prompt = {"promptOverride1": prompt}
    tmp = {}
    if prompt:
        tmp['profile-extraction'] = {'replacePrompts': prompt}
        wf_exec['taskOverrides'] = tmp

    wf_item = {
        'workflowName': 'profile-extraction-wf',
    }
    wf_exec['workflows'] = [wf_item]
    pretty_data = json.dumps(wf_exec, indent=4)
    print(pretty_data)

    start_or_schedule_wf(wf_exec)


if __name__ == '__main__':
    fc = read_text_file('fake_inputs/profile_examples.txt')
    start_wf(fc)

