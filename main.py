from co2_detector import CO2Detector

# Configurações do ambiente de teste
BROKER_MQTT = "localhost" 
DISPOSITIVO_ID = "4"      
TITULAR_ID = 1

if __name__ == "__main__":
    detector = CO2Detector(
        device_id=DISPOSITIVO_ID,
        titular_id=TITULAR_ID,
        broker=BROKER_MQTT
    )
    
    detector.turn_on()