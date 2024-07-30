import json
import networkx as nx
from pyvis.network import Network
import argparse
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

def get_color_for_category(category, category_colors, color_palette):
    if category not in category_colors:
        # Assign the next color from the palette
        category_colors[category] = color_palette[len(category_colors) % len(color_palette)]
    return category_colors[category]

# def generate_category_dropdown(categories):
#     category_options = ''.join(f'<option value="{cat}">{cat}</option>' for cat in categories)
#     category_dropdown = f"""
#     <div style="margin-bottom: 10px;">
#         <label for="categorySelector">Select Category:</label>
#         <select id="categorySelector" onchange="filterGraph()">
#             <option value="all">All</option>
#             {category_options}
#         </select>
#     </div>
#     """
#     return category_dropdown

# def generate_legend_html(category_colors):
#     legend_html = '<div style="margin-top: 10px;">'
#     legend_html += '<strong>Legend:</strong><ul style="list-style: none; padding: 0;">'
#     for category, color in category_colors.items():
#         color_hex = mcolors.to_hex(color)
#         legend_html += f'<li><span style="background-color: {color_hex}; padding: 5px; margin-right: 10px;">&nbsp;&nbsp;&nbsp;&nbsp;</span>{category}</li>'
#     legend_html += '</ul></div>'
#     return legend_html

# def inject_html_to_file(html_file_path, category_dropdown, legend_html):
#     with open(html_file_path, 'r') as file:
#         html_content = file.read()

#     new_html_content = html_content.replace(
#         '<body>',
#         f'<body>{category_dropdown}{legend_html}'
#     )

#     new_html_content = new_html_content.replace(
#         '</body>',
#         """
#         <script type="text/javascript">
#             function filterGraph() {
#                 var selectedCategory = document.getElementById("categorySelector").value;
#                 var allNodes = network.body.data.nodes.get();
#                 var allEdges = network.body.data.edges.get();
#                 var filteredNodes = [];
#                 var filteredEdges = [];
                
#                 if (selectedCategory === "all") {
#                     filteredNodes = allNodes;
#                     filteredEdges = allEdges;
#                 } else {
#                     for (var node of allNodes) {
#                         if (node.group === selectedCategory) {
#                             filteredNodes.push(node);
#                         }
#                     }}
#                     for (var edge of allEdges) {
#                         var fromNode = filteredNodes.find(node => node.id === edge.from);
#                         var toNode = filteredNodes.find(node => node.id === edge.to);
#                         if (fromNode && toNode) {
#                             filteredEdges.push(edge);
#                         }
#                     }}
                
#                 network.body.data.nodes.clear();
#                 network.body.data.edges.clear();
#                 network.body.data.nodes.add(filteredNodes);
#                 network.body.data.edges.add(filteredEdges);
#             }
#         </script>
#         </body>
#         """
#     )

#     with open(html_file_path, 'w') as file:
#         file.write(new_html_content)


def main():
    parser = argparse.ArgumentParser(description="Generate a knowledge graph from a JSON file.")
    parser.add_argument('input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('output_file', type=str, help='Path to the output HTML file')
    args = parser.parse_args()

    with open(args.input_file) as f:
        data = json.load(f)

    complete_tuples = data["complete_tuples"]

    # Create a directed graph
    G = nx.DiGraph()

    # Color palette for categories (using matplotlib's tab20 palette for variety)
    color_palette = plt.cm.tab20.colors
    category_colors = {}

    # Add edges to the graph
    added_edges = set()
    categories = set()
    for t in complete_tuples:
        subject, predicate, obj, subject_type, obj_type = t
        edge = (subject, obj, predicate)
        if edge not in added_edges:
            subject_color = get_color_for_category(subject_type, category_colors, color_palette)
            obj_color = get_color_for_category(obj_type, category_colors, color_palette)
            G.add_node(subject, title=subject, color=subject_color, group=subject_type)
            G.add_node(obj, title=obj, color=obj_color, group=obj_type)
            G.add_edge(subject, obj, label=predicate)
            added_edges.add(edge)
            categories.add(subject_type)
            categories.add(obj_type)

    # Create a PyVis network
    net = Network(notebook=True, height='750px', width='100%', directed=True)

    # Load the NetworkX graph into PyVis
    net.from_nx(G)

    net.set_edge_smooth('dynamic')
    net.show(args.output_file)

    # Generate dropdown and legend HTML
    # category_dropdown = generate_category_dropdown(categories)
    # legend_html = generate_legend_html(category_colors)

    # Inject the dropdown and legend into the HTML file
    # inject_html_to_file(args.output_file, category_dropdown, legend_html)

if __name__ == "__main__":
    main()
