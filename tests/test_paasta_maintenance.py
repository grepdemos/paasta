# Copyright 2015-2016 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import mock

from paasta_tools import paasta_maintenance


@mock.patch("paasta_tools.mesos_maintenance.is_host_drained", autospec=True)
@mock.patch(
    "paasta_tools.mesos_maintenance.get_hosts_past_maintenance_start", autospec=True
)
def test_is_safe_to_kill(mock_get_hosts_past_maintenance_start, mock_is_host_drained):
    mock_is_host_drained.return_value = False
    mock_get_hosts_past_maintenance_start.return_value = []
    assert not paasta_maintenance.is_safe_to_kill("blah")

    mock_is_host_drained.return_value = False
    mock_get_hosts_past_maintenance_start.return_value = ["blah"]
    assert paasta_maintenance.is_safe_to_kill("blah")

    mock_is_host_drained.return_value = True
    mock_get_hosts_past_maintenance_start.return_value = ["blah"]
    assert paasta_maintenance.is_safe_to_kill("blah")

    mock_is_host_drained.return_value = True
    mock_get_hosts_past_maintenance_start.return_value = []
    assert paasta_maintenance.is_safe_to_kill("blah")
