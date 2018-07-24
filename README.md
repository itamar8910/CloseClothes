# CloseClothes
### An application for finding similar clothes from images using deep learning 
![Demo Picture](final_demo.png)

---

## Getting started:
### Requirements:
- python 3.5+
- [dlib](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)
- [Android Studio](https://developer.android.com/studio/) with Kotlin configured

### Setting up:
#### Front end:
Open the `android` directory in Android Studio.
Build and run.
#### Back end:
Run:  
```
python3.5 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py init_db --update_feats -o database/data/*_clean.json # This extracts features from scraped data and will take a while
python main.py server
```
---
## Project structure.
```
    ├── algorithm # All things deep learning
    │   ├── README.md
    │   ├── __init__.py
    │   ├── bbox # Extract upper-body bounding boxes
    │   │   ├── __init__.py
    │   │   ├── bbox_heuristic.py # Upper body bbox from face bbox
    │   │   ├── crop.py # Crop images from bbox
    │   │   ├── draw_bbox_prediction.py # Visualize bbox
    │   ├── classification # Readying the data from DeepFashion for classification training
    │   │   ├── config.py # Constants
    │   │   ├── prepare_json_cats.py # Categorize Deepfashion into labeled categories
    │   │   ├── prepare_json_meta_cats.py # Categorize Deepfashion into upper-body categories
    │   │   ├── resnetimpl.py
    │   │   ├── split_train_test.py
    │   │   └── train_clf.py # Train classifier
    │   ├── extract_color_data_runner.py # Manually extract color data from images
    │   ├── feats # The code to use a trained model to exctract features
    │   │   ├── FeatsExtractor.py # The interface to exctract feats, used by the database
    │   │   ├── __init__.py
    │   │   ├── closest_feat.py
    │   │   ├── extract_feats.py
    │   │   ├── plot_knn.py # [DEPRECATED]: generate html to plot results (see vgg_demo.jpg)
    │   │   ├── resnetimpl.py
    │   │   └── weights # Trained model weights go here
    │   ├── nn_scorer.py # [DEPRECATED]: manually score results
    │   ├── rgb_utils.py # Utils to append color data to the database
    │   └── vgg_finetune # Re-train vgg with transfer-learning
    │       ├── clf_feats_frozen.py
    │       └── features_clf.py
    ├── android # The android App
    ├── database
    │   ├── BaseDB.py # Interface for databases
    │   ├── TinyDB_DB.py # Implementation of BaseDB using TinyDB
    │   ├── data # Cleaned up scraped data
    │   │   ├── castro_clean.json
    │   │   └── hm_clean.json
    │   ├── process_images.py # Pre-processing pipeline
    ├── main.py # Main commands to run the backend
    ├── requirements.txt # Pip package requirements
    ├── scraping # Data scraping from fashion outlets
    │   ├── ScrapeProduct.py # Base interface for scrapers
    │   ├── castro.py # Implementation of ScrapeProduct for castro
    │   ├── clean_castro.py # Script to clean up scraped castro data for indexing
    │   ├── clean_hm.py # Script to clean up scraped castro data for indexing
    │   ├── hm.py # Implementation of ScrapeProduct for h&m
    │   ├── phantomjs # The phantomjs browser driver
    │   ├── utils.py # Html utilities
    ├── server # Backend server that communicates with the Frontend app
    │   └── server_main.py # Implementation of the server using sockets
    ├── tests # Unit tests run with pytest
    ├── tiny_faces # The tiny-faces face recognition model
    └── vgg_demo.jpg
```
---
## Authors 
- Itamar Shenhar github: [itamar8910](www.github.com/itamar8910) - email: itamar8910@gmail.com
- Tomer Keren github: [Tadaboody](www.github.com/Tadaboody) - email: tomer.keren.dev@gmail.com
