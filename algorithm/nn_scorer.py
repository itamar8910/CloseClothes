from closest_feat import get_KNN
import json
import argparse

# TODO: this module is not tested

def get_intersection_size(s1, s2):
	return len(set(s1).intersection(s2))


def score(feats_dir, tar_json):
	"""
	gives score to the features in 'feats_dir', based on a target KNN for each sample in 'tar_json'
	tar_json structure: {'k':<K>, 
						'knns':{'sample_name':['samp1',...,'sampK'],
								...
							   }
						}
	"""
	tar_json = json.loads(tar_json)
	K = tar_json['K']
	samples_KNN = tar_json['knns']
	intersections = 0
	total = 0
	for sample in samples_KNN:
		sample_tar_KNN = samples_KNN[sample]
		sample_pred_KNN = get_KNN(feats_dir, sample, k=K)
		intersections += get_intersection_size(sample_pred_KNN, sample_tar_KNN)
		total += K

	return "{0:.2f}".format((intersections / float(total))*100.0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("feats_dir")
	parser.add_argument("json_path")
	args = parser.parse_args()

	print(score(args.feats_dir, args.json_path))