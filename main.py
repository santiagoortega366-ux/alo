"""EyeSafe - Punto de entrada.

Pipeline: captura -> detección de personas (visión por computador)
-> análisis de contexto (hora/zona) -> alerta en tiempo real.

Esqueleto funcional: amplíalo con tus propios modelos y reglas.
"""
import argparse
import os
import time
from datetime import datetime

import cv2
from dotenv import load_dotenv
from ultralytics import YOLO

PERSON_CLASS_ID = 0  # clase "person" en COCO


def parse_active_hours(value: str):
    start, end = value.split("-")
    fmt = "%H:%M"
    return (datetime.strptime(start, fmt).time(), datetime.strptime(end, fmt).time())


def is_within_hours(now, start, end) -> bool:
    if start <= end:
        return start <= now <= end
    return now >= start or now <= end  # franja que cruza medianoche


def evaluate_context(zone: str, now: datetime, active_hours) -> str:
    """Devuelve el nivel de riesgo: 'bajo' o 'alto'.

    Regla base: una persona dentro del horario de actividad normal es esperada;
    fuera de él es sospechosa. Aquí puedes agregar reglas por zona, tipo de
    actividad, objetos adicionales (vehículos/animales), etc.
    """
    start, end = active_hours
    return "bajo" if is_within_hours(now.time(), start, end) else "alto"


def send_alert(channel: str, zone: str, confidence: float, frame, events_dir: str):
    os.makedirs(events_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(events_dir, f"alerta_{zone}_{stamp}.jpg")
    cv2.imwrite(path, frame)
    message = f"🚨 [{stamp}] Persona detectada en '{zone}' (confianza {confidence:.2f}). Evidencia: {path}"
    if channel == "console":
        print(message)
    else:
        # TODO: implementar envío por Telegram / correo
        print(f"[{channel}] canal no implementado aún. {message}")


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="EyeSafe - vigilancia rural inteligente")
    parser.add_argument("--source", default=os.getenv("CAMERA_SOURCE", "0"))
    parser.add_argument("--mode", choices=["live", "demo"], default="live")
    args = parser.parse_args()

    source = int(args.source) if str(args.source).isdigit() else args.source
    zone = os.getenv("CAMERA_ZONE", "zona_principal")
    threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))
    active_hours = parse_active_hours(os.getenv("ACTIVE_HOURS", "06:00-18:00"))
    channel = os.getenv("ALERT_CHANNEL", "console")
    cooldown = int(os.getenv("ALERT_COOLDOWN", "60"))
    frame_skip = int(os.getenv("FRAME_SKIP", "5"))
    model = YOLO(os.getenv("MODEL_PATH", "yolov8n.pt"))

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise SystemExit(f"No se pudo abrir la fuente de video: {args.source}")

    print(f"👁️  EyeSafe iniciado | zona: {zone} | modo: {args.mode}")
    last_alert, count = 0.0, 0

    while True:
        ok, frame = cap.read()
        if not ok:
            if args.mode == "demo":
                break  # fin del video de prueba
            time.sleep(2)  # reintento ante caída del stream
            cap.open(source)
            continue

        count += 1
        if count % frame_skip:
            continue

        result = model(frame, classes=[PERSON_CLASS_ID], conf=threshold, verbose=False)[0]
        if len(result.boxes) == 0:
            continue

        confidence = float(result.boxes.conf.max())
        risk = evaluate_context(zone, datetime.now(), active_hours)

        if risk == "alto" and time.time() - last_alert >= cooldown:
            send_alert(channel, zone, confidence, result.plot(), "events")
            last_alert = time.time()
        elif risk == "bajo":
            print(f"ℹ️  Persona en horario normal ({zone}). Evento registrado sin alerta.")

    cap.release()
    print("✅ Procesamiento finalizado.")


if __name__ == "__main__":
    main()
