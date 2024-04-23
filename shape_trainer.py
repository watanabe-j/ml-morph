# Part of the standard library
import os
import sys
import glob
import argparse
# Not part of the standard library
import dlib

#Parsing arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", type=str, default='train.xml',
    help="training data (default = train.xml)", metavar='')
ap.add_argument("-t", "--test", type=str, default=None,
    help="test data (default = test.xml).if not provided, no testing is done", metavar='')
ap.add_argument("-o", "--out", type=str, default='predictor',
    help="output filename (default = predictor); extention '.dat' is appended unless the value ends with it", metavar='')
ap.add_argument("-th", "--threads", type=int, default=1,
    help="number of threads to be used (default = 1)", metavar='')
ap.add_argument("-dp", "--tree-depth", type=int, default=4,
    help="choice of tree depth (default = 4)", metavar='')
ap.add_argument("-c", "--cascade-depth", type=int, default=15,
    help="choice of cascade depth (default = 15)", metavar='')
ap.add_argument("-nu", "--nu", type=float, default=0.1,
    help="regularization parameter (default = 0.1)", metavar='')
ap.add_argument("-os", "--oversampling", type=int, default=10,
    help="oversampling amount (default = 10)", metavar='')
ap.add_argument("-j", "--jitter", type=float, default=0,
    help="oversampling translation jitter (default = 0)", metavar='')
ap.add_argument("-s", "--test-splits", type=int, default=20,
    help="number of test splits (default = 20)", metavar='')
ap.add_argument("-f", "--feature-pool-size", type=int, default=500,
    help="choice of feature pool size (default = 500)", metavar='')
ap.add_argument("-n", "--num-trees", type=int, default=500,
    help="number of regression trees (default = 500)", metavar='')
ap.add_argument("-l", "--lambda", type=float, default=0.1,
    help="sampling distance parameter (default = 0.1)", metavar='')
ap.add_argument("-rs", "--random-seed", type=str, default="",
    help="random seed (default = \"\")", metavar='')
ap.add_argument("-v", "--verbose", default=True, action = argparse.BooleanOptionalAction,
    help="if True, verbose output is printed (default = True)", metavar='')
args = vars(ap.parse_args())

#Setting up the training parameters
options = dlib.shape_predictor_training_options()
options.num_trees_per_cascade_level=args['num_trees']
options.nu = args['nu']
options.num_threads=args['threads']
options.tree_depth = args['tree_depth']
options.cascade_depth = args['cascade_depth']
options.feature_pool_size = args['feature_pool_size']
options.num_test_splits = args['test_splits']
options.oversampling_amount = args['oversampling']
options.oversampling_translation_jitter = args['jitter']
options.random_seed = args['random_seed']
options.lambda_param = args['lambda']
options.be_verbose = args['verbose']

outfile_name = args['out']
if not outfile_name.endswith('.dat'):
    outfile_name += ".dat"

#Training the model
train_path = os.path.join('./', args['dataset'])
dlib.train_shape_predictor(train_path, outfile_name, options)
print("Training error (average pixel deviation): {}".format(
    dlib.test_shape_predictor(train_path, outfile_name)))

#Testing the model (if test data was provided)
if args['test'] is not None:
    test_path = os.path.join('./', args['test'])
    print("Testing error (average pixel deviation): {}".format(
        dlib.test_shape_predictor(test_path, outfile_name)))