class Config(object):
    env = 'default'
    backbone = 'resnet18'
    classify = 'softmax'
    num_classes = 96
    metric = 'arc_margin'
    easy_margin = False
    use_se = False
    loss = 'focal_loss'

    display = False
    finetune = False

    train_root = 'data_lfw_tiny'
    train_list = 'train_data_generated.txt'
    val_list = 'val_data_generated.txt'

    test_root = '/data1/Datasets/anti-spoofing/test/data_align_256'
    test_list = 'test.txt'

    lfw_root = "data_lfw_tiny"
    lfw_test_list = "lfw_test_pair.txt"

    checkpoints_path = 'checkpoints'
    load_model_path = None
    test_model_path = None
    save_interval = 10

    train_batch_size = 8  # batch size
    test_batch_size = 16

    input_shape = (3, 128, 128)

    optimizer = 'sgd'

    use_gpu = True  # use GPU or not
    gpu_id = '0'
    num_workers = 2  # how many workers for loading data
    print_freq = 10  # print info every N batch

    debug_file = '/tmp/debug'  # if os.path.exists(debug_file): enter ipdb
    result_file = 'result.csv'

    max_epoch = 5
    lr = 0.01  # initial learning rate
    lr_step = 2
    lr_decay = 0.9  # when val_loss increase, lr = lr*lr_decay
    weight_decay = 5e-4
