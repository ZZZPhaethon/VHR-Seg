## Get start

For an overview of VHRseg's commands:

```shell
cd <repository> # replace <repository> with the path you cloned the repository to
python vhrsegment/cli.py
```

Help messages are also available for individual tasks, e.g.:

```shell
python vhrsegment/cli.py train -h
```

## Full Pipeline

The simplest way to use VHR-Seg is by running the entire pipeline.
Open a terminal and run the command below (replace `output_dir` with a path
where you would like to store the results):

```shell
python vhrsegment/cli.py pipeline output_dir
```

vhrsegment will ask for the required inputs, and then proceed to automatically build the dataset and train the chosen model. At the end, predictions can be made on a new dataset. Finished `pipeline`s can be re-run anytime to use the trained model for
making predictions on new data.

## Building a dataset

VHR-Seg supports building labeled and unlabeled datasets.
Unlabeled datasets can be used in combination with a trained model
to make predictions. Labeled datasets can additionally be used to train a model.

### Unlabeled dataset

To create an unlabeled dataset, only an input image is required
(all common image formats are supported). Run the following command to begin:

```shell
python vhrsegment/cli.py unlabeled-dataset output_dir
```

**Example of creating an unlabeled dataset** Example of creating an unlabeled dataset

Note: Square brackets `[...]` indicate a default option. Pressing `ENTER` will
choose the default, which can be seen in the example below.

```shell
$ python vhrsegment/cli.py unlabeled-dataset output_dir
VHR-Seg 1.0.0 

Initializing ...
Creating new UnlabeledDatasetTask ...

Please specify the tile size for input splitting:
Tile width [512]: 
Tile height [512]: 
Path to orthomosaic (input image): ../tests/data/mock_build_dataset_inputs/image.tif

Splitting data into tiles: 100%|██████████| 60/60 [00:01<00:00, 59.61it/s]
Task completed!
```

### Labeled dataset

To create a labeled dataset, a label map is required in addition to the input
image. The label map can be a single-channel (grayscale) 8-bit image where each
pixel's value gives the class of the corresponding pixel in the input image.
Or it can be a vector file, such as a `.shp` or `.geojson` file.

**Example of creating a labeled dataset** Example of creating a labeled dataset, run the following command to begin:

```shell
python vhrsegment/cli.py labeled-dataset output_dir
```

```shell
$ python vhrsegment/cli.py labeled-dataset output_dir
VHR-Seg 1.0.0 

Initializing ...
Creating new DatasetTask ...

Please specify the tile size for input splitting:
Tile width [512]: 
Tile height [512]: 
Path to orthomosaic (input image): .../tests/data/mock_build_dataset_inputs/image.tif
Path to label map: .../tests/data/mock_build_dataset_inputs/label_map.tif
Please now provide pixel values in the label map to class names.
Note that the value 0 is reserved for the background class.

Current summary:
background: 0

Enter the name of a class: banana

Current summary:
background: 0
banana: 1

Enter the name of a class or press ENTER to finish (type u then ENTER to undo the last entry): palmtree

Current summary:
background: 0
banana: 1
palmtree: 2

Enter the name of a class or press ENTER to finish (type u then ENTER to undo the last entry): 

Splitting data into tiles: 100%|██████████| 60/60 [00:01<00:00, 59.63it/s]

Calculating dataset distribution: 100%|██████████| 41/41 [00:00<00:00, 151.51it/s]

Calculating sample weights: 100%|██████████| 41/41 [00:00<00:00, 852.43it/s]

Palettizing labels: 100%|██████████| 41/41 [00:00<00:00, 469.27it/s]
Task completed!
```

### Using CVAT to create a labeled dataset

VHR-Seg integrates with [CVAT](https://cvat.ai)(Computer Vision Annotation Tool) to help you annotate datasets quickly.
CVAT utilizes deep learning models to semi-automatically label the images you upload. This means only a few clicks are required to obtain nearly perfect segmentation masks in most cases!

You can follow the [Labeling tutorials](labeling.md),
or use the description below to get started.

Run the following command to begin:

```shell
python vhrsegment/cli.py labeled-dataset output_dir --with-cvat
```

VHR-Seg will ask for an input image and split it into tiles. This is necessary because CVAT doesn't support annotating huge images
directly. After uploading the tiles to CVAT and annotating them, export the annotations in 'Cityscapes 1.0' format. The resulting `.zip` file is then fed to VHR-Seg, and a labeled dataset will be created from which a model can be trained!


**Example of creating a labeled dataset with CVAT**

```shell
VHR-Seg  1.0.0 

Initializing ...
Creating new UnlabeledDatasetTask ...

Please specify the tile size for input splitting:
Tile width [512]: 
Tile height [512]: 
Path to orthomosaic (input image): .../tests/data/mock_build_dataset_inputs/image.tif

Splitting data into tiles: 100%|██████████| 60/60 [00:01<00:00, 59.69it/s]

The image has been split, tiles are located in: ../output_dir/image_tiles
Please now visit https://cvat.ai to upload the tiles and label them
N.B.: When downloading the labels, choose the 'Cityscapes 1.0' format
Press any key to continue: 

Please now provide the mapping of pixel values in the label map to class names.
Note that the value 0 is reserved for the background class.

Current summary:
background: 0

Enter the name of a class: banana

Current summary:
background: 0
banana: 1

Enter the name of a class or press ENTER to finish (type u then ENTER to undo the last entry): 

Path to zip file downloaded from CVAT: .../tests/data/mock_build_dataset_inputs/cvat.zip

Calculating dataset distribution: 100%|██████████| 41/41 [00:00<00:00, 191.69it/s]

Calculating sample weights: 100%|██████████| 41/41 [00:00<00:00, 2622.24it/s]

Palettizing labels: 100%|██████████| 41/41 [00:00<00:00, 1132.21it/s]
Task completed!
```

## Model Training

To train a model, you will first need to create a labeled dataset (see above).
Then, run the following command to begin:

```shell
python vhrsegment/cli.py train model
```

**Example of training a model on a dataset**

```shell
$ python vhrsegment/cli.py train model

VHR-Seg 1.0.0 

Initializing ...
Creating new TrainTask ...

Path to dataset: my_dataset
Would you like to provide separate datasets for validation and testing? (y/N) n # can also press ENTER here for default N (no) option
Calculating train/val/test split ...

No GPUs available, using CPU
Batch size [2]: 1
Number of epochs (training iterations over entire train set) [50]: 1
Learning rate [0.0001]: 

Please choose a model for training:
1. Mask2Former
Choice: 1

Please choose a variant for this model:
1. mask2former_r50_8xb2-90k_cityscapes-512x1024
        Training Data:  Cityscapes
        Architecture:   ['R-50-D32', 'Mask2Former']
        Memory (GB):    5.67

2. mask2former_r101_8xb2-90k_cityscapes-512x1024
        Training Data:  Cityscapes
        Architecture:   ['R-101-D32', 'Mask2Former']
        Memory (GB):    6.81

3. mask2former_swin-t_8xb2-90k_cityscapes-512x1024
        Training Data:  Cityscapes
        Architecture:   ['Swin-T', 'Mask2Former']
        Memory (GB):    6.36

Press ENTER to see more options, or type your choice: 

4. mask2former_swin-s_8xb2-90k_cityscapes-512x1024
        Training Data:  Cityscapes
        Architecture:   ['Swin-S', 'Mask2Former']
        Memory (GB):    8.09

5. mask2former_swin-b-in22k-384x384-pre_8xb2-90k_cityscapes-512x1024
        Training Data:  Cityscapes
        Architecture:   ['Swin-B', 'Mask2Former']
        Memory (GB):    10.89

6. mask2former_swin-l-in22k-384x384-pre_8xb2-90k_cityscapes-512x1024
        Training Data:  Cityscapes
        Architecture:   ['Swin-L', 'Mask2Former']
        Memory (GB):    15.83

Press ENTER to see more options, or type your choice: 3
Downloading model files ...

processing mask2former_swin-s_8xb2-90k_cityscapes-512x1024...
downloading ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 312.1/312.1 MiB 11.9 MB/s eta 0:00:00
Successfully downloaded mask2former_swin-s_8xb2-90k_cityscapes-512x1024_20221127_143802-9ab177f6.pth to /home/yc5224/Desktop/vhrsegment/model/model_working_dir
Successfully dumped mask2former_swin-s_8xb2-90k_cityscapes-512x1024.py to /home/yc5224/Desktop/vhrsegment/model/model_working_dir
Model files downloaded

Launching model training ...
-- Truncated MMSegmentation training log --

Launching model evaluation ...
-- Truncated MMSegmentation evaluation log --

Task completed!
```

Note: It is possible to provide separate datasets for training, validation, and testing.
The only restriction is that all datasets must use the same label legend and tile dimensions.

### Tile Scaling

The `SCALE` and `SCALE_METHOD` environment variables can be set to replicate
the resolution study in the paper. `SCALE` must be a value between 0 and 1, and
`SCALE_METHOD` can be either 1 or 2, where 1 and 2 correspond to scale methods A
and B, respectively.

**Example using scale method B (pixelation) and a scale factor of 0.5**

```shell
$ SCALE_METHOD=2 SCALE=0.5 python vhrsegment/cli.py train output_dir
```

When a model is trained with scaling, the scaling will be remembered for other tasks, such as the `PredictTask`, so that the final model outputs are rescaled to match the input image size.

## Making Predictions

To make predictions, a (partially) trained model and a labeled or unlabeled
dataset Task are required.
A model can be applied to any dataset to make predictions, as long as the tile
dimensions of the dataset match the tile dimensions of the dataset used during
model training.

**Example of making predictions with a trained model**

```shell
VHR-Seg 1.0.0

Initializing ...
Creating new PredictTask ...

Path to trained model: model
Path to dataset: my_dataset

Launching model training ...
-- Truncated MMSegmentation inference log --

Merging predictions into segmentation map: 100%|██████████| 60/60 [00:00<00:00, 1310.34it/s]
The final segmentation map has been written to: /home/yc5224/Desktop/vhrsegment/my_predictions/segmentation_map_Aug_25_2025-11_48_54.tif
Task completed!
```