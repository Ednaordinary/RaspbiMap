import math
import json
import tqdm

# Cluster connection mechanism
# Take points and grow them until they hit others.
# Each point can connect to one point, but two cannot connect to eachother

class Point():
    def __init__(self, x, y, pointid):
        self.id = pointid
        self.x = x
        self.y = y
    def __str__(self):
        return str("Point " + str(self.id) + ": x(" + str(self.x) + ") y(" + str(self.y) + ")")
    def __repr__(self):
        return self.__str__()

class Cluster():
    def __init__(self):
        self.points = {}
        self.e = {}
    def register(self, point):
        self.points[point] = None
    def register_e(self, point):
        self.e[point] = [None]
    def drop_depth(self, cutoff):
        depths = []
        depth = 0
        for point in tqdm.tqdm(self.points.keys()):
            depth = 0
            for mpoint in self.points.keys():
                depth += ((point.x + mpoint.x)**2 + (point.y + mpoint.y)**2)**0.5
            depth = 1 / depth
            depths.append([point, depth])
        depths = sorted(depths, key=lambda x: x[1])
        #print(depths)
        #print(len(depths))
        depths = depths[int(len(depths)*cutoff):]
        dropped = depths[:int(len(depths)*cutoff)]
        #print(len(depths), len(dropped))
        temp_points = {}
        for point, depth in depths:
            temp_points[point] = self.points[point]
        self.points = temp_points
        return dropped
    def grow(self):
        for i, v in tqdm.tqdm(self.points.items()):
            candidate = [None, 0]
            for p, y in self.points.items():
                if y == None and p != i:
                    dist = ((i.x + p.x)**2 + (i.y + p.y)**2)**0.5
                    if dist > candidate[1] or candidate[1] == 0:
                        candidate = [p, dist]
            self.points[i] = candidate[0]
    def format_lines(self):
        segments = []
        for i, v in self.points.items():
            if v != None:
                segments.append([(i.x, i.y), (v.x, v.y)])
        return segments
    def export_cluster(self, location):
        export_points = {i.id: [i.x, i.y, (None if v is None else [v.id, v.x, v.y])] for (i, v) in self.points.items()}
        export_e = {i.id: [i.x, i.y, (None if v is None else [v.id, v.x, v.y])] for (i, v) in self.e.items()}
        with open(location, 'w', encoding='utf-8') as f:
            json.dump([export_points, export_e], f, ensure_ascii=False, indent=4)
    def import_cluster(self, location):
        with open(location, 'r') as f:
            import_cluster = json.load(f)
        import_points = {Point(float(v[0]), float(v[1]), int(x)): v[2] for (x, v) in import_cluster[0].items()}
        for point, v in tqdm.tqdm(import_points.items()):
            for p, y in import_points.items():
                if not isinstance(v, type(None)) and v[0] == p.id:
                    import_points[point] = p
                    break
        import_e = {Point(v[0], v[1], x): v[2] for (x, v) in import_cluster[1].items()}
        for point, v in import_e.items():
            for p, y in import_e.items():
                if v == p.id:
                    import_e[point] = p
                    break
        self.points = import_points
        self.e = import_e
