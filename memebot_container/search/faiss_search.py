import faiss
import numpy as np
from config import EMBEDDINGS_PATH
from typing import Tuple


class FaissSearch:
    def __init__(self):
        """
        Инициализирует объект FaissSearch с индексом Faiss для поиска по эмбеддингам.

        Эмбеддинги загружаются из файла 'embeddings_onnx.npy', а затем добавляются в индекс Faiss.
        Используется косинусное расстояние для сравнения эмбеддингов.
        """
        self.index = faiss.IndexFlatIP(384)
        embeddings = np.load(EMBEDDINGS_PATH)
        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, k: int=5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Выполняет поиск похожих эмбеддингов в индексе Faiss.

        :param query_embedding: Эмбеддинг запроса, для которого необходимо найти похожие элементы.
        :param k: Количество возвращаемых результатов.
        :return: Кортеж, содержащий массив расстояний и массив индексов k наиболее похожих элементов.
        """
        distances, indices = self.index.search(query_embedding, k)
        return distances, indices
