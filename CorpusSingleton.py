from Corpus import Corpus

class CorpusSingleton(Corpus):
    _instance = None

    def __new__(cls, nom):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # initialiser seulement si nouvelle instance
            cls._instance.__init__(nom)
        return cls._instance
    
    def __init__(self, nom):
        # Initialiser une seule fois
        if not hasattr(self, "_initialized"):
            super().__init__(nom)
            self._initialized = True