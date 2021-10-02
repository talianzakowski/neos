"""
Mapping of data file column names to constants allowing singular
upgrade should the data column names change in future. This also
provides greater readability of corresponding code.
"""

NEO_ID_FIELD = "id"
NEO_PRIMARY_DESIGNATION_FIELD = "pdes"
NEO_NAME_FIELD = "name"
NEO_DIAMETER_FIELD = "diameter"
NEO_HAZARD_FIELD = "pha"

CA_PRIMARY_DESIGNATION_FIELD = "des"
CA_ORBIT_ID = "orbit_id"
CA_ID = "id"
CA_TIME_OF_CLOSE_APPROACH_JD = "jd"
CA_TIME_OF_CLOSE_APPROACH_CD_FORMATTED = "cd"
CA_APPROACH_DISTANCE_AU = "dist"
CA_APPROACH_DISTANCE_MIN_AU = "dist_min"
CA_APPROACH_DISTANCE_MAX_AU = "dist_max"
CA_RELATIVE_VELOCITY_TO_APPROACH_BODY_KMS = "v_rel"
CA_RELATIVE_VELOCITY_TO_MASSLESS_BODY_KMS = "v_inf"
CA_THREE_SIGMA_TIME_UNCERTAINTY = "t_sigma_f"
CA_ABSOLUTE_MAGNITUDE = "h"
