# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
from datetime import date

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate
from service.models import Product, Color, Size, Category


class ProductFactory(factory.Factory):
    """Creates fake products that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["cheese", "shorts", "pot", "flowers"])
    category = FuzzyChoice(
        choices=[
            Category.ACCESSORIES,
            Category.BEAUTY,
            Category.FASHION,
            Category.GROCERIES,
        ]
    )
    available = FuzzyChoice(choices=[True, False])
    like = factory.Sequence(lambda n: n)
    color = FuzzyChoice(choices=[Color.BLACK, Color.GREEN, Color.PINK, Color.BLUE])
    size = FuzzyChoice(choices=[Size.XS, Size.S, Size.M, Size.L, Size.XL])
    create_date = FuzzyDate(date(2008, 1, 1))
    last_modify_date = FuzzyDate(date(2009, 2, 2))
