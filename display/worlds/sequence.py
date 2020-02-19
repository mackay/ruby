from display import World
import importlib

from display.gradient import hex_to_RGB
from display import Pixel


class SequenceWorld(World):

    def __init__(self, pixel_count, print_fps=False, timing_ms_per_update=33.3, enable_threading=True):
        super(SequenceWorld, self).__init__(pixel_count, print_fps=print_fps, timing_ms_per_update=timing_ms_per_update, enable_threading=enable_threading)

        self.frames = [ ]
        self.active_frame_ms = None

    def update(self, elapsed_time_ms):

        # if we're in an active frame, just stay in the frame and decrement duration
        if self.active_frame_ms:
            self.active_frame_ms -= elapsed_time_ms
            if self.active_frame_ms <= 0:
                self.active_frame_ms = 0

        # if we've run out of time in our active frame
        else:
            # if we have frames remaining, go to the next frame
            if self.frames:
                frame = self.frames[0]
                self.frames = self.frames[1:]
                self.active_frame_ms = frame["duration_ms"]
                self._show_frame(frame)

        return super(SequenceWorld, self).update(elapsed_time_ms)

    def set_sequence(self, sequence):
        self.active_frame_ms = 0
        self.frames = sequence["frames"]
        self.update(0)

    def _show_frame(self, frame):
        self.clear_sprites()
        for sprite in frame["sprites"]:
            sprite_impl = self._instance_from_class_object(sprite)

            if "dynamics" in sprite:
                for dynamic in sprite["dynamics"]:
                    dynamic_impl = self._instance_from_class_object(dynamic)
                    sprite_impl.add_dynamic(dynamic_impl)

            if "layer" in sprite:
                self.add_sprite( sprite_impl, sprite["layer"])
            else:
                self.add_sprite( sprite_impl )

        self._render_internal()

    def _instance_from_class_object(self, class_object):
        module_name, class_name = class_object["class_path"].rsplit(".", 1)

        class_object["args"] = self._process_args( class_object.get("args", [ ]) )
        class_object["kwargs"] = self._process_kwargs( class_object.get("kwargs", { }) )

        TargetClass = getattr(importlib.import_module(module_name), class_name)
        if class_object["kwargs"].keys():
            if class_object["args"]:
                target = TargetClass( *class_object["args"], **class_object["kwargs"] )
            else:
                target = TargetClass( **class_object["kwargs"] )
        else:
            if class_object["args"]:
                target = TargetClass( *class_object["args"])
            else:
                target = TargetClass( )

        return target

    def _process_args(self, args):
        processed_args = [ ]
        for arg in args:
            processed_args.append( self._process_arg_value(arg) )
        return processed_args

    def _process_kwargs(self, kwargs):
        processed_kwargs = { }
        for key in kwargs:
            processed_kwargs[key] = self._process_arg_value(kwargs[key])
        return processed_kwargs

    def _process_arg_value(self, value):
        if str(value).startswith("Pixel|"):
            rgb = hex_to_RGB(value.split("|")[-1])
            return Pixel.from_tuple(rgb)
        return value
