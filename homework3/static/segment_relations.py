class SegmentRelations:
    @staticmethod
    def relations(vk_group_id=None):

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
        return segment_relations
