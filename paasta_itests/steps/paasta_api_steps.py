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
from __future__ import absolute_import
from __future__ import unicode_literals

from behave import then
from bravado import exception as bexception

from paasta_tools.utils import decompose_job_id


@then('instance GET should return app_count "{app_count}" and an expected number of running instances for "{job_id}"')
def service_instance_status(context, app_count, job_id):
    (service, instance, _, __) = decompose_job_id(job_id)
    response = context.paasta_api_client.service.status_instance(
        instance=instance,
        service=service
    ).result()

    assert response['marathon']['app_count'] == int(app_count), response
#    assert response['marathon']['running_instance_count'] == response['marathon']['expected_instance_count'], response


@then('instance GET should return error code "{error_code}" for "{job_id}"')
def service_instance_status_error(context, error_code, job_id):
    (service, instance, _, __) = decompose_job_id(job_id)

    response = None
    try:
        response = context.paasta_api_client.service.status_instance(
            instance=instance,
            service=service
        ).result()
    except bexception.HTTPError as exc:
        assert exc.status_code == int(error_code)

    assert not response


@then('resources GET should show "{resource}" has {used:d} used')
def resouces_resource_used(context, resource, used):
    response = context.paasta_api_client.resources.resources().result()
    assert response[0][resource]['used'] == used, response


@then('resources GET with groupings "{groupings}" and filters "{filters}" should return {num:d} groups')
def resources_groupings_filters(context, groupings, filters, num):
    groupings = groupings.split(",")
    if len(filters) > 0:
        filters = filters.split("|")
    response = context.paasta_api_client.resources.resources(groupings=groupings, filter=filters).result()

    assert len(response) == num, response


@then('resources GET with groupings "{groupings}" should return {num:d} groups')
def resourses_groupings(context, groupings, num):
    return resources_groupings_filters(context, groupings, [], num)
