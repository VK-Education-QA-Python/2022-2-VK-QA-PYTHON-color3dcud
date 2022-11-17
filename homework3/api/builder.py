from dataclasses import dataclass

import faker

from static.default_urls import *
from static.segment_relations import SegmentRelations

faker = faker.Faker()


class Builder:
    @staticmethod
    def group(url=None):
        @dataclass
        class Group:
            group_url: str
            group_id: None = None
            group_id_list: None = None

        if url is None:
            url = DEFAULT_VK_GROUP_URL

        return Group(group_url=url)

    @staticmethod
    def segment(name=None, segment_type=None, vk_group_id=None):
        @dataclass
        class Segment:
            name: str
            segment_type: str
            relations: list
            segment_id: None = None

        segment_relations = SegmentRelations.relations(vk_group_id=vk_group_id)

        relations = []

        if segment_type in segment_relations:
            for i in range(len(segment_relations[segment_type])):
                relations.append(segment_relations[segment_type][i])
        else:
            segment_type = 'games'
            for i in range(len(segment_relations[segment_type])):
                relations.append(segment_relations[segment_type][i])

        if name is None:
            name = faker.bothify(f'{segment_type} from API test id = ?#?#?#?#?#?#?#?#?##?#?#?#?#?#?#?#?#')

        return Segment(name=name, segment_type=segment_type, relations=relations)
