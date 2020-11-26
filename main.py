import bpy
import os


class Car:

    def __init__(self, id, x):
        self.bl_car = None
        self.id = id
        self.name = f"Car-{self.id}"
        self.x = x
        self.y = 0
        self.z = 0

    def add_to_blender(self):
        file_path = r'C:\Users\egeme\Desktop\untitled.blend'
        inner_path = 'Object'
        object_name = 'Cube'

        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, object_name),
            directory=os.path.join(file_path, inner_path),
            filename=object_name
        )
        self.bl_car = bpy.data.objects[-1]
        self.bl_car.name = self.name
        self.bl_car.location.x = self.x
        self.bl_car["Description"] = f"merhaba-{self.id}"


for i in range(3):
    car = Car(i, i*3)
    car.add_to_blender()
    print(car.bl_car.name)
    print(car.bl_car.location.x, end=" ")
    print(car.bl_car.location.y, end=" ")
    print(car.bl_car.location.z)
    print(car.bl_car["Description"])
