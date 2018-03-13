import numpy as np


class Cluster(object):
    def __init__(self, point_data):
        self._center = np.array(point_data)
        self._point_list = []

    def update_center(self):
        num_list = [i.record_data for i in self._point_list]
        self._center = np.mean(num_list, axis=0)

    def clear_point(self):
        self._point_list.clear()

    def get_distance(self, point_data):
        if not isinstance(point_data, np.ndarray):
            np.array(point_data)
        return np.linalg.norm(self._center - point_data)

    def add(self, point_data):
        self._point_list.append(point_data)

    def count_confuse_matrix(self, labels):
        same_count = np.zeros(len(labels), dtype=int)
        label_point = [i.get_label() for i in self._point_list]
        for i in range(len(labels)):
            same_count[i] = label_point.count(labels[i])
        return same_count
