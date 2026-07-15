from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List
import subprocess
import os
import glob
from makeup import apply_full_makeup
from color_analysis import extract_colors

app = FastAPI()

# --- Connection Manager for WebSockets ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Örnek: Flutter'dan gelen bir mesajı simüle et (AI Asistan gibi)
            print(f"Soketten gelen veri: {data}")
            await manager.send_personal_message(f"Sunucu: '{data}' bilgisini aldı.", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/generate-3d")
async def generate_3d_model(
    file: UploadFile = File(...),
    lip_color: Optional[str] = Form(None),
    blush_color: Optional[str] = Form(None),
    eyeshadow_color: Optional[str] = Form(None),
    contour_color: Optional[str] = Form(None),
    concealer_color: Optional[str] = Form(None),
    eyeliner_color: Optional[str] = Form(None),
    foundation_color: Optional[str] = Form(None),
    foundation_intensity: Optional[float] = Form(0.0),
    bronzer_color: Optional[str] = Form(None),
    bronzer_intensity: Optional[float] = Form(0.15)
):
    # 1. Flutter'dan gelen fotoğrafı kaydet
    input_image_path = f"temp_{file.filename}"
    with open(input_image_path, "wb") as buffer:
        buffer.write(await file.read())

    # 2. Makyaj ayarları var mı kontrol et, varsa uygula (Orijinal resmin üzerine yazılır)
    if any([lip_color, blush_color, eyeshadow_color, contour_color, concealer_color, eyeliner_color, foundation_intensity > 0, bronzer_color]):
        print(f"Makyaj uygulanıyor: Dudak={lip_color}, Allık={blush_color}, Far={eyeshadow_color}, Fondöten={foundation_intensity}")
        success = apply_full_makeup(
            image_path=input_image_path, 
            out_path=input_image_path, 
            lip_hex=lip_color, 
            blush_hex=blush_color, 
            eye_hex=eyeshadow_color,
            contour_hex=contour_color,
            concealer_hex=concealer_color,
            eyeliner_hex=eyeliner_color,
            foundation_hex=foundation_color,
            foundation_alpha=foundation_intensity,
            bronzer_hex=bronzer_color,
            bronzer_alpha=bronzer_intensity
        )
        if not success:
            print("Uyarı: Makyaj uygulanamadı (Belki yüz bulunamadı).")

    # 3. 3D modele dönüştürmek için cli_demo.py'yi çalıştır
    command = [
        "python",
        "cli_demo.py",
        "-i", input_image_path
    ]

    print(f"Çalıştırılan komut: {' '.join(command)}")
    subprocess.run(command, check=True)

    # 4. Çıkan ZIP dosyasını bul ve gönder
    zip_files = glob.glob("*.zip") + glob.glob("results/*.zip")
    if not zip_files:
        return {"error": "3D model olusturuldu ama ZIP dosyasi klasörde bulunamadi!"}

    latest_zip = max(zip_files, key=os.path.getctime)
    print(f"Bulunan 3D Model: {latest_zip}")

    return FileResponse(path=latest_zip, media_type='application/zip', filename="3d_model_yuz.zip")

@app.post("/api/apply-makeup-texture")
async def apply_makeup_texture(
    file: UploadFile = File(...),
    lip_color: Optional[str] = Form(None),
    blush_color: Optional[str] = Form(None),
    eyeshadow_color: Optional[str] = Form(None),
    contour_color: Optional[str] = Form(None),
    concealer_color: Optional[str] = Form(None),
    eyeliner_color: Optional[str] = Form(None),
    foundation_color: Optional[str] = Form(None),
    foundation_intensity: Optional[float] = Form(0.0),
    bronzer_color: Optional[str] = Form(None),
    bronzer_intensity: Optional[float] = Form(0.15)
):
    input_image_path = f"temp_tex_{file.filename}"
    with open(input_image_path, "wb") as buffer:
        buffer.write(await file.read())

    if any([lip_color, blush_color, eyeshadow_color, contour_color, concealer_color, eyeliner_color, foundation_intensity > 0, bronzer_color]):
        print(f"Makyaj uygulanıyor (Texture): Dudak={lip_color}, Allık={blush_color}, Far={eyeshadow_color}, Fondöten={foundation_intensity}")
        success = apply_full_makeup(
            image_path=input_image_path, 
            out_path=input_image_path, 
            lip_hex=lip_color, 
            blush_hex=blush_color, 
            eye_hex=eyeshadow_color,
            contour_hex=contour_color,
            concealer_hex=concealer_color,
            eyeliner_hex=eyeliner_color,
            foundation_hex=foundation_color,
            foundation_alpha=foundation_intensity,
            bronzer_hex=bronzer_color,
            bronzer_alpha=bronzer_intensity
        )
        if not success:
            print("Uyarı: Texture üzerinde makyaj uygulanamadı (Belki yüz bulunamadı).")

    return FileResponse(path=input_image_path, media_type='image/jpeg', filename=file.filename)


@app.post("/api/analyze-colors")
async def analyze_colors(file: UploadFile = File(...), api_key: Optional[str] = Form("")):
    """Yüzden renkleri çıkarır ve yapay zeka ile analiz eder."""
    input_image_path = f"temp_color_{file.filename}"
    with open(input_image_path, "wb") as buffer:
        buffer.write(await file.read())

    # 1. Renkleri çıkar (Cilt, Göz, Dudak)
    skin_hex, iris_hex, lips_hex = extract_colors(input_image_path)
    
    if not skin_hex or not iris_hex or not lips_hex:
        os.remove(input_image_path)
        return JSONResponse(status_code=400, content={"error": "Yüz hatları tam olarak algılanamadı, lütfen daha net bir fotoğraf yükleyin."})

    # 2. Eğer kullanıcı kendi Gemini API anahtarını verdiyse analizi yap
    analysis_text = "API anahtarı verilmediği için detaylı yapay zeka analizi yapılamadı."
    # Removed generate_color_analysis_text usage as it is no longer provided
    # if api_key:
    #     analysis_text = generate_color_analysis_text(skin_hex, iris_hex, lips_hex, api_key)

    os.remove(input_image_path)

    return {
        "skin_color": skin_hex,
        "iris_color": iris_hex,
        "lip_color": lips_hex,
        "ai_analysis": analysis_text
    }

@app.post("/api/analyze-skin")
async def analyze_skin(file: UploadFile = File(...)):
    from color_analysis import analyze_skin_endpoint_logic
    input_image_path = f"temp_skin_{file.filename}"
    with open(input_image_path, "wb") as buffer:
        buffer.write(await file.read())

    result = analyze_skin_endpoint_logic(input_image_path)
    if os.path.exists(input_image_path):
        os.remove(input_image_path)

    if result is None:
        return JSONResponse(status_code=400, content={"error": "Yüz tespit edilemedi veya model çalıştırılamadı."})
        
    return JSONResponse(content=result)

@app.get("/api/debug-mediapipe")
def debug_mediapipe():
    try:
        import importlib
        import mediapipe as mp
        from mediapipe.python.solutions import face_mesh as mp_face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)
        return {"status": "success", "message": "Mediapipe başarıyla yüklendi."}
    except Exception as e:
        import traceback
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

