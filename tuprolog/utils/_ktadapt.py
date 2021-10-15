from tuprolog import logger
import jpype


@jpype.JImplementationFor("it.unibo.tuprolog.utils.Taggable")
class _KtTaggable:
    def __jclass_init__(cls):
        pass

    @property
    def tags(self):
        return self.getTags()

    def get_tag(self, name):
        return self.getTag(name)

    def replace_tags(self, tags):
        return self.replaceTags(tags)

    def contains_tag(self, name):
        return self.containsTag(name)


logger.debug("Configure Kotlin adapters for types in it.unibo.tuprolog.utils.*")
