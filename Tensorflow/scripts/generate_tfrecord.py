""" Sample TensorFlow XML-to-TFRecord converter

usage: generate_tfrecord.py [-h] [-x XML_DIR] [-l LABELS_PATH] [-o OUTPUT_PATH] [-i IMAGE_DIR] [-c CSV_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -x XML_DIR, --xml_dir XML_DIR
                        Path to the folder where the input .xml files are stored.
  -l LABELS_PATH, --labels_path LABELS_PATH
                        Path to the labels (.pbtxt) file.
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path of output TFRecord (.record) file.
  -i IMAGE_DIR, --image_dir IMAGE_DIR
                        Path to the folder where the input image files are stored. Defaults to the same directory as XML_DIR.
  -c CSV_PATH, --csv_path CSV_PATH
                        Path of output .csv file. If none provided, then no file will be written.
"""

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse
import tensorflow as tf
from PIL import Image
import io  # Import the standard io module

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Argument parser
parser = argparse.ArgumentParser(description="Sample TensorFlow XML-to-TFRecord converter")
parser.add_argument("-x", "--xml_dir", help="Path to the folder where the input .xml files are stored.", type=str)
parser.add_argument("-l", "--labels_path", help="Path to the labels (.pbtxt) file.", type=str)
parser.add_argument("-o", "--output_path", help="Path of output TFRecord (.record) file.", type=str)
parser.add_argument("-i", "--image_dir", help="Path to the folder where the input image files are stored. Defaults to the same directory as XML_DIR.", type=str, default=None)
parser.add_argument("-c", "--csv_path", help="Path of output .csv file. If none provided, then no file will be written.", type=str, default=None)

args = parser.parse_args()

if args.image_dir is None:
    args.image_dir = args.xml_dir

def parse_label_map(label_map_path):
    label_map = {}
    with open(label_map_path, 'r') as file:
        for line in file:
            if "id" in line:
                id = int(line.split(":")[1].strip())
            if "name" in line:
                name = line.split(":")[1].strip().replace("\"", "")
                label_map[name] = id
    return label_map

label_map_dict = parse_label_map(args.labels_path)

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (
                root.find('filename').text,
                int(root.find('size')[0].text),
                int(root.find('size')[1].text),
                member[0].text,
                int(member[4][0].text),
                int(member[4][1].text),
                int(member[4][2].text),
                int(member[4][3].text)
            )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def create_tf_example(row, image_dir):
    filename = row['filename']
    img_path = os.path.join(image_dir, filename)
    with tf.io.gfile.GFile(img_path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)  # Use standard io.BytesIO
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = filename.encode('utf8')
    image_format = b'jpg'
    xmins = [row['xmin'] / width]
    xmaxs = [row['xmax'] / width]
    ymins = [row['ymin'] / height]
    ymaxs = [row['ymax'] / height]
    classes_text = [row['class'].encode('utf8')]
    classes = [label_map_dict[row['class']]]

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': tf.train.Feature(int64_list=tf.train.Int64List(value=[height])),
        'image/width': tf.train.Feature(int64_list=tf.train.Int64List(value=[width])),
        'image/filename': tf.train.Feature(bytes_list=tf.train.BytesList(value=[filename])),
        'image/source_id': tf.train.Feature(bytes_list=tf.train.BytesList(value=[filename])),
        'image/encoded': tf.train.Feature(bytes_list=tf.train.BytesList(value=[encoded_jpg])),
        'image/format': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_format])),
        'image/object/bbox/xmin': tf.train.Feature(float_list=tf.train.FloatList(value=xmins)),
        'image/object/bbox/xmax': tf.train.Feature(float_list=tf.train.FloatList(value=xmaxs)),
        'image/object/bbox/ymin': tf.train.Feature(float_list=tf.train.FloatList(value=ymins)),
        'image/object/bbox/ymax': tf.train.Feature(float_list=tf.train.FloatList(value=ymaxs)),
        'image/object/class/text': tf.train.Feature(bytes_list=tf.train.BytesList(value=classes_text)),
        'image/object/class/label': tf.train.Feature(int64_list=tf.train.Int64List(value=classes)),
    }))
    return tf_example

def main():
    # Convert XML files to a CSV
    xml_df = xml_to_csv(args.xml_dir)
    if args.csv_path:
        xml_df.to_csv(args.csv_path, index=False)
        print(f'Successfully created the CSV file: {args.csv_path}')

    # Write TFRecord examples to file
    with tf.io.TFRecordWriter(args.output_path) as writer:
        for _, row in xml_df.iterrows():
            tf_example = create_tf_example(row, args.image_dir)
            writer.write(tf_example.SerializeToString())
    print(f'Successfully created the TFRecord file: {args.output_path}')

if __name__ == '__main__':
    main()

