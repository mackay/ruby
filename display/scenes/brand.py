from display.scenes import Scene
from core.models import Sequence, Frame, FrameSprite, FrameSpriteDynamic


class RubyShine(Scene):

    def __init__(self):
        super(RubyShine, self).__init__("Ruby Shine")


    def add_to_database(self):
        super(RubyShine, self).add_to_database()

        if self.exists():
            self.remove()

        sequence = Sequence.create(name=self.name)
        self._chase_frame(sequence, 0)
        self._pre_final_frame(sequence, 50)
        self._final_frame(sequence, 100)

    def _chase_frame(self, sequence, ordinal):

        chaser_speed_ms = 30
        frame_shoulder = 10

        frame = Frame.create(sequence=sequence,
                             duration_ms=5*1000,
                             ordinal=ordinal)

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.solid.SingleColor",
                                    ordinal=-10,
                                    context={
                                        "args": [
                                            "Pixel|#000000"
                                        ],
                                        "layer": "outer"
                                    })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.solid.SingleColor",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#000000"
                                        ],
                                        "layer": "inner"
                                    })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.ombre.OuterInnterOmbre",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#FF6961", "Pixel|#9B111E"
                                        ],
                                        "kwargs": {
                                            "to_shoulder": frame_shoulder
                                        },
                                        "layer": "outer"
                                    })
        FrameSpriteDynamic.create(sprite=sprite,
                                  class_path="display.dynamics.masks.DualChaserMask",
                                  context={
                                    "args": [ ],
                                    "kwargs": {
                                        "speed_ms": chaser_speed_ms
                                    }
                                  })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.Point",
                                    ordinal=10,
                                    context={
                                        "args": [ "Pixel|#FFFFFF", 0 ],
                                        "layer": "outer"
                                    })
        FrameSpriteDynamic.create(sprite=sprite,
                                  class_path="display.dynamics.chaser.ChaserPosition",
                                  context={
                                    "args": [ ],
                                    "kwargs": {
                                        "speed_ms": chaser_speed_ms
                                    }
                                  })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.Point",
                                    ordinal=10,
                                    context={
                                        "args": [ "Pixel|#FFFFFF", 0 ],
                                        "layer": "outer"
                                    })
        FrameSpriteDynamic.create(sprite=sprite,
                                  class_path="display.dynamics.chaser.ChaserPositionReverse",
                                  context={
                                    "args": [ ],
                                    "kwargs": {
                                        "speed_ms": chaser_speed_ms
                                    }
                                  })

    def _fade_in_frame(self, sequence, ordinal):

        chaser_speed_ms = 30
        frame_shoulder = 10

        frame = Frame.create(sequence=sequence,
                             duration_ms=5*1000,
                             ordinal=ordinal)

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.ombre.OuterInnterOmbre",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#FF6961", "Pixel|#9B111E"
                                        ],
                                        "kwargs": {
                                            "to_shoulder": frame_shoulder
                                        },
                                        "layer": "outer"
                                    })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.ombre.OuterInnterOmbre",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#000000", "Pixel|#000000"
                                        ],
                                        "kwargs": {
                                            "to_shoulder": frame_shoulder
                                        },
                                        "layer": "inner"
                                    })

        FrameSpriteDynamic.create(sprite=sprite,
                                  class_path="display.dynamics.ombre.OmbreMergeToDynamic",
                                  context={
                                    "args": [ ],
                                    "kwargs": {
                                        "speed_ms": chaser_speed_ms
                                    }
                                  })

        FrameSpriteDynamic.create(sprite=sprite,
                                  class_path="display.dynamics.ombre.OmbreMergeFromDynamic",
                                  context={
                                    "args": [ ],
                                    "kwargs": {
                                        "speed_ms": chaser_speed_ms
                                    }
                                  })

    def _pre_final_frame(self, sequence, ordinal):

        chaser_speed_ms = 30
        frame_shoulder = 10

        frame = Frame.create(sequence=sequence,
                             duration_ms=1*1000,
                             ordinal=ordinal)

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.ombre.OuterInnterOmbre",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#FF6961", "Pixel|#9B111E"
                                        ],
                                        "kwargs": {
                                            "to_shoulder": frame_shoulder
                                        },
                                        "layer": "outer"
                                    })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.ombre.OuterInnterOmbre",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#9B111E", "Pixel|#9B111E"
                                        ],
                                        "kwargs": {
                                            "to_shoulder": frame_shoulder
                                        },
                                        "layer": "inner"
                                    })

    def _final_frame(self, sequence, ordinal):
        frame_shoulder = 10

        frame = Frame.create(sequence=sequence,
                             duration_ms=5*1000,
                             ordinal=ordinal)

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.ombre.OuterInnterOmbre",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#FF6961", "Pixel|#9B111E"
                                        ],
                                        "kwargs": {
                                            "to_shoulder": frame_shoulder
                                        },
                                        "layer": "outer"
                                    })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.ombre.OuterInnterOmbre",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#9B111E", "Pixel|#9B111E"
                                        ],
                                        "kwargs": {
                                            "to_shoulder": frame_shoulder
                                        },
                                        "layer": "inner"
                                    })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.Splotch",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#FFF500", 120, 10
                                        ],
                                        "layer": "outer"
                                    })


