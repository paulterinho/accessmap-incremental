class OSWNormalizer:
    def __init__(self, tags):
        self.tags = tags

    def filter(self):
        return (
            self.is_sidewalk()
            or self.is_crossing()
            or self.is_footway()
            or self.is_road()
        )

    def normalize(self):
        if self.is_sidewalk():
            return self._normalize_sidewalk()
        elif self.is_crossing():
            return self._normalize_crossing()
        elif self.is_footway():
            return self._normalize_footway()
        elif self.is_road():
            return self._normalize_road()
        else:
            raise ValueError("This is an invalid way")

    def _normalize_footway(self):
        new_tags = {
            "highway": "footway",
        }
        if "width" in self.tags:
            try:
                new_tags["width"] = float(self.tags["width"])
            except ValueError:
                pass
        if "incline" in self.tags:
            try:
                new_tags["incline"] = float(self.tags["incline"])
            except ValueError:
                pass

        return new_tags

    def _normalize_sidewalk(self):
        new_tags = self._normalize_footway()
        new_tags["footway"] = "sidewalk"

        return new_tags

    def _normalize_crossing(self):
        new_tags = self._normalize_footway()
        new_tags["footway"] = "crossing"
        if "crossing" in self.tags:
            if self.tags["crossing"] in (
                "marked",
                "uncontrolled",
                "traffic_signals",
                "zebra",
            ):
                new_tags["crossing"] = "marked"
            elif self.tags["crossing"] in "unmarked":
                new_tags["crossing"] = "unmarked"

        return new_tags

    def _normalize_road(self):
        new_tags = {"highway": self.tags["highway"]}
        if "width" in self.tags:
            try:
                new_tags["width"] = float(self.tags["width"])
            except ValueError:
                pass

        return new_tags

    def is_sidewalk(self):
        return (self.tags.get("highway", "") == "footway") and (
            self.tags.get("footway", "") == "sidewalk"
        )

    def is_crossing(self):
        return (self.tags.get("highway", "") == "footway") and (
            self.tags.get("footway", "") == "crossing"
        )

    def is_footway(self):
        return self.tags.get("highway", "") == "footway"

    def is_road(self):
        return self.tags.get("highway", "") in (
            "primary",
            "secondary",
            "tertiary",
            "residential",
            "service",
        )
