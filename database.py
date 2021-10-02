"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # What additional auxiliary data structures will be useful?
        #
        # Creation of data structures for fast look up of an entry based on...
        # ...designation
        self.designation_index_map = self.create_neo_designation_index_map()
        # ...and name
        self.name_to_index_map = self.create_neo_name_index_map()

        for approach in self._approaches:
            approach_designation = approach._designation
            neo = self.get_neo_by_designation(approach_designation)

            if neo:  # Found correspond neo
                approach.neo = neo
                neo.approaches.append(approach)

    def create_neo_designation_index_map(self):
        """
        Method to create a designation to entry index mapping for neos to enable faster searching due
        to having a mapping where the designation will act as key and the value the index
        into the _neos data list, which can then be looked up
        """

        designation_to_index_map = {}

        for idx, neo in enumerate(self._neos):
            designation_to_index_map[neo.designation] = idx

        return designation_to_index_map

    def create_neo_name_index_map(self):
        """
        Method to create a name to entry index mapping for neos to enable faster searching due
        to having a mapping where the designation will act as key and the value the index
        into the _neos data list, which can then be looked up
        """

        name_to_index_map = {}

        for idx, neo in enumerate(self._neos):
            name_to_index_map[neo.name] = idx

        return name_to_index_map

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """

        data_index = self.designation_index_map.get(designation, None)

        if data_index is not None:
            return self._neos[data_index]
        else:
            return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        data_index = self.name_to_index_map.get(name, None)

        if data_index is not None:
            return self._neos[data_index]
        else:
            return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """

        if len(filters) == 0:
            for approach in self._approaches:
                yield approach

        for approach in self._approaches:
            passes_filter = False
            for filter in filters:
                if filter(approach):
                    passes_filter = True
                    continue
                else:
                    passes_filter = False
                    break

            if passes_filter:
                yield approach
