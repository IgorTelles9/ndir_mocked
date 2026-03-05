import json
import paho.mqtt.client as mqtt

class MqttPublisher:
    """Gerencia a conexão e publicação de mensagens no Broker MQTT."""
    
    def __init__(self, broker: str, port: int, client_id: str):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.client = mqtt.Client(client_id=self.client_id)
        
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[REDE] {self.client_id} conectado com sucesso ao Broker {self.broker}:{self.port}")
        else:
            print(f"[REDE] Falha na conexão. Código: {rc}")

    def _on_disconnect(self, client, userdata, rc):
        print(f"[REDE] {self.client_id} desconectado.")

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"[REDE] Erro crítico ao tentar conectar: {e}")

    def publish(self, topic: str, payload: dict):
        """Publica o dicionário como um JSON no tópico especificado."""
        payload_str = json.dumps(payload)
        self.client.publish(topic, payload_str)
        return payload_str 

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()