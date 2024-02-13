import tensorflow as tf


def validate_dataset(filenames, reader_opts=None):
    """
    Attempt to iterate over every record in the supplied iterable of TFRecord filenames
    :param filenames: iterable of filenames to read
    :param reader_opts: (optional) tf.python_io.TFRecordOptions to use when constructing the record iterator
    """
    i = 0
    for fname in filenames:
        print('validating ', fname)

        record_iterator = tf.io.tf_record_iterator(path=fname, options=reader_opts)
        try:
            for _ in record_iterator:
                i += 1
        except Exception as e:
            print('error in {} at record {}'.format(fname, i))
            print(e)

#############################
# The code below here uses the crcmod package to implement an alternative method which is able to print out
# if it finds a bad record and attempt to keep going. If the corruption in your file is just flipped bits this may be helpful.
# If the corruption is added or deleted bytes this will probably crash and burn.

import struct
from crcmod.predefined import mkPredefinedCrcFun

_crc_fn = mkPredefinedCrcFun('crc-32c')


def calc_masked_crc(data):
    crc = _crc_fn(data)
    return (((crc >> 15) | (crc << 17)) + 0xa282ead8) & 0xFFFFFFFF


def validate_dataset_slower(filenames):
    total_records = 0
    total_bad_len_crc = 0
    total_bad_data_crc = 0
    for f_name in filenames:
        i = 0
        print('validating ', f_name)

        with open(f_name, 'rb') as f:

            len_bytes = f.read(8)
            while len(len_bytes) > 0:
                # tfrecord format is a wrapper around protobuf data
                length, = struct.unpack('<Q', len_bytes) # u64: length of the protobuf data (excluding the header)
                len_crc, = struct.unpack('<I', f.read(4)) # u32: masked crc32c of the length bytes
                data = f.read(length) # protobuf data
                data_crc, = struct.unpack('<I', f.read(4)) # u32: masked crc32c of the protobuf data

                if len_crc != calc_masked_crc(len_bytes):
                    print('bad crc on len at record', i)
                    total_bad_len_crc += 1

                if data_crc != calc_masked_crc(data):
                    print('bad crc on data at record', i)
                    total_bad_data_crc += 1

                i += 1
                len_bytes = f.read(8)

        print('checked', i, 'records')
        total_records += i
    print('checked', total_records, 'total records')
    print('total with bad length crc: ', total_bad_len_crc)
    print('total with bad data crc: ', total_bad_data_crc)
    
