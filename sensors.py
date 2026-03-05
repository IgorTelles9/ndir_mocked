import random

class CO2Sensor:
    """
    Simula um sensor de Dióxido de Carbono (NDIR).
    Usa um modelo de random walk para gerar leituras de PPM 
    que flutuam suavemente.
    """
    def __init__(self, base_ppm: float = 600.0):
        # 400 ppm é o ar livre. 600-800 é um ambiente interno normal.
        self.current_ppm = base_ppm
        self.min_ppm = 400.0
        self.max_ppm = 5000.0 # Nível tóxico/abafado

    def read_ppm(self) -> float:
        # Flutuação aleatória para simular respiração e correntes de ar
        fluctuation = random.uniform(-3.0, 5.0) 
        self.current_ppm += fluctuation
        
        # Garante que não caia abaixo do nível atmosférico natural
        self.current_ppm = max(self.min_ppm, min(self.max_ppm, self.current_ppm))
        
        return round(self.current_ppm, 1)

class BatterySensor:
    """Simula o descarregamento da bateria do dispositivo."""
    def __init__(self):
        self.level = 100.0

    def consume(self, amount: float = 0.05):
        self.level -= amount
        self.level = max(0.0, self.level)
        return round(self.level, 1)