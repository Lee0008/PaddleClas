#copyright (c) 2021 PaddlePaddle Authors. All Rights Reserve.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from paddle import nn
import copy
from collections import OrderedDict

from .metrics import Topk, mAP, mINP, Recallk


class CombinedMetrics(nn.Layer):
    def __init__(self, config_list):
        super().__init__()
        self.metric_func_list = []
        assert isinstance(config_list, list), (
            'operator config should be a list')
        for config in config_list:
            print(config)
            assert isinstance(config,
                              dict) and len(config) == 1, "yaml format error"
            metric_name = list(config)[0]
            metric_params = config[metric_name]
            self.metric_func_list.append(eval(metric_name)(**metric_params))

    def __call__(self,
                 similarities_matrix,
                 query_img_id,
                 gallery_img_id,
                 x=None,
                 label=None):
        metric_dict = OrderedDict()
        for idx, metric_func in enumerate(self.metric_func_list):
            if x is None:
                metric_dict.update(metric_func(x, label))
            else:
                metric_dict.update(
                    metric_func(similarities_matrix, query_img_id,
                                gallery_img_id))
        return metric_dict


def build_metrics(config):
    metrics_list = CombinedMetrics(copy.deepcopy(config))
    return metrics_list
