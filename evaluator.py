from postprocessing import evaluate_discovery_model

evaluate_discovery_model.main(
    #path_to_data="/data/fabricdata/mitdwh_index_nhrel/balanced_training_data.pklz",
    path_to_data="/data/fabricdata/mitdwh_index_nhrel/training_data.pklz",
    path_to_vocab = "/data/fabricdata/mitdwh_index_nhrel/tf_dictionary.pkl",
    path_to_location = "/data/fabricdata/mitdwh_index_nhrel/",
    path_to_model = "/data/fabricdata/mitdwh_index_nhrel/model.h5epoch-19.hdf5",
    path_to_ae_model = "/data/fabricdata/mitdwh_index_nhrel/ae/",
    path_to_vae_model = "/data/fabricdata/mitdwh_index_nhrel/vae/",
    path_to_fqa_model = "/data/fabricdata/mitdwh_qa/fqa/",
    encoding_mode = "index",
    where_is_fabric = False)
