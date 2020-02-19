from core.models import Sequence

class Scene(object):
    def __init__(self, name):
        self.name = name

    def add_to_database(self):
        pass

    def exists(self):
        return Sequence().select().where(Sequence.name == self.name).exists()

    def remove(self):
        if not self.exists():
            return

        sequence = Sequence.get(Sequence.name == self.name)
        for frame in sequence.frames:
            for sprite in frame.sprites:
                for dynamic in sprite.dynamics:
                    dynamic.delete_instance()
                sprite.delete_instance()
            frame.delete_instance()
        sequence.delete_instance()
