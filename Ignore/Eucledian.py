import math

class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for object_id, center in self.center_points.items():
                dist = math.hypot(cx - center[0], cy - center[1])

                if dist < 25:
                    self.center_points[object_id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, object_id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if not same_object_detected:
                object_id = len(self.center_points) + 1
                self.center_points[object_id] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, object_id])

        # Update dictionary with IDs not used removed
        self.center_points = {object_id: center for object_id, center in self.center_points.items() if object_id in [obj_id for _, _, _, _, obj_id in objects_bbs_ids]}

        return objects_bbs_ids

