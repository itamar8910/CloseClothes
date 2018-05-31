from tiny_faces import get_faces
import pytest
import imageio

@pytest.fixture(scope="session")
def tiny_face_image():
    test_image_url = "http://newsimg.bbc.co.uk/media/images/47167000/jpg/_47167695_faces_jun_466.jpg"
    return imageio.imread(test_image_url)

@pytest.fixture(scope="session")
def tiny_faces_bboxes(tiny_face_image):
    return get_faces(tiny_face_image)

def test_bbox(tiny_faces_bboxes):
    assert len(tiny_faces_bboxes) > 0
    assert all(len(bbox) == 2 for bbox in tiny_faces_bboxes)
    def is_legal_bbox(bbox:list) -> bool:
        upper_left , down_right = bbox
        return all(upper_cord < lower_cord for upper_cord,lower_cord in zip(upper_left,down_right))
    assert all([is_legal_bbox(bbox) for bbox  in tiny_faces_bboxes])
    
