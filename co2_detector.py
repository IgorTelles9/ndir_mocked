import time
from sensors import CO2Sensor, BatterySensor
from network import MqttPublisher

class CO2Detector:
    """
    Controlador principal do Monitor de Qualidade do Ar.
    Coordena a leitura dos sensores e a transmissão contínua via rede.
    """
    def __init__(self, device_id: str, titular_id: int, broker: str = "localhost", port: int = 1883):
        self.device_id = device_id
        self.titular_id = titular_id
        self.topic = f"dispositivos/{self.device_id}/dados"
        
        # Instanciando componentes de hardware simulado
        self.co2_sensor = CO2Sensor(base_ppm=650.0)
        self.battery = BatterySensor()
        self.network = MqttPublisher(broker, port, client_id=f"detector_co2_{device_id}")
        
        # Frequência de envio abusiva (Gera o problema de privacidade)
        self.read_interval_seconds = 1.0 

    def turn_on(self):
        print("=========================================================")
        print(f" Inicializando AirQuality Monitor - Device ID: {self.device_id}")
        print("=========================================================")
        self.network.connect()
        time.sleep(1) # Aguarda handshake MQTT
        self._run_main_loop()

    def _run_main_loop(self):
        print(f"[SISTEMA] Iniciando monitoramento. Transmitindo a cada {self.read_interval_seconds}s...")
        print(f"[SISTEMA] Tópico alvo: {self.topic}\n")
        
        try:
            while True:
                if self.battery.level <= 0:
                    print("[SISTEMA] Bateria esgotada. Desligando...")
                    break

                # 1. Coleta dados físicos
                current_co2 = self.co2_sensor.read_ppm()
                current_battery = self.battery.consume()

                # 2. Monta o pacote de telemetria
                # Mantemos a chave "value" para compatibilidade com as Strategies do Gateway
                payload = {
                    "dispositivo_id": self.device_id,
                    "titular_id": self.titular_id,
                    "tipo_dispositivo": "co2_detector_indoor",
                    "metrica": "co2_ppm",
                    "value": current_co2, 
                    "ambiente": "home_office",
                    "status_bateria_pct": current_battery,
                    "timestamp": int(time.time())
                }

                # 3. Transmite
                json_sent = self.network.publish(self.topic, payload)
                
                # Log de tela
                print(f"[{time.strftime('%H:%M:%S')}] PUB: {json_sent}")
                
                time.sleep(self.read_interval_seconds)

        except KeyboardInterrupt:
            self.turn_off()

    def turn_off(self):
        print("\n[SISTEMA] Interrupção do usuário. Desligando...")
        self.network.disconnect()