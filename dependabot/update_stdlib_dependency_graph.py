import json
from graphviz import Digraph
import requests

dependencies = []
stdlib_modules_by_level = dict()
stdlib_modules_json_file = 'https://raw.githubusercontent.com/ballerina-platform/ballerina-standard-library/' \
                               'main/release/resources/stdlib_modules.json'
graph_file_path = 'dashboard/stdlib_graph.gv'


def main():
    global dependencies
    global stdlib_modules_by_level
    global stdlib_modules_json_file

    read_stdlib_modules()
    if dependencies:
        create_graph(stdlib_modules_by_level, dependencies)


def read_stdlib_modules():
    try:
        response = requests.get(url=stdlib_modules_json_file)

        if response.status_code == 200:
            stdlib_modules_data = json.loads(response.text)
            read_dependency_data(stdlib_modules_data)
        else:
            print('Failed to access standard library dependency data from', stdlib_modules_json_file)

    except json.decoder.JSONDecodeError:
        print('Failed to load standard library dependency data')


def read_dependency_data(stdlib_modules_data):
    for module in stdlib_modules_data['modules']:
        parent = remove_module_group_name(module['name'])
        level = module['level']
        stdlib_modules_by_level[level] = stdlib_modules_by_level.get(level, []) + [parent]
        for dependent in module['dependents']:
            dependencies.append({'parent': parent, 'dependent': remove_module_group_name(dependent)})


def create_graph(levels, edges):
    graph = Digraph('Stdlib Dependency Graph')

    for level in levels:
        with graph.subgraph(name='cluster_' + str(level)) as cluster:
            cluster.attr(style='filled', color='lightgrey')
            cluster.node_attr.update(style='filled', color='white')
            for node in levels[level]:
                cluster.node(node)
            cluster.attr(label='level ' + str(level))

    for edge in edges:
        graph.edge(edge['parent'], edge['dependent'])

    graph.render(graph_file_path)


def remove_module_group_name(module_name):
    ballerina = "module-ballerina-"
    ballerinai = "module-ballerina-"
    ballerinax = "module-ballerinax-"

    if ballerina in module_name:
        module_name.replace(ballerina, "")
    elif ballerinai in module_name:
        module_name.replace(ballerinai, "")
    elif ballerinax in module_name:
        module_name.replace(ballerinax, "")

    return module_name


main()
