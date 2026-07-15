import cv2
import numpy as np
import mediapipe as mp
from mediapipe.python.solutions import face_mesh as mp_face_mesh

face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
LIPS_OUTER = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]
LEFT_BROW = [46, 53, 52, 65, 55, 70, 63, 105, 66, 107]
RIGHT_BROW = [276, 283, 282, 295, 285, 300, 293, 334, 296, 336]

LEFT_EYELINER = [33, 246, 161, 160, 159, 158, 157, 173, 133]
RIGHT_EYELINER = [263, 466, 388, 387, 386, 385, 384, 398, 362]
LEFT_EYESHADOW = [226, 247, 30, 29, 27, 28, 56, 190, 243, 173, 157, 158, 159, 160, 161, 246, 33, 130, 226]
RIGHT_EYESHADOW = [463, 414, 286, 258, 257, 259, 260, 467, 446, 359, 263, 466, 388, 387, 386, 385, 384, 398, 362, 463]
LIP_UPPER = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 308, 415, 310, 312, 13, 82, 81, 80, 191, 78]
LIP_LOWER = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 402, 317, 14, 87, 178, 88, 95, 78, 61]

def hex_to_bgr(hex_code):
    try:
        hex_code = hex_code.lstrip('#')
        if len(hex_code) == 8: hex_code = hex_code[2:]
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))[::-1]
    except: return (0, 0, 0)

def apply_makeup(frame, points, color_bgr, alpha=0.5, blur_size=(51, 51)):
    if not points: return frame
    pts = np.array(points, np.int32).reshape((-1, 1, 2))
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)
    mask = cv2.GaussianBlur(mask, blur_size, 0)
    mask_float = np.expand_dims((mask.astype(float) / 255.0) * alpha, axis=-1)
    color_frame = np.empty_like(frame)
    color_frame[:] = color_bgr
    return (frame * (1.0 - mask_float) + color_frame * mask_float).astype(np.uint8)

def apply_full_makeup(image_path, out_path, lip_hex=None, lip_alpha=0.7, blush_hex=None, blush_alpha=0.5, eye_hex=None, eye_alpha=0.6, contour_hex=None, contour_alpha=0.6, concealer_hex=None, concealer_alpha=0.75, eyeliner_hex=None, eyeliner_alpha=0.9, foundation_hex=None, foundation_alpha=0.9, bronzer_hex=None, bronzer_alpha=0.15):
    frame = cv2.imread(image_path)
    if frame is None: return False
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = face_mesh.process(rgb)
    if not res.multi_face_landmarks: return False 
    h, w, _ = frame.shape
    landmarks = {i: (int(lm.x * w), int(lm.y * h)) for i, lm in enumerate(res.multi_face_landmarks[0].landmark)}
    
    # --- GLOBAL EXCLUSION MASK (Gözler, Kaşlar, Dudaklar) ---
    e_mask_f = np.zeros(frame.shape[:2], dtype=float)
    if any([foundation_hex, contour_hex, concealer_hex, blush_hex, bronzer_hex]):
        exclusion_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        exclusion_parts = [LEFT_EYE, RIGHT_EYE, LIPS_OUTER, LEFT_BROW, RIGHT_BROW]
        for part in exclusion_parts:
            pts = np.array([landmarks[i] for i in part if i in landmarks], np.int32).reshape((-1, 1, 2))
            cv2.fillPoly(exclusion_mask, [pts], 255)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        exclusion_mask = cv2.dilate(exclusion_mask, kernel, iterations=1)
        exclusion_mask = cv2.GaussianBlur(exclusion_mask, (21, 21), 0)
        e_mask_f = exclusion_mask.astype(float)/255.0

    if foundation_alpha > 0 and foundation_hex:
        base_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        oval_pts = np.array([landmarks[i] for i in FACE_OVAL if i in landmarks], np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(base_mask, [oval_pts], 255)
        
        # Yüz kenarlarını çok daha yumuşak geçişli yap
        base_mask = cv2.GaussianBlur(base_mask, (91, 91), 0)
        
        # Maskeleri matematiksel (float) olarak çıkarıp clip ile sınırla
        b_mask_f = base_mask.astype(float)/255.0
        final_mask_f = np.clip(b_mask_f - e_mask_f, 0.0, 1.0)
        
        # Alpha'yı fondöten yoğunluğuna göre ayarla (0.6 çarpanı kaldırıldı, tam alpha)
        f_alpha = np.expand_dims(final_mask_f * min(1.0, foundation_alpha), axis=-1)
        
        # 3D GÖLGE VE IŞIĞI KORUYAN PROFESYONEL FONDÖTEN HARMANLAMASI (HSV)
        f_bgr = hex_to_bgr(foundation_hex)
        f_hsv = cv2.cvtColor(np.uint8([[f_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        target_hsv = frame_hsv.copy()
        
        # Cildin Hue (renk tonu) tamamen fondötene eşitlenir
        target_hsv[:,:,0] = f_hsv[0] 
        # Cildin Saturation (canlılık) değeri fondötenle harmanlanır
        target_hsv[:,:,1] = np.clip(target_hsv[:,:,1] * 0.3 + f_hsv[1] * 0.7, 0, 255)
        # Value (Parlaklık/Gölgeler) ASLA DEĞİŞTİRİLMEZ! Bu sayede 3D maske yapay durmaz.
        
        perfect_skin = cv2.cvtColor(target_hsv, cv2.COLOR_HSV2BGR)
        
        # Hafif bir pürüzsüzleştirme (blur) ekleyerek fondöten dokusu ver
        smoothed_skin = cv2.bilateralFilter(perfect_skin, 9, 75, 75)
        perfect_skin = cv2.addWeighted(perfect_skin, 0.5, smoothed_skin, 0.5, 0)
        
        frame = (frame*(1.0-f_alpha) + perfect_skin*f_alpha).astype(np.uint8)

    if contour_hex:
        c_bgr = hex_to_bgr(contour_hex)
        c_m = np.zeros(frame.shape[:2], dtype=np.uint8)
        try:
             l_pts = np.array([landmarks[127], landmarks[147], landmarks[214], landmarks[192]], np.int32)
             cv2.fillPoly(c_m, [l_pts], 255)
             r_pts = np.array([landmarks[356], landmarks[376], landmarks[434], landmarks[416]], np.int32)
             cv2.fillPoly(c_m, [r_pts], 255)
             n_l = np.array([landmarks[190], landmarks[189], landmarks[168], landmarks[6]], np.int32).reshape((-1,1,2))
             cv2.polylines(c_m, [n_l], False, 255, int(w*0.015), cv2.LINE_AA)
             n_r = np.array([landmarks[414], landmarks[413], landmarks[168], landmarks[6]], np.int32).reshape((-1,1,2))
             cv2.polylines(c_m, [n_r], False, 255, int(w*0.015), cv2.LINE_AA)
             c_m = cv2.GaussianBlur(c_m, (151, 151), 0)
             c_mask_f = np.clip((c_m.astype(float)/255.0) - e_mask_f, 0.0, 1.0)
             c_f = np.expand_dims(c_mask_f * contour_alpha, axis=-1)
             cfrm = np.empty_like(frame)
             cfrm[:] = c_bgr
             frame = (frame*(1.0-c_f) + cfrm*c_f).astype(np.uint8)
        except Exception: pass

    if concealer_hex:
         c_bgr = hex_to_bgr(concealer_hex)
         c_m = np.zeros(frame.shape[:2], dtype=np.uint8)
         try:
             # Gözlerin biraz daha aşağısına çekildi ki göze girmesin ve genişlesin (çok abartmadan)
             c_left = (landmarks[119][0], int(landmarks[119][1] + h*0.03))
             c_right = (landmarks[348][0], int(landmarks[348][1] + h*0.03))
             # Yatayda yayılım (genişlik), Dikeyde dar (alta doğru)
             cv2.ellipse(c_m, c_left, (int(w*0.09), int(h*0.04)), 0, 0, 360, 255, -1)
             cv2.ellipse(c_m, c_right, (int(w*0.09), int(h*0.04)), 0, 0, 360, 255, -1)
             c_m = cv2.GaussianBlur(c_m, (71, 71), 0)
             c_mask_f = np.clip((c_m.astype(float)/255.0) - e_mask_f, 0.0, 1.0)
             c_f = np.expand_dims(c_mask_f * concealer_alpha, axis=-1)
             cfrm = np.empty_like(frame)
             cfrm[:] = c_bgr
             frame = (frame * (1.0 - c_f) + cfrm * c_f).astype(np.uint8)
         except Exception: pass

    if eye_hex:
        lp = [landmarks[i] for i in LEFT_EYESHADOW if i in landmarks]
        rp = [landmarks[i] for i in RIGHT_EYESHADOW if i in landmarks]
        frame = apply_makeup(frame, lp, hex_to_bgr(eye_hex), eye_alpha, blur_size=(41, 41))
        frame = apply_makeup(frame, rp, hex_to_bgr(eye_hex), eye_alpha, blur_size=(41, 41))
        
    if eyeliner_hex:
        c_bgr = hex_to_bgr(eyeliner_hex)
        e_m = np.zeros(frame.shape[:2], dtype=np.uint8)
        try:
            l_e = [landmarks[i] for i in LEFT_EYELINER if i in landmarks]
            r_e = [landmarks[i] for i in RIGHT_EYELINER if i in landmarks]
            if l_e and r_e:
                dxl, dyl = landmarks[33][0]-landmarks[246][0], landmarks[33][1]-landmarks[246][1]
                # Uzunluk tatlı ortada tutuldu (2.2)
                l_e.insert(0, (int(landmarks[33][0]+dxl*2.2), int(landmarks[33][1]+dyl*2.2-(h*0.015))))
                dxr, dyr = landmarks[263][0]-landmarks[466][0], landmarks[263][1]-landmarks[466][1]
                r_e.insert(0, (int(landmarks[263][0]+dxr*2.2), int(landmarks[263][1]+dyr*2.2-(h*0.015))))
                
                # Kalınlık eski sağlıklı değerine geri getirildi (0.004)
                thickness = max(1, int(w*0.004))
                cv2.polylines(e_m, [np.array(l_e, np.int32).reshape((-1, 1, 2))], False, 255, thickness, cv2.LINE_AA)
                cv2.polylines(e_m, [np.array(r_e, np.int32).reshape((-1, 1, 2))], False, 255, thickness, cv2.LINE_AA)
                e_m = cv2.GaussianBlur(e_m, (5, 5), 0)
                e_f = np.expand_dims((e_m.astype(float)/255.0)*eyeliner_alpha, axis=-1)
                cfrm = np.empty_like(frame)
                cfrm[:] = c_bgr
                frame = (frame*(1.0-e_f) + cfrm*e_f).astype(np.uint8)
        except Exception: pass

    if blush_hex:
        c_bgr = hex_to_bgr(blush_hex)
        b_m = np.zeros(frame.shape[:2], dtype=np.uint8)
        try:
             cl = (landmarks[205][0], int(landmarks[205][1] - h * 0.02))
             cr = (landmarks[425][0], int(landmarks[425][1] - h * 0.02))
             cv2.ellipse(b_m, cl, (int(w*0.13), int(h*0.06)), 0, 0, 360, 255, -1)
             cv2.ellipse(b_m, cr, (int(w*0.13), int(h*0.06)), 0, 0, 360, 255, -1)
             b_m = cv2.GaussianBlur(b_m, (151, 151), 0)
             b_mask_f = np.clip((b_m.astype(float)/255.0) - e_mask_f, 0.0, 1.0)
             b_f = np.expand_dims(b_mask_f * (blush_alpha * 0.5), axis=-1)
             cfrm = np.empty_like(frame)
             cfrm[:] = c_bgr
             frame = (frame*(1.0-b_f) + cfrm*b_f).astype(np.uint8)
        except Exception: pass

    if bronzer_hex:
        c_bgr = hex_to_bgr(bronzer_hex)
        b_m = np.zeros(frame.shape[:2], dtype=np.uint8)
        try:
             # Şakaklar ve yüzün çok hafif dış kısımları (allıktan bağımsız sıcaklık)
             cl = (landmarks[227][0], landmarks[227][1])
             cr = (landmarks[447][0], landmarks[447][1])
             cv2.ellipse(b_m, cl, (int(w*0.08), int(h*0.12)), 30, 0, 360, 255, -1)
             cv2.ellipse(b_m, cr, (int(w*0.08), int(h*0.12)), -30, 0, 360, 255, -1)
             
             # Alın kenarları / şakak üstü
             cl_t = (landmarks[71][0], landmarks[71][1])
             cr_t = (landmarks[301][0], landmarks[301][1])
             cv2.ellipse(b_m, cl_t, (int(w*0.06), int(h*0.06)), 0, 0, 360, 255, -1)
             cv2.ellipse(b_m, cr_t, (int(w*0.06), int(h*0.06)), 0, 0, 360, 255, -1)

             b_m = cv2.GaussianBlur(b_m, (151, 151), 0)
             b_mask_f = np.clip((b_m.astype(float)/255.0) - e_mask_f, 0.0, 1.0)
             b_f = np.expand_dims(b_mask_f * bronzer_alpha, axis=-1)
             cfrm = np.empty_like(frame)
             cfrm[:] = c_bgr
             frame = (frame*(1.0-b_f) + cfrm*b_f).astype(np.uint8)
        except Exception: pass

    if lip_hex:
        c_bgr = hex_to_bgr(lip_hex)
        up = [landmarks[i] for i in LIP_UPPER if i in landmarks]
        low = [landmarks[i] for i in LIP_LOWER if i in landmarks]
        frame = apply_makeup(frame, up, c_bgr, lip_alpha, blur_size=(11, 11))
        frame = apply_makeup(frame, low, c_bgr, lip_alpha, blur_size=(11, 11))
        
    cv2.imwrite(out_path, frame)
    return True
