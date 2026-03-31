# import omni.ext
# import omni.usd
# import asyncio
# from pxr import UsdGeom, Gf


# print("FILE LOADED 🚀")  # DEBUG


# class ServerRoomExtension(omni.ext.IExt):

#     def on_startup(self, ext_id):
#         print("🔥 EXTENSION STARTED")
#         asyncio.ensure_future(self.setup_scene())

#     async def setup_scene(self):
#         context = omni.usd.get_context()

#         # Create new stage
#         context.new_stage()

#         while not context.get_stage():
#             await asyncio.sleep(0.1)

#         print("✅ Stage ready")

#         stage = context.get_stage()
#         self.create_scene(stage)

#     def create_scene(self, stage):

#         print("🚀 Creating cube...")

#         # Create world
#         world = stage.DefinePrim("/World", "Xform")
#         stage.SetDefaultPrim(world)

#         # Create cube
#         cube = UsdGeom.Cube.Define(stage, "/World/Cube")
#         cube.CreateSizeAttr(2)
#         cube.AddTranslateOp().Set(Gf.Vec3f(0, 0, 1))

#         print("✅ Cube created!")
import omni.ext
import omni.usd
import asyncio
from pxr import UsdGeom, Gf, UsdLux


class ServerRoomExtension(omni.ext.IExt):

    def on_startup(self, ext_id):
        asyncio.ensure_future(self.setup_scene())

    async def setup_scene(self):
        context = omni.usd.get_context()
        context.new_stage()

        while not context.get_stage():
            await asyncio.sleep(0.1)

        stage = context.get_stage()

        # ✅ Create scene
        self.create_server_room(stage)

        # ✅ Save scene
        self.save_stage(stage)

    def create_server_room(self, stage):

        print("🏗️ Creating Server Room...")

        # ---------------- WORLD ----------------
        world = stage.DefinePrim("/World", "Xform")
        stage.SetDefaultPrim(world)

        # ---------------- LIGHTS ----------------
        light = UsdLux.DistantLight.Define(stage, "/World/MainLight")
        light.CreateIntensityAttr(4000)

        top_light = UsdLux.SphereLight.Define(stage, "/World/TopLight")
        top_light.CreateIntensityAttr(3000)
        top_light.AddTranslateOp().Set(Gf.Vec3f(0, 0, 15))

        # ---------------- FLOOR ----------------
        floor = UsdGeom.Cube.Define(stage, "/World/Floor")
        floor.CreateSizeAttr(50)
        floor.AddScaleOp().Set(Gf.Vec3f(1, 1, 0.05))
        floor.AddTranslateOp().Set(Gf.Vec3f(0, 0, -1))

        # ---------------- WALLS ----------------
        walls = [
            (Gf.Vec3f(0, -25, 5), Gf.Vec3f(1, 0.05, 0.4)),
            (Gf.Vec3f(0, 25, 5), Gf.Vec3f(1, 0.05, 0.4)),
            (Gf.Vec3f(-25, 0, 5), Gf.Vec3f(0.05, 1, 0.4)),
            (Gf.Vec3f(25, 0, 5), Gf.Vec3f(0.05, 1, 0.4)),
        ]

        for i, (pos, scale) in enumerate(walls):
            wall = UsdGeom.Cube.Define(stage, f"/World/Wall_{i}")
            wall.CreateSizeAttr(50)
            wall.AddScaleOp().Set(scale)
            wall.AddTranslateOp().Set(pos)

        # ---------------- SERVER RACKS ----------------
        for i in range(6):
            for j in range(4):

                rack = UsdGeom.Cube.Define(stage, f"/World/Rack_{i}_{j}")
                rack.CreateSizeAttr(2)
                rack.AddScaleOp().Set(Gf.Vec3f(1, 1, 3))

                x = i * 5 - 12
                y = j * 5 - 8
                z = 1.5

                rack.AddTranslateOp().Set(Gf.Vec3f(x, y, z))

        # ---------------- COOLING UNITS ----------------
        for i in range(2):
            ac = UsdGeom.Cube.Define(stage, f"/World/AC_{i}")
            ac.CreateSizeAttr(3)
            ac.AddScaleOp().Set(Gf.Vec3f(1, 1, 2))
            ac.AddTranslateOp().Set(Gf.Vec3f(-20 + i * 40, 0, 2))

        print("🚀 Server Room Created Successfully!")

    # ✅ FIXED FUNCTION
    def save_stage(self, stage):
        file_path = "D:/omniverse/server_room.usd"
        stage.GetRootLayer().Export(file_path)
        print(f"💾 Saved at: {file_path}")