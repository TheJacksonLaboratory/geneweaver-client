"""Test module for test data access objects.

@see https://neomodel.readthedocs.io/en/latest/getting_started.html
"""

import random
from typing import List

from neomodel import (
    IntegerProperty,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    db,
)


# Some test graph objects
# NOTE: This is not the total structure of the graph.
class GeneticEntity(StructuredNode):
    """Superclass for entities."""

    geneId = StringProperty(required=False)  # noqa: N815
    chr = StringProperty(required=False)
    start = IntegerProperty(required=False)
    end = IntegerProperty(required=False)


class Gene(GeneticEntity):
    """Test only."""

    geneName = StringProperty(required=False)  # noqa: N815
    species = StringProperty(required=False)
    ortholog = RelationshipTo("Gene", "ORTHOLOG")


class Transcript(GeneticEntity):
    """Test only."""

    transcriptId = StringProperty(required=True)  # noqa: N815
    produces = RelationshipTo("Gene", "PRODUCES")


class Variant(GeneticEntity):
    """Test only."""

    rsId = StringProperty(required=True)  # noqa: N815
    eqtl = RelationshipTo("Gene", "EQTL")
    variant_effect = RelationshipTo("Transcript", "VARIANT EFFECT")


class Peak(StructuredNode):
    """Test only."""

    peakId = StringProperty(required=True)  # noqa: N815
    epigenome = StringProperty(required=False)
    tissueDescription = StringProperty(required=False)  # noqa: N815
    featureType = StringProperty(required=False)  # noqa: N815
    start = IntegerProperty(required=False)
    end = IntegerProperty(required=False)
    overlap = RelationshipTo("Variant", "OVERLAP")


class GraphManager:
    """Simple class used to manage graph content during testing.

    Can create and delete nodes and relationships.
    """

    def clear(self) -> None:
        """Clear all."""
        query = "MATCH (n) WITH n DETACH DELETE n"
        db.cypher_query(query)

    def create_orthologs(self, count) -> List:
        """Create test orthologs.

        @param count: number of ortholog connections to create
        @return list of objects and relationships created
        """
        ret = []
        for i in range(count):
            a = self._gene("ENSG", i, "Homo sapiens")
            ret.append(a)
            b = self._gene("ENSMUSG", i, "Mus musculus")
            ret.append(b)

            r = a.ortholog.connect(b)
            ret.append(r)

        return ret

    def _gene(self, prefix, i, species) -> Gene:
        r = Gene()
        r.geneId = "{}TEST{}".format(prefix, i)
        r.geneName = "FOXP2_TEST{}".format(i)
        r.species = species
        r.chr = 1
        r.start = random.randint(0, 10000)
        r.end = random.randint(0, 10000)
        r.save()
        return r

    def create_a_graph(self, count, connect=True) -> List:
        """Create test graph."""
        ret = []
        for i in range(count):
            a = self._gene("ENSG", i, "Homo sapiens")
            ret.append(a)

            b = self._gene("ENSMUSG", i, "Mus musculus")
            ret.append(b)

            if connect:
                h = a.ortholog.connect(b)
                ret.append(h)

            t = Transcript(transcriptId="TRANSTest{}".format(i)).save()
            ret.append(t)

            if connect:
                p = t.produces.connect(a)
                ret.append(p)

            v = Variant(rsId="TESTRS{}".format(i)).save()
            ret.append(v)

            if connect:
                ve = v.variant_effect.connect(t)
                ret.append(ve)

                eqtl = v.eqtl.connect(a)
                ret.append(eqtl)

            p = Peak(peakId="Peak{}".format(i)).save()
            ret.append(p)

            if connect:
                o = p.overlap.connect(v)
                ret.append(o)

        return ret
