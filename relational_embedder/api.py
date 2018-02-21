import word2vec
from data_prep import data_prep_utils as dpu
from relational_embedder import composition
from scipy.spatial.distance import cosine
import pandas as pd
import numpy as np
import heapq


class Fabric:

    def __init__(self, we_model, relational_embedding, path_to_relations):
        self.M = we_model
        self.RE = relational_embedding
        self.path_to_relations = path_to_relations

    def topk_similar_vectors(self, input_string, k=10):
        el = dpu.encode_cell(input_string)
        indexes, metrics = self.M.cosine(el, n=k)
        res = self.M.generate_response(indexes, metrics).tolist()
        return res

    def similarity_between(self, entity1, entity2):
        x = dpu.encode_cell(entity1)
        y = dpu.encode_cell(entity2)
        vec_x = self.M.get_vector(x)
        vec_y = self.M.get_vector(y)
        distance = cosine(vec_x, vec_y)
        similarity = 1 - distance
        return similarity

    def analogy(self, x, y, z):
        """
        y is to ??? what z is to x
        :param x:
        :param y:
        :param z:
        :return:
        """
        x = dpu.encode_cell(x)
        y = dpu.encode_cell(y)
        z = dpu.encode_cell(z)
        indexes, metrics = self.M.analogy(pos=[x, y], neg=[z], n=10)
        res = self.M.generate_response(indexes, metrics).tolist()
        return res

    def vector_for_entity(self, cell=None, attribute=None, table=None):
        vec = None
        if cell:
            cell = dpu.encode_cell(cell)
            vec = self.M.get_vector(cell)
        elif table:
            table = dpu.encode_cell(table)
            if attribute:
                attribute = dpu.encode_cell(attribute)
                vec = self.RE[table]["columns"][attribute]
            else:
                vec = self.RE[table]["vector"]
        elif attribute:
            attribute = dpu.encode_cell(attribute)
            print("Not supported yet!")
            return
        return vec

    def topk_relations(self, vec_e, k=None):
        topk = []
        for vec, relation in self.relation_iterator():
            if np.isnan(vec).any():
                # FIXME: we could push this checks to building time, avoiding having bad vectors in the relemb
                continue
            distance = cosine(vec_e, vec)
            similarity = 1 - distance
            topk.append((relation, similarity))
        topk = sorted(topk, key=lambda x: x[1], reverse=True)
        if k:
            return topk[:k]
        else:
            return topk

    def topk_columns(self, vec_e, k=None):
        topk = []
        for vec, relation, column in self.column_iterator():
            if np.isnan(vec).any():
                # FIXME: we could push this checks to building time, avoiding having bad vectors in the relemb
                continue
            distance = cosine(vec_e, vec)
            similarity = 1 - distance
            topk.append((column, relation, similarity))
        topk = sorted(topk, key=lambda x: x[2], reverse=True)
        if k:
            return topk[:k]
        else:
            return topk

    def topk_rows(self, vec_e, k=5):
        # class HeapObj:
        #     def __init__(self, row, relation, similarity):
        #         self.row = row
        #         self.relation = relation
        #         self.similarity = similarity
        #
        #     def __lt__(self, other):
        #         return self.similarity < other.similarity
        # topk = heapq.heapify([])
        topk = []
        min_el = -1000
        for vec, relation, row_idx in self.row_iterator():
            if np.isnan(vec).any():
                # FIXME: we could push this checks to building time, avoiding having bad vectors in the relemb
                continue
            distance = cosine(vec_e, vec)
            similarity = 1 - distance
            # decide if we keep it or not
            if similarity > min_el:
                #row = self.resolve_row_idx(row_idx, relation)
                # Add and keep fixed-size
                topk.append((row_idx, relation, similarity))
                topk = sorted(topk, key=lambda x: x[2], reverse=True)
                topk = topk[:k]
                min_el = topk[-1][2]  # update min el to last value in list
        # Once found the row_idx, resolve them to actual rows before returning
        to_return = []
        for row_idx, relation, similarity in topk:
            row = self.resolve_row_idx(row_idx, relation)
            to_return.append((row, relation, similarity))
        return to_return

    """
    Iterator Utils
    """

    def relation_iterator(self):
        """
        Given a relational embedding, iterate over the relation vectors
        :param relational_embedding:
        :return:
        """
        for relation, v in self.RE.items():
            yield v["vector"], relation

    def column_iterator(self):
        """
        Given a relational embedding, iterate over the relation vectors
        :param relational_embedding:
        :return:
        """
        for relation, v in self.RE.items():
            for column, vector in self.RE[relation]["columns"].items():
                yield vector, relation, column

    def row_iterator(self):
        """
        Given a relational embedding, iterate over the rows
        :param relational_embedding:
        :return:
        """
        for relation, v in self.RE.items():
            for row_idx, vector in self.RE[relation]["rows"].items():
                yield vector, relation, row_idx

    """
    Utils
    """
    def resolve_row_idx(self, row_idx, relation):
        df = pd.read_csv(self.path_to_relations + "/" + relation, encoding='latin1')
        row = df.iloc[row_idx]
        return row


def init(path_to_we_model, path_to_relations):
    we_model = word2vec.load(path_to_we_model)
    relational_embedding = composition.compose_dataset(path_to_relations, we_model)
    api = Fabric(we_model, relational_embedding, path_to_relations)
    return api



if __name__ == "__main__":
    print("Fabric - relational embedding API")
