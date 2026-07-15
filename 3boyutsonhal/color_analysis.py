import cv2
import numpy as np
import traceback

try:
    import mediapipe as mp
    from mediapipe.python.solutions import face_mesh as mp_face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)
except Exception as e:
    face_mesh = None

LEFT_IRIS = 468
LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291]

def bgr_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[2]), int(color[1]), int(color[0]))

def extract_colors(image_path):
    try:
        frame = cv2.imread(image_path)
        if frame is None: return None, None, None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        if not results.multi_face_landmarks: return None, None, None
        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = frame.shape

        # Tam olarak istenen 3 nokta: Alın ortası(151), Sol Yanak içi(425), Sağ Yanak içi(205)
        three_points = [151, 205, 425]
        safe_pixels = []
        patch_size = 5
        
        for idx in three_points:
            cx, cy = int(face_landmarks.landmark[idx].x * w), int(face_landmarks.landmark[idx].y * h)
            roi = frame[max(0, cy-patch_size):min(h, cy+patch_size), max(0, cx-patch_size):min(w, cx+patch_size)]
            if roi.size > 0: safe_pixels.extend(roi.reshape(-1, 3))
            
        if len(safe_pixels) == 0:
            skin_color = (0,0,0)
        else:
            r_val, g_val, b_val = np.median(np.array(safe_pixels), axis=0)
            skin_color = (int(b_val), int(g_val), int(r_val)) # BGR format
        
        iris_point = face_landmarks.landmark[LEFT_IRIS]
        ix, iy = int(iris_point.x * w), int(iris_point.y * h)
        iris_color = frame[iy, ix] if (0 <= ix < w and 0 <= iy < h) else (0,0,0)

        lip_points = np.array([[int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)] for i in LIPS], np.int32)
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [lip_points], 255)
        mean_lip_color = cv2.mean(frame, mask=mask)[:3]

        return bgr_to_hex(skin_color), bgr_to_hex(iris_color), bgr_to_hex(mean_lip_color)
    except:
        return "#F0D5B8", "#000000", "#FF0000"

def calculate_skin_tone_and_undertone(bgr_color):
    b, g, r = bgr_color
    hsv = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]
    h, s, v = hsv
    
    # Daha hassas ten rengi parlaklık değerleri
    if v > 200: cilt_rengi = "Açık"
    elif v > 150: cilt_rengi = "Buğday"
    elif v > 90: cilt_rengi = "Esmer"
    else: cilt_rengi = "Koyu"
        
    # Daha hassas alt ton sınırları
    if h < 10 or h > 165: alt_ton = "Pembe Alt Tonlu"
    elif h < 18: alt_ton = "Nötr Alt Tonlu"
    else: alt_ton = "Sarı Alt Tonlu"
    return cilt_rengi, alt_ton

def get_product_recommendations(cilt_rengi, alt_ton, exact_hex):
    recs = {"fondöten": [], "kapatıcı": [], "allık": [], "ruj": [], "far": []}
    
    # Her kategoriden MAX 3 adet en uygun olan verilecek
    if cilt_rengi == "Açık":
        if alt_ton == "Pembe Alt Tonlu":
            recs["fondöten"] = ["FT-01", "FT-02"]
            recs["kapatıcı"] = ["KP-01", "KP-02"]
            recs["allık"], recs["ruj"], recs["far"] = ["AL-01", "AL-02"], ["RJ-01", "RJ-02"], ["FR-01", "FR-02"]
        else:
            recs["fondöten"] = ["FT-02", "FT-03"]
            recs["kapatıcı"] = ["KP-03", "KP-04"]
            recs["allık"], recs["ruj"], recs["far"] = ["AL-10", "AL-14"], ["RJ-14", "RJ-46"], ["FR-04"]
    
    elif cilt_rengi == "Buğday":
        recs["fondöten"] = ["FT-04", "FT-05"]
        recs["kapatıcı"] = ["KP-07", "KP-08"]
        if alt_ton == "Sarı Alt Tonlu": 
            recs["allık"], recs["ruj"], recs["far"] = ["AL-12", "AL-13"], ["RJ-16", "RJ-17"], ["FR-06", "FR-07"]
        else: 
            recs["allık"], recs["ruj"], recs["far"] = ["AL-05", "AL-08"], ["RJ-06", "RJ-13"], ["FR-15"]
    
    elif cilt_rengi == "Esmer":
        recs["fondöten"] = ["FT-07", "FT-08"]
        recs["kapatıcı"] = ["KP-13", "KP-14"]
        if alt_ton == "Sarı Alt Tonlu": 
            recs["allık"], recs["ruj"], recs["far"] = ["AL-16", "AL-17"], ["RJ-26", "RJ-30"], ["FR-10", "FR-12"]
        else: 
            recs["allık"], recs["ruj"], recs["far"] = ["AL-20", "AL-24"], ["RJ-24", "RJ-34"], ["FR-20"]
        
    else:  # Koyu
        recs["fondöten"] = ["FT-10", "FT-11"]
        recs["kapatıcı"] = ["KP-20", "KP-21"]
        recs["allık"], recs["ruj"], recs["far"] = ["AL-20", "AL-24"], ["RJ-24", "RJ-34"], ["FR-20", "FR-22"]
            
    return recs

def categorize_eye_color(iris_hex):
    """Iris hex renginden göz rengi kategorisini döndürür."""
    try:
        h = iris_hex.lstrip('#')
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        # Mavi tonları
        if b > r + 30 and b > g:
            return "mavi"
        # Yeşil tonları
        if g > r + 15 and g > b + 10:
            return "yesil"
        # Koyu kahve / siyah
        if brightness < 60:
            return "koyu_kahve"
        # Açık kahve / ela
        if r > 80 and g > 50 and b < 80:
            return "kahve"
        return "kahve"
    except:
        return "kahve"

import math
def detect_face_shape(landmarks, w, h):
    def dist(lm1, lm2):
        return math.sqrt(((lm1.x - lm2.x)*w)**2 + ((lm1.y - lm2.y)*h)**2)

    length = dist(landmarks[10], landmarks[152]) # forehead to chin
    width = dist(landmarks[234], landmarks[454]) # cheek to cheek
    jaw = dist(landmarks[132], landmarks[361]) # jawline
    forehead = dist(landmarks[21], landmarks[251]) # temples
    
    ratio = length / width if width > 0 else 1.0
    
    if ratio > 1.35:
        if jaw > forehead * 0.9:
            return "Dikdörtgen", "Yüzünüz Dikdörtgen şeklinde. Kontürü alın köklerine ve çene alt köşelerine uygulayarak yüzünüzü daha oval gösterebilirsiniz. Allığı elmacık kemiklerinin üzerine yatay uygulayın."
        else:
            return "Oval", "Yüzünüz Oval şeklinde. Dengeli bir hat. Kontürü sadece elmacık kemiklerinizin hemen altına (şakaklardan yanağa) hafifçe uygulayın. Allığı elmacık kemiklerinize sürün."
    elif forehead > jaw * 1.15:
        return "Kalp", "Yüzünüz Kalp şeklinde. Geniş bir alın ve sivri bir çene hattı. Alın köşelerinize kontür uygulayıp daraltın. Çene ucuna ve çevresine aydınlatıcı sürerek dengeleyin."
    elif width > forehead and width > jaw * 1.1:
        return "Elmas", "Yüzünüz Elmas şeklinde. Elmacık kemikleriniz geniş ve belirgin. Daha yumuşak olması için kontürü elmacık kemiklerinin tepe noktalarına uygulayın, alın ortasını aydınlatın."
    else:
        if jaw > width * 0.85:
            return "Kare", "Yüzünüz Kare şeklinde. Sert hatları yumuşatmak için kontürü çene köşelerinize ve şakaklarınıza yuvarlak oval bir fırçayla uygulayın. Allığı tam yanak ortasına değdirin."
        else:
            return "Yuvarlak", "Yüzünüz Yuvarlak şeklinde. Daha ince kemiksi bir hat yaratmak için kontürü şakaklardan yanak boşluğuna ve çene hattına doğru dikey ilerleterek sürün."

def analyze_skin_endpoint_logic(image_path):
    try:
        frame = cv2.imread(image_path)
        if frame is None: return {"error": "Hata"}
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        if not results.multi_face_landmarks: return {"error": "Yuz bulunamadi"}
        
        h, w, _ = frame.shape
        face_landmarks = results.multi_face_landmarks[0]
        
        shape_name, shape_advice = detect_face_shape(face_landmarks.landmark, w, h)
        
        # Cilt rengi: alın (151) + yanak içleri (205, 425)
        three_points = [151, 205, 425]
        safe_pixels = []
        for idx in three_points:
            cx, cy = int(face_landmarks.landmark[idx].x * w), int(face_landmarks.landmark[idx].y * h)
            roi = frame_rgb[max(0, cy-5):min(h, cy+5), max(0, cx-5):min(w, cx+5)]
            if roi.size > 0: safe_pixels.extend(roi.reshape(-1, 3))
        
        if len(safe_pixels) == 0: raise Exception("No pixels")
            
        r_val, g_val, b_val = np.median(np.array(safe_pixels), axis=0)
        exact_hex = f"#{int(r_val):02x}{int(g_val):02x}{int(b_val):02x}".upper()
        cilt_rengi, alt_ton = calculate_skin_tone_and_undertone((int(b_val), int(g_val), int(r_val)))
        
        # Göz (iris) rengi: sol iris merkezi (468)
        iris_hex = "#4B3621"  # varsayılan koyu kahve
        try:
            iris_lm = face_landmarks.landmark[468]
            ix, iy = int(iris_lm.x * w), int(iris_lm.y * h)
            ip = frame_rgb[max(0,iy-3):min(h,iy+3), max(0,ix-3):min(w,ix+3)]
            if ip.size > 0:
                ir, ig, ib = np.median(ip.reshape(-1,3), axis=0)
                iris_hex = f"#{int(ir):02x}{int(ig):02x}{int(ib):02x}".upper()
        except:
            pass
        eye_category = categorize_eye_color(iris_hex)

        # Saç rengi: alın üstü bölge (üst kafa, landmark 10 biraz yukarısı)
        hair_category = "koyu_kahve"  # varsayılan
        try:
            top_lm = face_landmarks.landmark[10]
            hx, hy = int(top_lm.x * w), int(top_lm.y * h - 30)
            hroi = frame_rgb[max(0,hy-15):max(1,hy), max(0,hx-20):min(w,hx+20)]
            if hroi.size > 0:
                hr, hg, hb = np.median(hroi.reshape(-1,3), axis=0)
                brightness = (hr * 299 + hg * 587 + hb * 114) / 1000
                if brightness > 200:
                    hair_category = "sari"
                elif brightness > 130:
                    hair_category = "kumral"
                elif hr > hb + 20:
                    hair_category = "kizil"
                else:
                    hair_category = "koyu_kahve"
        except:
            pass

        oneriler = get_product_recommendations(cilt_rengi, alt_ton, exact_hex)
        
        all_found = {'FT-01': '#FFF5E8', 'FT-02': '#FFE8D6', 'FT-03': '#F5D6C6', 'FT-04': '#F0D5B8', 'FT-05': '#E8C4A8', 'FT-06': '#E5C9A5', 'FT-07': '#DDB896', 'FT-08': '#D4A574', 'FT-09': '#D2A679', 'FT-10': '#C9A07A', 'FT-11': '#C68E5A', 'FT-12': '#BC8860'}
        all_conc = {'KP-01': '#F4EAE6', 'KP-02': '#F2DFCD', 'KP-03': '#E0C8B0', 'KP-04': '#D2B9A1', 'KP-05': '#CCAF94', 'KP-06': '#C6A587', 'KP-07': '#E5C09B', 'KP-08': '#DEC19F', 'KP-09': '#D4AD86', 'KP-10': '#CCA37A', 'KP-11': '#C4976D', 'KP-12': '#BC8A5E', 'KP-13': '#AF764B', 'KP-14': '#A56D43', 'KP-15': '#9C6239', 'KP-16': '#935831', 'KP-17': '#8A4E29', 'KP-18': '#824622', 'KP-19': '#763C1B', 'KP-20': '#633318', 'KP-21': '#552912', 'KP-22': '#49210E', 'KP-23': '#411C0C', 'KP-24': '#341508', 'KP-25': '#260B03'}
        
        closest_f = [{"hex": all_found.get(c, "#FFFFFF"), "brand": "LuceBella", "product": "Fondöten", "shade": c} for c in oneriler["fondöten"]]
        closest_c = [{"hex": all_conc.get(c, "#FFFFFF"), "brand": "LuceBella", "product": "Kapatıcı", "shade": c} for c in oneriler["kapatıcı"]]
        
        return {
            "hex": exact_hex,
            "undertone": alt_ton,
            "cilt_rengi": cilt_rengi,
            "iris_hex": iris_hex,
            "eye_category": eye_category,
            "hair_category": hair_category,
            "shape": shape_name,
            "advice": f"Cildiniz {cilt_rengi} tonlarında ve {alt_ton}. Gözleriniz {eye_category.replace('_', ' ')} rengi. {shape_advice} Size en uygun makyaj paletini hazırladık.",
            "closest_foundations": closest_f,
            "closest_concealers": closest_c,
            "recommended_makeup": {"blush": oneriler["allık"], "lipstick": oneriler["ruj"], "eyeshadow": oneriler["far"]}
        }
    except Exception as e:
        return {"hex": "#F0D5B8", "undertone": "Nötr", "cilt_rengi": "Buğday", "iris_hex": "#4B3621", "eye_category": "kahve", "hair_category": "koyu_kahve", "shape": "Oval", "advice": f"Hata oluştu: {str(e)}", "closest_foundations": [], "closest_concealers": [], "recommended_makeup": {}}
