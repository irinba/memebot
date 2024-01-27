from transformers import AutoTokenizer
import onnxruntime as ort
import numpy as np
from config import MODEL_PATH
from typing import List, Union


class EmbeddingModel:
    def __init__(self):
        """
        Инициализирует модель для получения эмбеддингов текстов.

        Загружает токенайзер и ONNX Runtime сессию для заданной предобученной модели.
        """
        self.tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-small')
        self.ort_session = ort.InferenceSession(MODEL_PATH)

    def get_embedding(self, input_texts: Union[str, List[str]]) -> np.ndarray:
        """
        Получает эмбеддинги для предоставленного текста или списка текстов.

        :param input_texts: Один текст или список текстов для обработки.
        :return: Массив эмбеддингов для каждого из входных текстов.
        """
        inputs = self.tokenizer(input_texts, max_length=128, padding='max_length', truncation=True, return_tensors='np')

        ort_inputs = {self.ort_session.get_inputs()[0].name: inputs['input_ids'],
                      self.ort_session.get_inputs()[1].name: inputs['attention_mask']}

        sentence_embeddings = self.ort_session.run(None, ort_inputs)[1]
        # нормализация эмбеддингов
        norms = np.linalg.norm(sentence_embeddings, axis=1, keepdims=True)
        normalized_embeddings = sentence_embeddings / norms
        return normalized_embeddings
