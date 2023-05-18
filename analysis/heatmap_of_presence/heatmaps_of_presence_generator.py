"""Generate the heatmap"""
import pandas as pd

from heatmap_of_presence_builder import order_data
from heatmap_of_presence_builder import compose_heatmap


def algorithm(paths: [], convert_to_csv=False):
    for i in range(len(paths)):
        try:
            path = paths[i]
            dataframe = pd.read_csv(path)
            real_route_presence, planned_route_presence, route_carrier = order_data(dataframe)

            if convert_to_csv:
                real_route_presence.to_csv(f"real_route_presence{i}.csv")
                planned_route_presence.to_csv(f"planned_route_presence{i}.csv")

            real_to_planned_relation = real_route_presence[:-1] / planned_route_presence[:-1]

            heatmap = compose_heatmap(real_to_planned_relation, route_carrier)
            heatmap.show()
        except:
            print("ERROR OCCURRED")


if __name__ == '__main__':
    demo_files_amount = 6
    paths = [f"sample{i}.csv" for i in range(demo_files_amount)]
    print(paths)
    algorithm(paths, convert_to_csv=True)
