# Upper body bounding box, with heuristic that have to do with face/body proprtions

# requires dlib, https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf
import face_recognition # https://github.com/ageitgey/face_recognition
from PIL import Image, ImageDraw

def face_to_upperbody(img_shape, face_x, face_y, face_w, face_h):
    down_shift = face_h
    WIDTH_SCALE = 3
    HEIGHT_SCALE = 5

    face_center_x = face_x + face_w/2.0
    face_center_y = face_y + face_y/2.0
    body_x = face_center_x - face_w/2.0 * WIDTH_SCALE
    body_y = face_y + face_h

    return (max(0, body_x), max(0, body_y), min(face_w*WIDTH_SCALE,img_shape[1]) , min(face_h*HEIGHT_SCALE, img_shape[0]))

def draw_bboxes(img_path, bboxes):

    pil_image = Image.fromarray( face_recognition.load_image_file(img_path))
    for x,y,width,height in bboxes:
        print("drawing:" ,  x,y,width,height)
        draw = ImageDraw.Draw(pil_image)
        draw.rectangle(((x,y),(x+width,y+height)),outline="black")
    pil_image.show()

def get_upperbody_bbox(img_path, w_face_bbox=False):
    # Load the jpg file into a numpy array
    img1 = face_recognition.load_image_file(img_path)
    return get_uperbody_bbox_from_npy(img1, w_face_bbox=w_face_bbox)

def get_uperbody_bbox_from_npy(img_npy,  w_face_bbox=False ):
    if len(img_npy.shape) == 4:
        img_npy = img_npy[0]
    
   
    from tiny_faces import get_faces
    # face_locations = face_recognition.face_locations(img_npy)
    tmp_locations = get_faces(img_npy)
    face_locations = []
    for loc in tmp_locations:
        face_locations.append([float(loc[0][0]), float(loc[0][1]), float(loc[1][0] - loc[0][0]), float(loc[1][1] - loc[1][0])])

    if len(face_locations) == 0:
        raise Exception("NO FACES DETECTED")
        
    if len(face_locations) > 1:
        print("WARNING: More than one person detected, currently only supoorts one person oer image")
    
    face_location = face_locations[0]
        
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    
    face_bbox = (left, top, right-left, bottom-top) # x y w h
    upperbody_bbox = face_to_upperbody(img_npy.shape, *face_bbox) # x y w h
    if w_face_bbox:
        return face_bbox, upperbody_bbox
    return upperbody_bbox

def draw_upperbody_bbox(img_path):
    face_bbox, upperbody_bbox = get_upperbody_bbox(img_path, w_face_bbox=True)
    draw_bboxes(img_path, [face_bbox, upperbody_bbox])

if __name__ == "__main__":
    import sys
    draw_upperbody_bbox(sys.argv[1])
    exit()
    
