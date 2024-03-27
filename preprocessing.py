import argparse
import os
import utils


ap = argparse.ArgumentParser()
ap.add_argument('-i','--input-dir', type=str, default='images', help="input directory containing image files (default = images)", metavar='')
ap.add_argument('-c','--csv-file', type=str, default=None, help="(optional) XY coordinate file in csv format", metavar='')
ap.add_argument('-t','--tps-file', type=str, default=None, help="(optional) tps coordinate file", metavar='')
ap.add_argument('-trd','--train-dir', type=str, default='train', help="(optional) output directory name for training data (default = train)", metavar='')
ap.add_argument('-tsd','--test-dir', type=str, default='test', help="(optional) output directory name for test data (default = test)", metavar='')
ap.add_argument('-trx','--train-xml', type=str, default='train.xml', help="(optional) output xml name for training data (default = train.xml)", metavar='')
ap.add_argument('-tsx','--test-xml', type=str, default='test.xml', help="(optional) output xml name for test data (default = test.xml)", metavar='')
ap.add_argument('-r','--replace-dir', type=bool, default=False, help="(optional) determines action when directories specified by --train-dir and --test-dir already exist: when True, existing directories are replaced; when False, existing directories are retained and images are added in them (default = False)", metavar='')


    
args = vars(ap.parse_args())

assert os.path.isdir(args['input_dir']), "Could not find the folder {}".format(args['input_dir'])
    
file_sizes=utils.split_train_test(args['input_dir'], args['train_dir'], args['test_dir'], args['replace_dir'])

if args['csv_file'] is not None:
    dict_csv=utils.read_csv(args['csv_file'])
    utils.generate_dlib_xml(dict_csv,file_sizes['train'],folder=args['train_dir'],out_file=args['train_xml'])
    utils.generate_dlib_xml(dict_csv,file_sizes['test'],folder=args['test_dir'],out_file=args['test_xml'])
    
if args['tps_file'] is not None:
    dict_tps=utils.read_tps(args['tps_file'])
    utils.generate_dlib_xml(dict_tps,file_sizes['train'],folder=args['train_dir'],out_file=args['train_xml'])
    utils.generate_dlib_xml(dict_tps,file_sizes['test'],folder=args['test_dir'],out_file=args['test_xml'])
  