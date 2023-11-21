from marshmallow import Schema, fields, validate

class MetricSchema(Schema):
    """
    {
        "key": "tests"
        "value": [10.0]
    }
    """
    key = fields.Str(required=True)
    value = fields.List(fields.Float (required=True))


class MeasureSchema(Schema):
    """
    {
        "key": "passed_tests",
        "metrics": [
            {
                "key": "tests",
                "value": [10.0]
            },
            {
                "key": "test_errors",
                "value": [3.0]
            },
            {
                "key": "test_failures",
                "value": [1.0]
            }
        ]
    }
    """

    key = fields.Str(required=True)
    metrics = fields.List(fields.Nested(MetricSchema), required=True)


class CalculateMeasureSchema(Schema):
    """
    {
        
    "measures": [
            {
                "key": "passed_tests",
                "metrics": [
                    {
                        "key": "tests",
                        "value": 10.0
                    },
                    {
                        "key": "test_errors",
                        "value": 3.0
                    },
                    {
                        "key": "test_failures",
                        "value": 1.0
                    }
                ]
            },
            {
                "key": "test_builds",
                "metrics": [
                    {
                        "key": "param1",
                        "value": 8.0
                    },
                    {
                        "key": "param2",
                        "value": 19.0
                    },
                    {
                        "key": "param3",
                        "value": 4.0
                    }
                ]
            },
    }
    """

    measures = fields.List(fields.Nested(MeasureSchema), required=True)

# ANTIGO
#
# class CalculateMeasureSchema(Schema):
#     """
#     {
#         "measures": [
#             {
#                 "key": "passed_tests",
#                 "parameters": {
#                     "tests": 10,
#                     "test_errors": 3,
#                     "test_failures": 1
#                 }
#             },
#             {
#                 "key": "test_builds",
#                 "parameters": {
#                     "param1": 8,
#                     "param2": 19,
#                     "parma3": 4
#                 }
#             }
#         ]
#     }
#     """
#
#     measures = fields.List(fields.Nested(MeasureSchema), required=True)


class CalculatedSubEntitySchema(Schema):
    key = fields.Str(required=True)
    value = fields.Float(validate=validate.Range(min=0, max=1), required=True)
    weight = fields.Float(validate=validate.Range(min=0, max=100), required=True)


class SubCharacteristicSchema(Schema):
    key = fields.Str(required=True)
    measures = fields.List(fields.Nested(CalculatedSubEntitySchema), required=True)


class CalculateSubCharacteristicSchema(Schema):
    """
    {
        "subcharacteristics": [
            {
                "key": "testing_status",
                "measures": [
                    {
                        "key": "passed_tests",
                        "value": 1.0,
                        "weight": 33,
                    },
                    ...
                ]
            },
            ...
        ]
    }
    """

    subcharacteristics = fields.List(fields.Nested(SubCharacteristicSchema), required=True)


class CharacteristicSchema(Schema):
    key = fields.Str(required=True)
    subcharacteristics = fields.List(fields.Nested(CalculatedSubEntitySchema), required=True)


class CalculateCharacteristicSchema(Schema):
    """
    {
        "characteristics": [
            {
                "key": "reliability",
                "subcharacteristics": [
                    {
                        "key": "testing_status",
                        "value": 1.0,
                        "weight": 50,
                    },
                    ...
                ]
            },
            ...
        ]
    }
    """

    characteristics = fields.List(fields.Nested(CharacteristicSchema), required=True)


class TSQMISchema(Schema):
    key = fields.Str(required=True)
    characteristics = fields.List(fields.Nested(CalculatedSubEntitySchema), required=True)


class CalculateTSQMISchema(Schema):
    """
    {
        "tsqmi": {
            "key": "tsqmi",
            "characteristics": [
                {
                    "key": "reliability",
                    "value": 1.0,
                    "weight": 50,
                },
                ...
            ]
        }
    }
    """

    tsqmi = fields.Nested(TSQMISchema, required=True)


class NonComplexFileDensitySchema(Schema):
    """
    "key": "non_complex_file_density",
    "function": calculate_em1
    """

    complexity = fields.List(fields.Float(required=True))
    functions = fields.List(fields.Float(required=True))


class CommentedFileDensitySchema(Schema):
    """
    "key": "commented_file_density",
    "function": calculate_em2
    """

    comment_lines_density = fields.List(fields.Float(required=True))


class DuplicationAbsenceSchema(Schema):
    """
    "key": "duplication_absense",
    "function": calculate_em3
    """

    duplicated_lines_density = fields.List(fields.Float(required=True))


class PassedTestsSchema(Schema):
    """
    "key": "passed_tests",
    "function": calculate_em4
    """

    tests = fields.List(fields.Float(required=True))
    test_errors = fields.Float(required=True)
    test_failures = fields.Float(required=True)


class TestBuildsSchema(Schema):
    """
    "key": "test_builds",
    "function": calculate_em5
    """

    test_execution_time = fields.List(fields.Float(required=True))
    tests = fields.List(fields.Float(required=True))


class TestCoverageSchema(Schema):
    """
    "key": "test_coverage",
    "function": calculate_em6
    """

    coverage = fields.List(fields.Float(required=True))


class TeamThroughputSchema(Schema):
    """
    "key": "team_throughput",
    "function": calculate_em7
    """

    total_issues = fields.Int(required=True)
    resolved_issues = fields.Int(required=True)
