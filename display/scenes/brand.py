from display.scenes import Scene
from core.models import Sequence, Frame, FrameSprite, FrameSpriteDynamic


class RubyShine(Scene):

    def __init__(self):
        super(RubyShine, self).__init__("Ruby Shine")

        self.frame_shoulder = 10
        self.chaser_speed_ms = 15

    def add_to_database(self):
        super(RubyShine, self).add_to_database()

        if self.exists():
            self.remove()

        sequence = Sequence.create(name=self.name)
        self._chase_frame(sequence, 0, frame_time_ms=1000*2)
        self._fade_in_frame(sequence, 25, frame_time_ms=1500)
        self._static_background_frame(sequence, 50, frame_time_ms=500)

        for i in range(1, 5):
            self._sparkle_frame(sequence, 100*i, position=120, frame_time_ms=750)
            self._sparkle_frame(sequence, 110*i, position=80, frame_time_ms=750)
            self._sparkle_frame(sequence, 120*i, position=150, frame_time_ms=750)
            self._sparkle_frame(sequence, 130*i, position=120, frame_time_ms=750)


    def _chase_frame(self, sequence, ordinal, frame_time_ms=1000*4):
        frame = Frame.create(sequence=sequence,
                             duration_ms=frame_time_ms,
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
                                            "to_shoulder": self.frame_shoulder
                                        },
                                        "layer": "outer"
                                    })
        FrameSpriteDynamic.create(sprite=sprite,
                                  class_path="display.dynamics.masks.DualChaserMask",
                                  context={
                                    "args": [ ],
                                    "kwargs": {
                                        "speed_ms": self.chaser_speed_ms
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
                                        "speed_ms": self.chaser_speed_ms
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
                                        "speed_ms": self.chaser_speed_ms
                                    }
                                  })

    def _fade_in_frame(self, sequence, ordinal, frame_time_ms=1000*3):
        frame = Frame.create(sequence=sequence,
                             duration_ms=frame_time_ms,
                             ordinal=ordinal)

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.ombre.OuterInnterOmbre",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#FF6961", "Pixel|#9B111E"
                                        ],
                                        "kwargs": {
                                            "to_shoulder": self.frame_shoulder
                                        },
                                        "layer": "outer"
                                    })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.solid.SingleColor",
                                    ordinal=10,
                                    context={
                                        "args": [
                                            "Pixel|#000000"
                                        ],
                                        "layer": "inner"
                                    })

        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.solid.SingleColor",
                                    ordinal=20,
                                    context={
                                        "args": [
                                            "Pixel|#9B111E"
                                        ],
                                        "layer": "inner"
                                    })

        FrameSpriteDynamic.create(sprite=sprite,
                                  class_path="display.dynamics.FadeIn",
                                  context={
                                    "args": [ ],
                                    "kwargs": {
                                        "life_ms": float(frame_time_ms)
                                    }
                                  })


    def _static_background_frame(self, sequence, ordinal, frame_time_ms=1000*1):
        frame = Frame.create(sequence=sequence,
                             duration_ms=frame_time_ms,
                             ordinal=ordinal)

        self._static_background_sprites(frame)

    def _sparkle_frame(self, sequence, ordinal, position=10, frame_time_ms=1000*5):
        frame = Frame.create(sequence=sequence,
                             duration_ms=frame_time_ms,
                             ordinal=ordinal)

        self._static_background_sprites(frame)
        self._sparkle_splotch_sprites(frame, position)




    def _static_background_sprites(self, frame):
        FrameSprite.create( frame=frame,
                            class_path="display.sprites.ombre.OuterInnterOmbre",
                            ordinal=0,
                            context={
                                "args": [
                                    "Pixel|#FF6961", "Pixel|#9B111E"
                                ],
                                "kwargs": {
                                    "to_shoulder": self.frame_shoulder
                                },
                                "layer": "outer"
                            })

        FrameSprite.create( frame=frame,
                            class_path="display.sprites.ombre.OuterInnterOmbre",
                            ordinal=0,
                            context={
                                "args": [
                                    "Pixel|#9B111E", "Pixel|#9B111E"
                                ],
                                "kwargs": {
                                    "to_shoulder": self.frame_shoulder
                                },
                                "layer": "inner"
                            })

    def _sparkle_splotch_sprites(self, frame, position, size=10):
        sprite = FrameSprite.create(frame=frame,
                                    class_path="display.sprites.Splotch",
                                    ordinal=0,
                                    context={
                                        "args": [
                                            "Pixel|#FFF500", position, size
                                        ],
                                        "layer": "outer"
                                    })
        FrameSpriteDynamic.create(sprite=sprite,
                                  class_path="display.dynamics.AlphaLifespan",
                                  context={
                                    "args": [ 1000*1 ]
                                  })
