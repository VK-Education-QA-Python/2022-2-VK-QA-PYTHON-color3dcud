from dataclasses import dataclass

import faker

faker = faker.Faker()


class Builder:
    @staticmethod
    def segment(name=None, segment_type=None, vk_group_id=None):
        @dataclass
        class Segment:
            name: str
            segment_type: str
            relations: list
            segment_id: None = None

        segment_relations = {
            'vk': [
                {
                    "object_type": "remarketing_vk_group",
                    "params": {
                        "source_id": vk_group_id,
                        "type": "positive"
                    }
                }
            ],
            'games': [
                {
                    "object_type": "remarketing_player",
                    "params": {
                        "type": "positive",
                        "left": 365,
                        "right": 0
                    }
                },
                {
                    "object_type": "remarketing_payer",
                    "params": {
                        "type": "positive",
                        "left": 365,
                        "right": 0
                    }
                }
            ]
        }

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

    @staticmethod
    def campaign(name=None):
        @dataclass
        class Campaign:
            pass
