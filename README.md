# ETMap

Geo temporal and spatial visualization of epidemic track. The main contents include Character detection and recognition (based on PaddleOCR), Named entity recognition (based on PaddleNLP), Map display and interaction (based on Leaflet) and Front and end interaction (based on Flask).

## How to use

1. Clone this repo:

      ```shell
      git clone https://github.com/geoyee/ETMap.git
      ```

2.  Install dependencies:

      ```shell
      pip install -r requirements.txt
      ```

3. Start server:

      ```shell
      python demo.py
      ```

      View the demo by navigating to `http://localhost:5000`.

## TODO

- [x] Add OCR.
- [x] Add geocoding.
- [x] Add Map.
- [x] Merge functions and update display.
- [x] Add GCJ02 to WGS84.
- [ ] Add draw lines.
- [ ] Update geo-text-split and place merge.
- [ ] Add about time.
- [ ] Update UI about image input.

## Reference

1. [playing-with-leaflet](https://github.com/geoyee/playing-with-leaflet)
2. [flask-leaflet-demo](https://github.com/adwhit/flask-leaflet-demo)
3. [leaflet-tutorials-interesting](https://github.com/twtrubiks/leaflet-tutorials-interesting)
4. [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.5/doc/doc_en/models_list_en.md)
5. [PaddleNLP](https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md)
