import json

base_path = '/home/yfliu/DataMining_Workspace/DataMining/CapstoneProject/yelp_dataset_challenge_academic_dataset/task3'
business_file_path = '/home/yfliu/DataMining_Workspace/DataMining/CapstoneProject/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
business_review_file_path = '/home/yfliu/DataMining_Workspace/DataMining/CapstoneProject/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
manual_annotation_task_path = '/home/yfliu/DataMining_Workspace/DataMining/CapstoneProject/yelp_dataset_challenge_academic_dataset/task3/manualAnnotationTask'


def get_target_business_type():
	import os
	result = []

	for (dirpath, dirnames, filenames) in os.walk(manual_annotation_task_path):
		for filename in filenames:
			result.append(filename.split('.')[0])

	return result


def build_business_type_id_map(business_type_list):
	result = {}

	reader = open(business_file_path, 'r')
	line = reader.readline()

	while line:
		json_line = json.loads(line)
		categories = json_line['categories']

		for cat in categories:
			if cat in business_type_list:
				business_id = json_line['business_id']

				if cat not in result:
					result[cat] = set() 

				result[cat].add(business_id)

		line = reader.readline()

	reader.close()
	return result


def included_in_target_business_type(current_id, business_category_id_map):
	for cat in business_category_id_map:
		if current_id in business_category_id_map[cat]:
			return True

	return False


def record_review(business_id_review_map, bus_id, review):
	if bus_id not in business_id_review_map:
		business_id_review_map[bus_id] = []

	business_id_review_map[bus_id].append(review)


def read_review_related_to_business_id(business_category_id_map):
	reader = open(business_review_file_path, 'r')
	business_id_review_map = {}

	line = reader.readline()

	while line:
		json_line = json.loads(line)
		bus_id = json_line['business_id'] 

		if included_in_target_business_type(bus_id, business_category_id_map):
			record_review(business_id_review_map, bus_id, json_line['text'])

		line = reader.readline()

	reader.close()
	return business_id_review_map 


def output_category_review_to_disk(business_category_id_map, business_id_review_map):
	import codecs

	for cat in business_category_id_map:
		reviews = []
		business_ids = business_category_id_map[cat]

		for bus_id in business_ids:
			if bus_id not in business_id_review_map:
				continue 

			reviews += business_id_review_map[bus_id]

		file_name = base_path + '/categoryReviewMap/' + cat + '_reviews.txt'

		with codecs.open(file_name, 'a', encoding='utf-8') as writer:
			writer.write(''.join(reviews))


if __name__ == '__main__':
	target_business_type = get_target_business_type()
	business_category_id_map = build_business_type_id_map(target_business_type)
	business_id_review_map = read_review_related_to_business_id(business_category_id_map)
	output_category_review_to_disk(business_category_id_map, business_id_review_map)
