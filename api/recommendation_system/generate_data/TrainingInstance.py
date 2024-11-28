class TrainingInstance:
    """
    
        A single training instance (sentence pair).

        Один обучающий пример (пара предложений).

        (Класс данных, который хранит в себе информацию)

        `info` - id Пользователя

        `tokens` - Последовательность пользователя

        `masked_lm_positions` - Номер индекса (для массива) замаскированных элементов

        `masked_lm_labels` - Название замаскированных элементов
    
    """

    def __init__(self, info, tokens, masked_lm_positions, masked_lm_labels):
        self.info = info
        self.tokens = tokens
        self.masked_lm_positions = masked_lm_positions
        self.masked_lm_labels = masked_lm_labels

    def __str__(self):
        s = ""
        s += f"info: {self.info}\n"
        s += f"tokens: {self.tokens}\n"
        s += f"masked_lm_positions: {self.masked_lm_positions}\n"
        s += f"masked_lm_labels: {self.masked_lm_labels}\n"
        s += "\n"
        return s

    def __repr__(self):
        return self.__str__()