import pandas as pd
import plotly.graph_objs as go
from .data import title_case_to_initials
from .colors import (default_colors,
                     generate_label_colors, hex_to_rgba, update_rgba_opacity)


# Functions included in this file:
# # digraph_dot_from_transition_matrix
# # make_sankey_df
# # make_link_and_node_df
# # plot_sankey


def digraph_dot_from_transition_matrix(transition_matrix, choices,
                                       colors=None, shape='circle'):
    """Automatically generates a digraph dot string.
    This only generates the string and is not responsible for plotting.

    Example Input:
    choices = ['Space Mountain', 'Indiana Jones Adventure', 'Haunted Mansion']
    transition_matrix = np.array([[0.8, 0.15, 0.05],
                                  [0.3, 0.65, 0.05],
                                  [0.15, 0.05, 0.8]],)
    Output:
    digraph {{
        rankdir=LR;
        node [shape=circle,style=filled,color=".7 .3 1.0"];
        SM
        IJA
        HM
        SM -> SM[label="0.8"];
        SM -> IJA[label="0.15"];
        SM -> HM[label="0.05"];
        IJA -> SM[label="0.3"];
        IJA -> IJA[label="0.65"];
        IJA -> HM[label="0.05"];
        HM -> SM[label="0.15"];
        HM -> IJA[label="0.05"];
        HM -> HM[label="0.8"];
    }}
    """
    choices_initials = [title_case_to_initials(x) for x in choices]

    header_text = []
    if colors:
        for choice, color in zip(choices_initials, colors):
            header_text.append(f"""\n    {choice}[shape={shape},style=filled,color={color}]""")
    else:
        for choice in choices_initials:
            header_text.append(f"""\n    {choice}[shape={shape}]""")
    header = "".join(header_text)

    body_text = []
    for i, choice in enumerate(choices_initials):
        for j, value in enumerate(transition_matrix[i]):
            body_text.append(f"""\n    {choices_initials[i]} -> {choices_initials[j]}[label="{value}"];""")
    body = "".join(body_text)

    digraph = f"""digraph {{
    rankdir=LR;""" + header + body + "\n}}"

    return digraph


def make_sankey_df(history_df, dropna=False, fillna='None'):
    """Counts the number of occurences of each line of the history_df
    
    Takes a history_df in this format:
     idx  |   0   |   1   | ...
    ------+-------+-------+-----
     id_1 | cat_1 | cat_2 | ...
     id_2 | cat_2 | None  | ...
    
    Returns:
        |   0   |   1   | ... | num | idx_0 | idx_1 | ...
    ----+-------+-------+-----+-----+-------+-------+-----
     1  | cat_1 | cat_2 | ... |  2  |   1   |   8   | ...
     2  | cat_2 | None  | ... | 10  |   2   |   9   | ...
    ...
    
    Eg. id_1 = RQ1, cat_1 = Saliva, cat_2 = Blood, etc.
    ...
    
    use history_df.pivot to get the history_df after indexing
    Eg:
    history_df = history_df.pivot(index='rq', columns='ib_num', values='specimen_type')
    """
    steps = history_df.columns.to_list()
    index = history_df.index.name
    history_df = history_df.fillna(fillna)

    sankey_df = history_df.reset_index().groupby(steps)[index].nunique().reset_index().rename(columns={index: 'num'})

    # generate source-target indices
    idx_start = 0
    if dropna is True:
        sankey_df = sankey_df.replace({fillna: None})
        for step in steps:
            sankey_df[f'step_{step}'] = sankey_df[step].astype('category').cat.codes.replace({-1: None}) + idx_start
            idx_start = sankey_df[f'step_{step}'].max() + 1
    else:
        for step in steps:
            sankey_df[f'step_{step}'] = sankey_df[step].astype('category').cat.codes + idx_start
            idx_start = sankey_df[f'step_{step}'].max() + 1

    return sankey_df


def make_link_and_node_df(sankey_df, num_steps: int, dropna=False):
    """Takes a df in the following format (output of make_sankey_df):
        |   0   |   1   | ... | num | step_0 | step_1 | ...
    ----+-------+-------+-----+-----+--------+--------+-----
     1  | cat_1 | cat_2 | ... |  2  |   0    |   8    | ...
     2  | cat_2 | None  | ... | 10  |   1    |   9    | ...
    ...
    
    Returns link_df:
       | source | target | num
    ---+--------+--------+-----
     0 |   0    |   8    | 114
     1 |   1    |   9    |  57
    ...
    
    Returns node_df:
       | source | label | step
    ---+--------+-------+--------
     0 |   0    | cat_1 | step_0
     1 |   1    | cat_2 | step_0
    ...
    """
    # reshape into source-target
    steps = range(num_steps)
    link_df = pd.lreshape(sankey_df,
                          groups={'source': [f'step_{step}' for step in steps[:-1]],
                                  'target': [f'step_{step}' for step in steps[1:]]})[['source', 'target', 'num']]
    link_df = link_df.groupby(['source', 'target']).sum().reset_index()

    # get index labels
    node_df = pd.lreshape(sankey_df,
                          groups={'source': [f'step_{step}' for step in steps],
                                  'label': steps})[['source', 'label']].drop_duplicates().sort_values(
        'source').reset_index(drop=True)

    # link source indices to step
    step_source = sankey_df[[f'step_{step}' for step in steps]].to_dict(orient='list')
    step_source = {k: list(set(v)) for k, v in step_source.items()}
    source_step_dict = {}
    for k, v in step_source.items():
        for source in v:
            source_step_dict[source] = k
    node_df['step'] = node_df['source'].apply(lambda x: source_step_dict[x])

    if dropna is True:
        # generate new indices for link_df
        step_stack_df = pd.lreshape(link_df, {'step_stack': ['source', 'target']})[['step_stack']]
        step_stack_df['new_idx'] = step_stack_df['step_stack'].astype('category').cat.codes
        step_stack_df = step_stack_df.drop_duplicates()
        replace_dict = dict(zip(step_stack_df['step_stack'], step_stack_df['new_idx']))
        link_df.loc[:, ['source', 'target']] = link_df.loc[:, ['source', 'target']].replace(
            replace_dict)  # reassign missing keys

        # filter out missing keys from node_df
        node_df = node_df[(node_df['source'].isin(replace_dict.keys()))]
        node_df.loc[:, 'source'] = node_df.loc[:, 'source'].replace(replace_dict)  # reassign missing keys

    return link_df, node_df


def plot_sankey(link_df, node_df,
                label_colors=None,
                title="Basic Sankey Diagram"):
    """Takes link_df and node_df as inputs:
    
    link_df:
       | source | target | num
    ---+--------+--------+-----
     0 |   0    |   8    | 114
     1 |   0    |   9    |  57
    ...
    
    node_df:
       | idx | label
    ---+-----+-------
     0 |  0  | cat_1
     1 |  1  | cat_2
    
    label_colors should be hex
    """
    num_steps = node_df['step'].nunique() - 1
    node_df.loc[:, 'x_pos'] = node_df['step'].astype('category').cat.codes / num_steps
    node_df.loc[:, 'y_pos'] = 0.001

    sankey = go.Sankey(arrangement="snap",
                       node={'pad': 15, 'thickness': 20,
                             'line': {'color': 'black', 'width': 0.5},
                             'x': node_df['x_pos'].to_list(),
                             'y': node_df['y_pos'].to_list(),
                             'label': node_df['label'].to_list()
                             },
                       link={'source': link_df['source'].to_list(),
                             'target': link_df['target'].to_list(),
                             'value': link_df['num'].to_list(),
                             }
                       )

    if label_colors:
        node_df['color'] = node_df['label'].apply(lambda cat: hex_to_rgba(label_colors[cat], opacity=0.9))
        sankey.node.color = node_df['color'].to_list()
        sankey.link.color = sankey.node.color
        sankey.link.color = [update_rgba_opacity(sankey.node.color[idx], 0.3) for idx in sankey.link.source]
    else:
        label_colors = generate_label_colors(node_df['label'].unique(), default_colors)
        node_df['color'] = node_df['label'].apply(lambda cat: label_colors[cat])
        sankey.node.color = node_df['color'].to_list()

    fig = go.Figure(data=sankey)
    fig.update_layout(title_text=title, font_size=10)
    return fig
