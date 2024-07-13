import tensorflow as tf

def validate_tfrecords(filenames):
    """
    Validate TFRecord files by iterating over their contents using TensorFlow's tf.data API.
    
    :param filenames: List of filenames to read
    """
    total_records = 0
    for fname in filenames:
        print('Validating', fname)
        try:
            raw_dataset = tf.data.TFRecordDataset(fname)
            for record in raw_dataset:
                total_records += 1
        except Exception as e:
            print(f'Error in {fname}: {e}')
            continue
        print(f'Checked {total_records} records in {fname}')
    print(f'Total records checked: {total_records}')

def validate_tfrecord_crc(filenames):
    """
    Validate TFRecord files at a lower level by checking CRCs.
    
    :param filenames: List of filenames to read
    """
    import struct
    from crcmod.predefined import mkPredefinedCrcFun

    crc_fn = mkPredefinedCrcFun('crc-32c')

    def calc_masked_crc(data):
        crc = crc_fn(data)
        return (((crc >> 15) | (crc << 17)) + 0xa282ead8) & 0xFFFFFFFF

    total_records = 0
    total_bad_len_crc = 0
    total_bad_data_crc = 0

    for fname in filenames:
        print('Validating', fname)
        with open(fname, 'rb') as f:
            i = 0
            while True:
                len_bytes = f.read(8)
                if len(len_bytes) == 0:
                    break

                length, = struct.unpack('<Q', len_bytes)
                len_crc, = struct.unpack('<I', f.read(4))
                data = f.read(length)
                data_crc, = struct.unpack('<I', f.read(4))

                if len_crc != calc_masked_crc(len_bytes):
                    print(f'Bad CRC on length at record {i} in {fname}')
                    total_bad_len_crc += 1

                if data_crc != calc_masked_crc(data):
                    print(f'Bad CRC on data at record {i} in {fname}')
                    total_bad_data_crc += 1

                i += 1
                total_records += 1
        print(f'Checked {i} records in {fname}')

    print(f'Total records checked: {total_records}')
    print(f'Total records with bad length CRC: {total_bad_len_crc}')
    print(f'Total records with bad data CRC: {total_bad_data_crc}')


