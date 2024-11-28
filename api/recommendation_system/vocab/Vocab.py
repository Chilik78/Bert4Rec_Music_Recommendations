from collections import Counter



class Vocab:
    """Выполняет сквозную токенизацию."""

    def __init__(self, user_to_list):
        # layout of the  ulary
        # item_id based on freq
        # special token
        # user_id based on nothing
        self.counter = Counter()
        self.user_set = set()
        for u, item_list in user_to_list.items():
            self.counter.update(item_list)
            self.user_set.add(str(u))

        self.user_count = len(self.user_set)
        self.item_count = len(self.counter.keys())
        self.special_tokens = {"[pad]", "[MASK]", '[NO_USE]'}
        self.token_to_ids = {}  # index begin from 1

        # Присвоение ID каждому item
        for token, count in self.counter.most_common():
            self.token_to_ids[token] = len(self.token_to_ids) + 1

        # Присвоение ID специальным токенам (Добавляется в конце) 
        for token in self.special_tokens:
            self.token_to_ids[token] = len(self.token_to_ids) + 1

        self.id_to_tokens = {v: k for k, v in self.token_to_ids.items()}
        self.vocab_words = list(self.token_to_ids.keys())

    def convert_tokens_to_ids(self, tokens):
        return self.__convert_by_vocab(self.token_to_ids, tokens)

    def convert_ids_to_tokens(self, ids):
        return self.__convert_by_vocab(self.id_to_tokens, ids)

    def __convert_by_vocab(self, vocab, items):
        """
            Converts a sequence of [tokens|ids] using the vocab.

            Преобразует последовательность [токенов|идентификаторов] с помощью vocab.    
        """
        output = []
        for item in items:
            output.append(vocab[item])
        return output

    @property
    def get_vocab_words(self):
        return self.vocab_words  # not in order

    @property
    def get_item_count(self):
        return self.item_count
    
    @property
    def get_user_count(self):
        return self.user_count

    @property
    def get_items(self):
        return list(self.counter.keys())

    @property
    def get_users(self):
        return self.user_set

    @property
    def get_special_token_count(self):
        return len(self.special_tokens)

    @property
    def get_special_token(self):
        return self.special_tokens

    @property
    def get_vocab_size(self):
        return self.get_item_count + self.get_special_token_count + 1 #self.get_user_count()