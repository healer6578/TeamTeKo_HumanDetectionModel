#Libraries to import #가져올 라이브러리
import time
import serial
import requests

discord_webhook_url = "https://discord.com/api/webhooks/1136635165771309096/D5EozN59RBlrMNkcFPvyBmXbD_hw5N2byya30Rh_OZv-gtjI-oL6H_ATHc1MsWIQ1ivt"  #Replace with your Discord webhook URL #디스코드 웹후크 URL과 함께 넣습니다.
serial1 = serial.Serial('COM18', 115200)  # Correct the baud rate to 115200 #전송 속도를 115200으로 수정

def send_message_to_discord(message):
    data = {"content": message}
    try:
        result = requests.post(discord_webhook_url, json=data)
        result.raise_for_status()  #An exception if the request fails (status code >= 400) #요청이 실패한 경우 예외(상태 코드 >= 400)
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")

try:
    while True:
        dataString = serial1.readline().decode().strip()

        if "Starting inferencing" in dataString:
            send_message_to_discord("Received data: " + dataString)
        elif "Taking photo" in dataString:
            send_message_to_discord("Received data: " + dataString)
        elif "Predictions" in dataString:
            send_message_to_discord("Received data: " + dataString)
        else:
            send_message_to_discord("Received data: " + dataString)

            #Labeling the results #결과에 레이블 지정
            class_scores = {}
            if class_scores.get("Human", 0) > 6.0:
                send_message_to_discord("Result: non-disabled. Human Score: {:.2f}".format(class_scores.get("Human", 0)))
            elif class_scores.get("Cane", 0) > 6.0 or class_scores.get("Pregnant", 0) > 6.0:
                send_message_to_discord("Result: disabled. Cane Score: {:.2f}, Pregnant Score: {:.2f}".format(class_scores.get("Cane", 0), class_scores.get("Pregnant", 0)))

            #Extract class scores from the received data #수신된 데이터에서 클래스 점수 추출
            for line in dataString.splitlines():
                if ":" in line:
                    key, value = line.split(":")
                    class_scores[key.strip()] = float(value.strip())

        
        time.sleep(2)

#Program will stop when (Ctrl +  C) #프로그램은 (Ctrl + C)
except KeyboardInterrupt:
    send_message_to_discord("Keyboard interrupt detected. Exiting...")
finally:
    serial1.close()
