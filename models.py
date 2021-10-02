"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

"""
from helpers import cd_to_datetime, datetime_to_str
from constants import (
    CA_ABSOLUTE_MAGNITUDE,
    CA_APPROACH_DISTANCE_AU,
    CA_APPROACH_DISTANCE_MAX_AU,
    CA_APPROACH_DISTANCE_MIN_AU,
    CA_ORBIT_ID,
    CA_PRIMARY_DESIGNATION_FIELD,
    CA_RELATIVE_VELOCITY_TO_APPROACH_BODY_KMS,
    CA_RELATIVE_VELOCITY_TO_MASSLESS_BODY_KMS,
    CA_THREE_SIGMA_TIME_UNCERTAINTY,
    CA_TIME_OF_CLOSE_APPROACH_CD_FORMATTED,
    CA_TIME_OF_CLOSE_APPROACH_JD,
    NEO_DIAMETER_FIELD,
    NEO_ID_FIELD,
    NEO_NAME_FIELD,
    NEO_PRIMARY_DESIGNATION_FIELD,
    NEO_HAZARD_FIELD,
)


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    # Q: How can you, and should you, change the arguments to this constructor?
    #    If you make changes, be sure to update the comments in this file.
    #
    # A: Yes, I changed the signature to make the class more testable.

    def __init__(self, zipped_item):
        """Create a new `NearEarthObject`.

        :param info: A zip object of data values [0] and respective column names [1]
        """
        self.hazardous = False
        for item in zipped_item:
            data = item[0]
            field = item[1]

            if field == NEO_ID_FIELD:
                self.id = data
            elif field == NEO_PRIMARY_DESIGNATION_FIELD:
                self.designation = data
            elif field == NEO_NAME_FIELD:
                name = data
                formatted_name = self.neaten_name(name)
                if (
                    len(formatted_name) == 0
                ):  # Ensure empty string is represented by None
                    formatted_name = None
                self.name = formatted_name
            elif field == NEO_DIAMETER_FIELD:
                diameter = data
                if len(diameter) == 0:
                    diameter = float("nan")
                self.diameter = float(diameter)
            elif field == NEO_HAZARD_FIELD:
                hazardous = data

                if hazardous.upper() == "Y":
                    self.hazardous = True
                else:
                    self.hazardous - False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    def neaten_name(self, name):
        """Remove spurious characters from name."""
        first = name.lstrip('"')
        second = first.rstrip('"')
        third = second.lstrip()
        fourth = third.rstrip()

        return fourth

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self.designation + "::" + self.name

    def __str__(self):
        """Return `str(self)`."""
        return f"NEO: Name: {self.name} Designation: {self.designation} \
                 Diameter: {self.diameter} Hazardous: {self.hazardous}"

    def __repr__(self):
        """Return `repr(self)`.

        A computer-readable string representation of this object.
        """
        return (
            f"NearEarthObject(designation={self.designation!r},  \
              name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )

    def serialize(self):
        """Create a dictionary representing the NEO in terms of required data.

        Return a map of relevant data items for the output CSV and JSON

        :return Map of this NEO coerced into strings
        """
        results = {}

        results["designation"] = str(self.designation)
        results["name"] = str(self.name)
        results["diameter_km"] = str(self.diameter)
        results["potentially_hazardous"] = str(self.hazardous)

        return results


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, close_approach):
        """Create a new `CloseApproach`.

        :param info: A zipped data, header iterable representing a JSON close approach
        """
        self.magnitude = 0.0

        for pair in close_approach:
            data = pair[0]
            header = pair[1]

            if header == CA_PRIMARY_DESIGNATION_FIELD:
                self._designation = data
            elif header == CA_ORBIT_ID:
                self.orbit_id = data
            elif header == CA_TIME_OF_CLOSE_APPROACH_JD:
                self.jd_time = float(data)
            elif header == CA_TIME_OF_CLOSE_APPROACH_CD_FORMATTED:
                self.time = cd_to_datetime(data)
            elif header == CA_APPROACH_DISTANCE_AU:
                self.distance = float(data)
            elif header == CA_APPROACH_DISTANCE_MIN_AU:
                self.approach_distance_min = float(data)
            elif header == CA_APPROACH_DISTANCE_MAX_AU:
                if data is None or len(data) == 0:
                    data = 0.0
                self.approach_distance_max = float(data)
            elif header == CA_RELATIVE_VELOCITY_TO_APPROACH_BODY_KMS:
                if data is None or len(data) == 0:
                    data = 0.0
                self.velocity = float(data)
            elif header == CA_RELATIVE_VELOCITY_TO_MASSLESS_BODY_KMS:
                if data is None or len(data) == 0:
                    data = 0.0
                self.velocity_to_massless_body = float(data)
            elif header == CA_THREE_SIGMA_TIME_UNCERTAINTY:
                self.time_uncertainty = data
            elif header == CA_ABSOLUTE_MAGNITUDE:
                if data is not None:
                    self.magnitude == float(data)
                else:
                    self.magnitude = 0.0

        # Ensure velocity is always populated!
        if not hasattr(self, "velocity"):
            self.velocity = float(0.0)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"CloseApproach Velocity: {self.velocity} km/h Distance: {self.distance} AUs {self.time_str} NEO: {self.neo}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r},\
                            distance={self.distance:.2f}, "\
                            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )

    def serialize(self):
        """Return a dictionary representation of the Close Approach."""
        approach = {}

        approach["datetime_utc"] = datetime_to_str(self.time)
        approach["distance_au"] = self.distance
        approach["velocity_km_s"] = self.velocity
        approach["designation"] = self._designation

        if self.neo:
            approach["neo"] = self.neo
            approach["name"] = self.neo.name
            if hasattr(self.neo, "name") and self.neo.name is not None:
                approach["name"] = self.neo.name
            else:
                approach["name"] = ""
        else:
            approach["name"] = ""

        if self.neo:
            approach["diameter"] = self.neo.diameter
        else:
            approach["diameter"] = "nan"

        if self.neo:
            approach["hazardous"] = str(self.neo.hazardous)
        else:
            approach["hazardous"] = "False"

        return approach
